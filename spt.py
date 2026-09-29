from main import resolve_instancia, resolve_todas_instancias, salvar_resumo_csv


def prioridade_spt(candidato):
    """
    Regra SPT (Shortest Processing Time).

    Quando há empate (disputa pela mesma máquina), escolhe a operação
    com a MENOR duração.
    """
    return candidato['duracao']


def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_spt, verbose=verbose)
    return makespan, cronograma


if __name__ == '__main__':
    resumo = resolve_todas_instancias(
        'instancias',
        prioridade_spt,
        caminho_csv_detalhado='solucoesSPT_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesSPT_resumo.csv')