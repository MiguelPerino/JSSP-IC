from main import resolve_instancia, resolve_todas_instancias, salvar_resumo_csv


def prioridade_lwkr(candidato):
    """
    Regra LWKR (Least Work Remaining).

    O oposto do MWKR: quando há empate, escolhe o job que tem MENOS
    trabalho total pela frente (está mais perto de terminar).

    Ideia: "tira logo do caminho" quem já está quase acabando, pra ele
    liberar as máquinas que ainda vai usar o quanto antes.

    Como a função 'trabalho_restante' já é o número puro (sem inverter o
    sinal), a função 'simular' já pega naturalmente o MENOR valor.
    """
    return candidato['trabalho_restante']


def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_lwkr, verbose=verbose)
    return makespan, cronograma


if __name__ == '__main__':
    resumo = resolve_todas_instancias(
        'instancias',
        prioridade_lwkr,
        caminho_csv_detalhado='solucoesLWKR_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesLWKR_resumo.csv')
