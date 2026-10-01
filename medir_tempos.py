"""
Mede o tempo de execução de cada uma das 6 heurísticas em todas as
instâncias, usando time.perf_counter() (mais preciso que time.time()
para medir duração de código).

Para a heurística Random, o tempo medido já inclui as 10 tentativas
(é o tempo real do método como ele é usado no trabalho, não de uma
tentativa isolada).

"""
import os
import csv
import time

from main import resolve_instancia
from spt import prioridade_spt
from lpt import prioridade_lpt
from mwkr import prioridade_mwkr
from lwkr import prioridade_lwkr
from fifo import prioridade_fifo
from random_priority import solver as random_solver


prioridades = {
    "SPT": prioridade_spt,
    "LPT": prioridade_lpt,
    "MWKR": prioridade_mwkr,
    "LWKR": prioridade_lwkr,
    "FIFO": prioridade_fifo,
}

pasta_instancias = "instancias"
instancias = sorted(nome for nome in os.listdir(pasta_instancias) if not nome.startswith('.'))

resultados = {nome: {} for nome in instancias}

print("=" * 80)
print("MEDINDO TEMPO DE EXECUÇÃO DAS 6 HEURÍSTICAS NAS 162 INSTÂNCIAS")
print("=" * 80)
print()

for idx, nome_instancia in enumerate(instancias, 1):
    caminho = os.path.join(pasta_instancias, nome_instancia)
    print(f"[{idx}/{len(instancias)}] {nome_instancia}")

    for nome_h, func in prioridades.items():
        inicio = time.perf_counter()
        resolve_instancia(caminho, func)
        fim = time.perf_counter()
        resultados[nome_instancia][nome_h] = fim - inicio

    inicio = time.perf_counter()
    random_solver(caminho, tentativas=10)
    fim = time.perf_counter()
    resultados[nome_instancia]["Random"] = fim - inicio

print()
print("Salvando tempos_execucao.csv...")

nomes_heuristicas = list(prioridades.keys()) + ["Random"]

with open("tempos_execucao.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["Instancia"] + [f"Tempo_{h}(s)" for h in nomes_heuristicas])

    for nome_instancia in instancias:
        linha = [nome_instancia]
        for h in nomes_heuristicas:
            linha.append(f"{resultados[nome_instancia][h]:.6f}")
        writer.writerow(linha)

print()
print(f"{'Heurística':<10}{'Tempo médio (s)':>18}{'Tempo total (s)':>18}")
print("-" * 46)

for h in nomes_heuristicas:
    tempos = [resultados[nome][h] for nome in instancias]
    media = sum(tempos) / len(tempos)
    total = sum(tempos)
    print(f"{h:<10}{media:>18.4f}{total:>18.4f}")
