import os


def file_handling(path_instancia):
    """
    Lê uma instância no formato 'standard' da JSPLIB.

    Formato do arquivo:
        (linhas de comentário começando com # são ignoradas)
        n_jobs n_machines
        m1 d1 m2 d2 m3 d3 ...    <- job 0: pares (máquina, duração)
        m1 d1 m2 d2 m3 d3 ...    <- job 1
        ...

    Retorna:
        n_jobs: número de jobs
        n_machines: número de máquinas
        jobs: lista de jobs, onde cada job é uma lista de tuplas (maquina, duracao)
              na ORDEM em que devem ser executadas (isso não pode mudar!)

    Exemplo de retorno para o job 0 do ft06:
        jobs[0] = [(2, 1), (0, 3), (1, 6), (3, 7), (5, 3), (4, 6)]
        -> esse job tem que passar pela máquina 2 (1 unidade de tempo),
           DEPOIS máquina 0 (3 unidades), DEPOIS máquina 1 (6 unidades), etc.   
    """
    with open(path_instancia, 'r', encoding='utf-8') as f:
        # remove linhas vazias e linhas de comentário (#)
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.strip().startswith('#')]

    n_jobs, n_machines = map(int, linhas[0].split())

    jobs = []
    for i in range(1, n_jobs + 1):
        valores = list(map(int, linhas[i].split()))

        operacoes = []
        # os valores vêm em pares: maquina, duracao, maquina, duracao, ...
        for k in range(0, len(valores), 2):
            maquina = valores[k]
            duracao = valores[k + 1]
            operacoes.append((maquina, duracao))

        jobs.append(operacoes)

    return n_jobs, n_machines, jobs


def simular(jobs, n_machines, prioridade_func, verbose=False):
    """
    Simula a construção de um cronograma (schedule) para o Job Shop.

    Ideia geral (passo a passo):

    1. Cada job só pode ter UMA operação "disponível" por vez: a próxima
       da sua fila (não dá pra fazer a operação 3 antes da 2).

    2. Para cada job ainda não terminado, calculamos o "earliest start time"
       (est) daquela próxima operação: é o maior entre
            - quando o JOB ficou livre (terminou a operação anterior)
            - quando a MÁQUINA que essa operação precisa ficou livre

    3. Olhamos todos esses candidatos e achamos o menor "est" entre todos.
       Isso significa: essa é a operação que PODE começar mais cedo.

    4. Se só uma operação tem esse "est" mínimo, agendamos ela direto.
       Se MAIS DE UMA empatam nesse menor horário, significa que elas estão
       disputando a mesma máquina de verdade - aí usamos a regra de
       prioridade (prioridade_func) pra decidir quem vai primeiro.

    5. Atualizamos os relógios (máquina e job) e repetimos até não sobrar
       nenhuma operação.

    prioridade_func: função que recebe um candidato (dict) e devolve um
                      número. Quem tiver o MENOR número, vence o desempate.
                      (ex: pra SPT, a função devolve a duração da operação)

    Retorna:
        makespan: tempo total do cronograma
        cronograma: lista de operações agendadas, cada uma é um dict com
                    job, op_index, machine, inicio, fim
    """
    n_jobs = len(jobs)

    next_op = [0] * n_jobs       # próxima operação (índice) de cada job
    job_ready = [0] * n_jobs     # quando o job fica livre p/ próxima operação
    machine_free = [0] * n_machines  # quando cada máquina fica livre

    total_ops = sum(len(job) for job in jobs)
    agendadas = 0

    cronograma = []

    while agendadas < total_ops:

        # PASSO 1 e 2: monta a lista de candidatos
        candidatos = []
        for j in range(n_jobs):
            if next_op[j] < len(jobs[j]):  # job ainda tem operação pendente
                maquina, duracao = jobs[j][next_op[j]]

                est = max(job_ready[j], machine_free[maquina])

                # soma das durações da operação atual + todas as futuras
                # (usado depois pela regra MWKR, mas calculamos sempre)
                trabalho_restante = sum(d for (_, d) in jobs[j][next_op[j]:])

                candidatos.append({
                    'job': j,
                    'op_index': next_op[j],
                    'machine': maquina,
                    'duracao': duracao,
                    'est': est,
                    'job_ready': job_ready[j],
                    'trabalho_restante': trabalho_restante,
                })

        # PASSO 3: acha o menor "est" entre os candidatos
        menor_est = min(c['est'] for c in candidatos)
        empatados = [c for c in candidatos if c['est'] == menor_est]

        # PASSO 4: resolve o empate com a regra de prioridade
        if len(empatados) == 1:
            escolhido = empatados[0]
        else:
            escolhido = min(empatados, key=prioridade_func)

        # PASSO 5: agenda a operação escolhida e atualiza relógios
        j = escolhido['job']
        m = escolhido['machine']
        inicio = escolhido['est']
        fim = inicio + escolhido['duracao']

        cronograma.append({
            'job': j,
            'op_index': escolhido['op_index'],
            'machine': m,
            'inicio': inicio,
            'fim': fim,
        })

        if verbose:
            flag = " <- tinha empate, decidido pela regra de prioridade" if len(empatados) > 1 else ""
            print(f"  Agendado: Job {j} | Op {escolhido['op_index']} | "
                  f"Máquina {m} | Início={inicio} Fim={fim}{flag}")

        machine_free[m] = fim
        job_ready[j] = fim
        next_op[j] += 1
        agendadas += 1

    makespan = max(machine_free)
    return makespan, cronograma


def resolve_instancia(path_instancia, prioridade_func, verbose=False):
    """Lê uma instância e roda a simulação com a regra de prioridade dada."""
    n_jobs, n_machines, jobs = file_handling(path_instancia)
    makespan, cronograma = simular(jobs, n_machines, prioridade_func, verbose=verbose)
    return makespan, cronograma


def resolve_todas_instancias(pasta_instancias, prioridade_func):
    "Roda a heurística em todas as instâncias de uma pasta e imprime o makespan."
    instancias = sorted(os.listdir(pasta_instancias))

    for nome in instancias:
        caminho = os.path.join(pasta_instancias, nome)
        if not os.path.isfile(caminho):
            continue

        makespan, _ = resolve_instancia(caminho, prioridade_func)
        print(f"{nome}: makespan = {makespan}")
