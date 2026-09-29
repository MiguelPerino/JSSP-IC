"""
Calcula o GAP da MELHOR heurística de cada instância contra o valor
oficial (optimum/BKS) do JSPLIB — usando o CSV JÁ CONGELADO
(comparacao_jssp_OFICIAL_artigo.csv) como fonte, ao invés de rodar as
heurísticas de novo.

Isso garante 100% de consistência com o restante do artigo: os mesmos
valores de makespan (inclusive os da heurística Random) usados nas
tabelas de GAP interno e de vitórias são os mesmos usados aqui.
"""
import csv
import json

ARQUIVO_CONGELADO = "comparacao_jssp.csv"
ARQUIVO_REFERENCIAS = "instances.json"
ARQUIVO_SAIDA = "gap_vs_otimo.csv"

HEURISTICAS = ["SPT", "LPT", "MWKR", "LWKR", "FIFO", "Random"]


def carregar_referencias(caminho_json):
    with open(caminho_json, encoding='utf-8') as f:
        dados = json.load(f)

    referencias = {}
    for item in dados:
        nome = item['name']
        if item.get('optimum') is not None:
            referencias[nome] = (item['optimum'], 'optimum')
        elif item.get('bounds') is not None:
            referencias[nome] = (item['bounds']['upper'], 'upper_bound')
        else:
            referencias[nome] = (None, 'sem_referencia')
    return referencias


def main():
    referencias = carregar_referencias(ARQUIVO_REFERENCIAS)

    linhas_saida = []

    with open(ARQUIVO_CONGELADO, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            nome_instancia = row['Instancia']
            valores = {h: int(row[h]) for h in HEURISTICAS}
            melhor_valor = min(valores.values())

            # quais heurísticas empataram no menor valor (para exibição)
            vencedoras = [h for h, v in valores.items() if v == melhor_valor]
            melhor_heuristica = "/".join(vencedoras)

            valor_ref, tipo_ref = referencias.get(nome_instancia, (None, 'nao_encontrada'))

            if valor_ref is not None:
                gap = ((melhor_valor - valor_ref) / valor_ref) * 100
                gap_str = f"{gap:.2f}"
            else:
                gap_str = ""

            linhas_saida.append([
                nome_instancia, melhor_heuristica, melhor_valor,
                valor_ref if valor_ref is not None else "",
                tipo_ref, gap_str
            ])

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Instancia", "Melhor_Heuristica", "Melhor_Makespan",
                          "Referencia_Oficial", "Tipo_Referencia", "Gap(%)"])
        writer.writerows(linhas_saida)

    # resumo para conferência
    gaps = [float(l[5]) for l in linhas_saida if l[5] != ""]
    sem_ref = sum(1 for l in linhas_saida if l[5] == "")

    print("=" * 70)
    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
    print(f"Instâncias com GAP calculado: {len(gaps)}")
    print(f"Instâncias sem referência oficial: {sem_ref}")
    print(f"GAP médio (melhor das 6 vs. ótimo/BKS oficial): {sum(gaps)/len(gaps):.2f}%")
    print(f"Menor GAP: {min(gaps):.2f}%  |  Maior GAP: {max(gaps):.2f}%")
    print("=" * 70)


if __name__ == '__main__':
    main()
