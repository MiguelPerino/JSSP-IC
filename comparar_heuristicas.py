"""
Roda TODAS as heurísticas em TODAS as instâncias e gera uma tabela
comparativa

    Instância | SPT | LPT | MWKR | LWKR | FIFO | Random | Melhor | Gap SPT | Gap LPT | ...

Gap de cada heurística = quão pior ela ficou em relação à MELHOR
heurística naquela instância específica:

    Gap = ((makespan_heuristica - melhor_makespan) / melhor_makespan) * 100
"""
import os
import csv

from main import resolve_instancia, file_handling
from spt import prioridade_spt
from lpt import prioridade_lpt
from mwkr import prioridade_mwkr
from lwkr import prioridade_lwkr
from fifo import prioridade_fifo
from random_priority import solver as random_solver


# Heurísticas "simples" (uma passada só, usam resolve_instancia direto)
prioridades = {
    "SPT": prioridade_spt,
    "LPT": prioridade_lpt,
    "MWKR": prioridade_mwkr,
    "LWKR": prioridade_lwkr,
    "FIFO": prioridade_fifo,
}

NOMES_HEURISTICAS = list(prioridades.keys()) + ["Random"]

pasta_instancias = "instancias"
instancias = sorted(nome for nome in os.listdir(pasta_instancias) if not nome.startswith('.'))

resultados = {}  # resultados[instancia][heuristica] = makespan

print("=" * 80)
print("EXECUTANDO TODAS AS HEURÍSTICAS EM TODAS AS INSTÂNCIAS")
print("=" * 80)
print(f"Total de instâncias: {len(instancias)}")
print(f"Total de heurísticas: {len(NOMES_HEURISTICAS)}")
print()

for idx, nome_instancia in enumerate(instancias, 1):
    print(f"Processando {idx}/{len(instancias)}: {nome_instancia}")

    caminho = os.path.join(pasta_instancias, nome_instancia)
    resultados[nome_instancia] = {}

    # Heurísticas determinísticas (SPT, LPT, MWKR, LWKR, FIFO)
    for nome_heuristica, prioridade_func in prioridades.items():
        makespan, _ = resolve_instancia(caminho, prioridade_func)
        resultados[nome_instancia][nome_heuristica] = makespan

    # Random precisa do solver próprio (roda 10x e fica com a melhor)
    makespan_random, _ = random_solver(caminho, tentativas=10)
    resultados[nome_instancia]["Random"] = makespan_random

print()
print("Gerando arquivo comparacao_jssp.csv...")

with open("comparacao_jssp.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=';')

    header = ["Instancia"] + NOMES_HEURISTICAS + ["Melhor"]
    for nome in NOMES_HEURISTICAS:
        header.append(f"Gap {nome}")
    writer.writerow(header)

    for nome_instancia in instancias:
        makespans = resultados[nome_instancia]
        melhor = min(makespans.values())

        linha = [nome_instancia]
        for nome in NOMES_HEURISTICAS:
            linha.append(makespans[nome])
        linha.append(melhor)

        for nome in NOMES_HEURISTICAS:
            if melhor == 0:
                gap = 0.0
            else:
                gap = ((makespans[nome] - melhor) / melhor) * 100
            linha.append(f"{gap:.2f}")

        writer.writerow(linha)

print()
print("Arquivo comparacao_jssp.csv criado com sucesso!")
print()
print("HEURÍSTICAS TESTADAS:")
for i, nome in enumerate(NOMES_HEURISTICAS, 1):
    print(f"  {i}. {nome}")
print()
print("Colunas do CSV:")
print("  - Makespan de cada heurística")
print("  - Melhor makespan (menor entre todas, naquela instância)")
print("  - Gap de cada heurística em relação ao melhor da instância")
