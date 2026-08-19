from main import resolve_instancia, resolve_todas_instancias
 
 
def prioridade_spt(candidato):
    """
    Regra SPT (Shortest Processing Time).
 
    Quando há empate (disputa pela mesma máquina), escolhe a operação
    com a MENOR duração.
 
    A função 'simular' sempre pega quem tem o MENOR valor de retorno,
    então aqui basta devolver a própria duração.
    """
    return candidato['duracao']
 
 
def solver(path_instancia, verbose=False):
    makespan, cronograma = resolve_instancia(path_instancia, prioridade_spt, verbose=verbose)
    return makespan, cronograma
 
 
if __name__ == '__main__':
    # resolve_todas_instancias('JSPLIB/instances', prioridade_spt)
    solver('ft06', prioridade_spt)
 
