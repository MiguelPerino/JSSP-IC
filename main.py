import os
import csv


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
    """
    with open(path_instancia, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.strip().startswith('#')]

    n_jobs, n_machines = map(int, linhas[0].split())

    jobs = []
    for i in range(1, n_jobs + 1):
        valores = list(map(int, linhas[i].split()))

        operacoes = []
        for k in range(0, len(valores), 2):
            maquina = valores[k]
            duracao = valores[k + 1]
            operacoes.append((maquina, duracao))

        jobs.append(operacoes)

    return n_jobs, n_machines, jobs


def simular(jobs, n_machines, prioridade_func, verbose=False):
    """
    Simula a construção de um cronograma (schedule) para o Job Shop.

    1. Cada job só pode ter UMA operação "disponível" por vez: a próxima
       da sua fila.
    2. Para cada job ainda não terminado, calculamos o "earliest start time"
       (est) daquela próxima operação: o maior entre quando o JOB ficou
       livre e quando a MÁQUINA que essa operação precisa ficou livre.
    3. Achamos o menor "est" entre todos os candidatos.
    4. Se só uma operação tem esse "est" mínimo, agendamos ela direto.
       Se houver empate, usamos a regra de prioridade (prioridade_func)
       pra decidir quem vai primeiro.
    5. Atualizamos os relógios e repetimos até não sobrar nenhuma operação.

    prioridade_func: recebe um candidato (dict) e devolve um número.
                      Quem tiver o MENOR número, vence o desempate.
    """
    n_jobs = len(jobs)

    next_op = [0] * n_jobs
    job_ready = [0] * n_jobs
    machine_free = [0] * n_machines

    total_ops = sum(len(job) for job in jobs)
    agendadas = 0

    cronograma = []

    while agendadas < total_ops:

        candidatos = []
        for j in range(n_jobs):
            if next_op[j] < len(jobs[j]):
                maquina, duracao = jobs[j][next_op[j]]
                est = max(job_ready[j], machine_free[maquina])
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

        menor_est = min(c['est'] for c in candidatos)
        empatados = [c for c in candidatos if c['est'] == menor_est]

        if len(empatados) == 1:
            escolhido = empatados[0]
        else:
            escolhido = min(empatados, key=prioridade_func)

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


def salvar_cronograma_unificado_csv(cronograma_completo, caminho_csv):
    """
    Salva o cronograma de TODAS as instâncias em um único CSV grande,
    com as colunas: Instancia, Job, Operacao, Maquina, Inicio, Fim.
    """
    with open(caminho_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Instancia', 'Job', 'Operacao', 'Maquina', 'Inicio', 'Fim'])

        for nome_instancia, op in cronograma_completo:
            writer.writerow([nome_instancia, op['job'], op['op_index'], op['machine'], op['inicio'], op['fim']])


def resolve_todas_instancias(pasta_instancias, prioridade_func, caminho_csv_detalhado=None):
    """
    Roda a heurística em todas as instâncias de uma pasta, imprime o makespan
    de cada uma e devolve o resumo (lista de tuplas nome/makespan).

    Se 'caminho_csv_detalhado' for informado, salva UM ÚNICO CSV com o
    cronograma completo de TODAS as instâncias juntas.
    """
    instancias = sorted(os.listdir(pasta_instancias))

    resumo = []
    cronograma_completo = []

    for nome in instancias:
        if nome.startswith('.'):
            # ignora arquivos ocultos/de sistema, ex: .gitkeep, .DS_Store
            continue

        caminho = os.path.join(pasta_instancias, nome)
        if not os.path.isfile(caminho):
            continue

        makespan, cronograma = resolve_instancia(caminho, prioridade_func)
        print(f"{nome}: makespan = {makespan}")
        resumo.append((nome, makespan))

        cronograma_ordenado = sorted(cronograma, key=lambda op: op['inicio'])
        for op in cronograma_ordenado:
            cronograma_completo.append((nome, op))

    if caminho_csv_detalhado:
        salvar_cronograma_unificado_csv(cronograma_completo, caminho_csv_detalhado)

    return resumo


def salvar_resumo_csv(resumo, caminho_csv):
    """Salva um único CSV com o makespan de cada instância."""
    with open(caminho_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Instancia', 'Makespan'])
        for nome, makespan in resumo:
            writer.writerow([nome, makespan])