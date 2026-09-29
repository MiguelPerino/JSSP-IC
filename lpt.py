from main import resolve_instancia, resolve_todas_instancias, salvar_resumo_csv


def prioridade_lpt(candidato):
    """
    Regra LPT (Longest Processing Time).

    O oposto do SPT: quando há empate (disputa pela mesma máquina),
    escolhe a operação com a MAIOR duração.

    A função 'simular' sempre pega quem tem o MENOR valor de retorno,
    então aqui invertemos o sinal da duração pra "enganar" a comparação:
    quanto MAIOR a duração, MENOR fica o valor negativo, e por isso vence.
    """
    return -candidato['duracao']


def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_lpt, verbose=verbose)
    return makespan, cronograma


if __name__ == '__main__':
    resumo = resolve_todas_instancias(
        'instancias',
        prioridade_lpt,
        caminho_csv_detalhado='solucoesLPT_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesLPT_resumo.csv')
