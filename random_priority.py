import os
import random
from main import (
    resolve_instancia,
    salvar_cronograma_unificado_csv,
    salvar_resumo_csv,
)


def prioridade_random(candidato):
    """
    Quando há empate, escolhe aleatoriamente entre os candidatos
    empatados (não usa nenhum dado do job, só sorteia um número). #Pode gerar resultados bons, vemos quando rodamos com todas as outras heuristicas
    """
    return random.random()


def solver(path_instancia, verbose=False, tentativas=10):
    """
    Como a escolha é aleatória, rodamos a simulação várias vezes
    (10) pra essa MESMA instância e devolvemos a MELHOR solução
    encontrada entre as tentativas
    """
    melhor_makespan = float('inf')
    melhor_cronograma = None

    for _ in range(tentativas):
        makespan, cronograma = resolve_instancia(path_instancia, prioridade_random, verbose=verbose)
        if makespan < melhor_makespan:
            melhor_makespan = makespan
            melhor_cronograma = cronograma

    return melhor_makespan, melhor_cronograma


def resolve_todas_instancias_random(pasta_instancias, tentativas=10, caminho_csv_detalhado=None):
    """
    Versão própria do 'resolve_todas_instancias' pra regra Random, já que
    aqui cada instância precisa rodar várias vezes (não só uma).
    """
    instancias = sorted(os.listdir(pasta_instancias))

    resumo = []
    cronograma_completo = []

    for nome in instancias:
        if nome.startswith('.'):
            continue

        caminho = os.path.join(pasta_instancias, nome)
        if not os.path.isfile(caminho):
            continue

        makespan, cronograma = solver(caminho, tentativas=tentativas)
        print(f"{nome}: makespan = {makespan} (melhor de {tentativas} tentativas)")
        resumo.append((nome, makespan))

        cronograma_ordenado = sorted(cronograma, key=lambda op: op['inicio'])
        for op in cronograma_ordenado:
            cronograma_completo.append((nome, op))

    if caminho_csv_detalhado:
        salvar_cronograma_unificado_csv(cronograma_completo, caminho_csv_detalhado)

    return resumo


if __name__ == '__main__':
    resumo = resolve_todas_instancias_random(
        'instancias',
        tentativas=10,
        caminho_csv_detalhado='solucoesRandom_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesRandom_resumo.csv')
