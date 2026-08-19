from main import resolve_instancia, resolve_todas_instancias, salvar_resumo_csv


def prioridade_fifo(candidato):
    """
    Regra FIFO (First In First Out).

    Quando há empate, escolhe o job que ficou disponível para essa
    operação HÁ MAIS TEMPO (ou seja, o menor valor de 'job_ready').

    Ideia: quem está esperando na fila há mais tempo, passa primeiro -
    igual uma fila de banco.
    """
    return candidato['job_ready']


def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_fifo, verbose=verbose)
    return makespan, cronograma


if __name__ == '__main__':
    resumo = resolve_todas_instancias(
        'instancias',
        prioridade_fifo,
        caminho_csv_detalhado='solucoesFIFO_detalhado.csv'
    )
    salvar_resumo_csv(resumo, 'solucoesFIFO_resumo.csv')
