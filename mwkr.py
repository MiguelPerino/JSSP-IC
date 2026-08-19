from main import resolve_instancia, resolve_todas_instancias, salvar_resumo_csv


def prioridade_mwkr(candidato):
    """
    Regra MWKR (Most Work Remaining).

    Quando há empate, escolhe o job que ainda tem MAIS trabalho total
    pela frente (soma da duração da operação atual + todas as futuras
    daquele job).

    Ideia: prioriza quem "tem mais chão pela frente", pra esse job não
    virar gargalo lá na frente do cronograma.

    Como a função 'simular' sempre pega o MENOR valor, invertemos o sinal
    do trabalho_restante (igual fizemos no LPT).
    """
    return -candidato['trabalho_restante']


def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_mwkr, verbose=verbose)
    return makespan, cronograma


if __name__ == '__main__':
    resumo = resolve_todas_instancias(
        'instancias',
        prioridade_mwkr,
        caminho_csv_detalhado='solucoesMWKR_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesMWKR_resumo.csv')
