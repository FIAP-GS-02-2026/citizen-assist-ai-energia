"""Compara as alternativas de recarga e grava os resultados em resultados/*.csv.

Execute com: python analise.py
"""

import csv
import os

import energia as e

PASTA_RESULTADOS = os.path.join(e.PASTA, "resultados")

VEICULOS = (
    # (nome, chave da bateria, chave da autonomia)
    ("Bike elétrica", "bateria_bike", "autonomia_bike"),
    ("Patinete elétrico", "bateria_patinete", "autonomia_patinete"),
)

BANDEIRAS = (
    ("verde", 0.0),
    ("amarela", "bandeira_amarela"),
    ("vermelha 1", "bandeira_vermelha_1"),
    ("vermelha 2", "bandeira_vermelha_2"),
)


def tarifas(p):
    """Tarifas usadas na comparação, em R$/kWh e sem tributos."""
    return {
        "convencional": e.tarifa_r_kwh(p["tusd_b1"], p["te_b1"]),
        "branca_fora_ponta": e.tarifa_r_kwh(p["tusd_branca_fora_ponta"], p["te_branca_fora_ponta"]),
        "branca_intermediario": e.tarifa_r_kwh(p["tusd_branca_intermediario"], p["te_branca_intermediario"]),
        "branca_ponta": e.tarifa_r_kwh(p["tusd_branca_ponta"], p["te_branca_ponta"]),
        "tusd_b1": p["tusd_b1"] / 1000,
    }


def comparar(p, km_por_dia=None, eficiencia=None):
    """Monta a comparação das alternativas para cada veículo, num período de 12 meses."""
    km_por_dia = p["km_por_dia"] if km_por_dia is None else km_por_dia
    eficiencia = p["eficiencia_carregador"] if eficiencia is None else eficiencia
    t = tarifas(p)
    fator = p["fator_emissao_sin_2025"]
    linhas = []
    for nome, chave_bateria, chave_autonomia in VEICULOS:
        wh_km = e.consumo_por_km(p[chave_bateria], p[chave_autonomia])
        kwh_ano = e.energia_anual_kwh(wh_km, km_por_dia, p["dias_uso_ano"], eficiencia)
        emissao_rede = e.emissao_kg(kwh_ano, fator)

        # A) Rede, tarifa convencional (bandeira verde)
        custo_conv = e.custo(kwh_ano, t["convencional"])
        linhas.append({
            "veiculo": nome, "alternativa": "A) Tomada, tarifa convencional (bandeira verde)",
            "kwh_ano": kwh_ano, "custo_ano_rs": custo_conv, "investimento_rs": 0.0,
            "payback_anos": "", "co2_kg_ano": emissao_rede,
            "viabilidade": "Imediata: qualquer tomada de casa, sem investimento nem cadastro.",
        })
        # B) Rede, Tarifa Branca, recarga fora de ponta
        custo_branca = e.custo(kwh_ano, t["branca_fora_ponta"])
        linhas.append({
            "veiculo": nome, "alternativa": "B) Tomada, Tarifa Branca fora de ponta",
            "kwh_ano": kwh_ano, "custo_ano_rs": custo_branca, "investimento_rs": 0.0,
            "payback_anos": "", "co2_kg_ano": emissao_rede,
            "viabilidade": ("Exige pedir a Tarifa Branca para a casa inteira; só compensa se a casa usar pouca "
                            "energia no horário de ponta, que é bem mais caro. Fins de semana e feriados "
                            "nacionais são sempre fora de ponta."),
        })
        # C) Solar conectada à rede, parcela do sistema dimensionada para a recarga
        wp = e.potencia_solar_wp(kwh_ano, p["irradiacao_inclinada_media"], p["taxa_desempenho"])
        investimento = wp * p["preco_solar_wp"]
        # O valor real do Fio B da Enel não está publicado na tabela de tarifas. Por isso a
        # alternativa C sai como faixa: pior caso (Fio B = TUSD inteira) e melhor caso
        # (Fio B desprezível, mesma conta da regra antiga do art. 26).
        for regra_antiga, rotulo in ((False, "sistema novo em 2026, pior caso"),
                                     (True, "sistema novo em 2026, melhor caso")):
            valor = e.valor_kwh_compensado(t["convencional"], t["tusd_b1"], p["fio_b_2026"], regra_antiga)
            custo_residual = kwh_ano * (t["convencional"] - valor)
            economia = custo_conv - custo_residual
            linhas.append({
                "veiculo": nome, "alternativa": f"C) Solar em casa ({rotulo})",
                "kwh_ano": kwh_ano, "custo_ano_rs": custo_residual, "investimento_rs": investimento,
                "payback_anos": e.payback_anos(investimento, economia), "co2_kg_ano": 0.0,
                "potencia_wp": wp,
                "viabilidade": ("Só faz sentido como parte de um sistema solar da casa toda: exige telhado ou "
                                "área própria (ou geração compartilhada), investimento e pedido de acesso à Enel. "
                                "Um sistema só para a bike teria custos fixos que o cálculo proporcional não inclui."),
            })
    return linhas


def recarga_completa(p):
    """Custo de uma carga completa (bateria de 0 a 100%) em cada bandeira."""
    t = tarifas(p)
    linhas = []
    for nome, chave_bateria, _ in VEICULOS:
        kwh = e.energia_da_tomada_kwh(p[chave_bateria], p["eficiencia_carregador"])
        for cor, chave in BANDEIRAS:
            acrescimo = p[chave] if isinstance(chave, str) else chave
            linhas.append({
                "veiculo": nome, "bandeira": cor, "kwh_tomada": kwh,
                "custo_rs": e.custo(kwh, t["convencional"], acrescimo),
            })
    return linhas


def sensibilidade(p):
    """Como o custo anual da bike muda com a distância diária e a eficiência do carregador.

    A coluna custo_se_conta_final_dobrar mostra o custo caso tributos e outros itens
    da conta dobrem o valor: serve para checar se a conclusão muda (não muda).
    """
    linhas = []
    for km in (2, 6, 10, 20):
        for eficiencia in (0.75, 0.85, 0.95):
            bike = [c for c in comparar(p, km_por_dia=km, eficiencia=eficiencia)
                    if c["veiculo"] == "Bike elétrica"]
            linhas.append({
                "km_por_dia": km, "eficiencia": eficiencia,
                "kwh_ano": bike[0]["kwh_ano"],
                "custo_ano_convencional_rs": bike[0]["custo_ano_rs"],
                "custo_se_conta_final_dobrar_rs": bike[0]["custo_ano_rs"] * 2,
                "economia_ano_tarifa_branca_rs": bike[0]["custo_ano_rs"] - bike[1]["custo_ano_rs"],
            })
    return linhas


def sensibilidade_solar(p):
    """Retorno da parcela solar com preços e taxas de desempenho diferentes (bike, pior caso do Fio B).

    Preços: R$ 2,08/Wp (menor média estadual do levantamento), R$ 2,45/Wp (média nacional)
    e R$ 3,06/Wp (premissa da equipe: 25% acima da média, já que SP não está entre os mais baratos).
    """
    linhas = []
    for preco in (2.08, 2.45, 3.06):
        for td in (0.70, 0.75, 0.80):
            q = dict(p, preco_solar_wp=preco, taxa_desempenho=td)
            bike = [c for c in comparar(q) if c["veiculo"] == "Bike elétrica"]
            linhas.append({
                "preco_rs_wp": preco, "taxa_desempenho": td,
                "potencia_wp": bike[2]["potencia_wp"], "investimento_rs": bike[2]["investimento_rs"],
                "payback_pior_caso_anos": bike[2]["payback_anos"],
                "payback_melhor_caso_anos": bike[3]["payback_anos"],
            })
    return linhas


def solar_mensal(p):
    """Geração mês a mês da parcela solar da bike, comparada ao consumo mensal médio."""
    comp = comparar(p)
    bike = [c for c in comp if c["veiculo"] == "Bike elétrica"]
    wp = bike[2]["potencia_wp"]
    consumo_mes = bike[0]["kwh_ano"] / 12
    return [
        {"mes": g["mes"], "geracao_kwh": g["kwh"], "consumo_medio_kwh": consumo_mes,
         "saldo_kwh": g["kwh"] - consumo_mes}
        for g in e.geracao_mensal_kwh(wp, e.carregar_irradiacao(), p["taxa_desempenho"])
    ]


def gravar_csv(nome, linhas):
    """Grava uma lista de dicionários em resultados/<nome>.csv (UTF-8 com BOM para o Excel)."""
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    campos = []
    for linha in linhas:
        for campo in linha:
            if campo not in campos:
                campos.append(campo)
    caminho = os.path.join(PASTA_RESULTADOS, f"{nome}.csv")
    with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in linha.items()})
    return caminho


def brl(valor):
    """Formata em reais no padrão brasileiro."""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


def main():
    p = e.carregar_premissas()
    fatores = e.carregar_fator_emissao()
    comp = comparar(p)
    cargas = recarga_completa(p)
    sens = sensibilidade(p)
    sens_solar = sensibilidade_solar(p)
    mensal = solar_mensal(p)
    for nome, linhas in (("comparacao", comp), ("recarga_completa", cargas), ("sensibilidade", sens),
                         ("sensibilidade_solar", sens_solar), ("solar_mensal", mensal)):
        gravar_csv(nome, linhas)

    print("Recarga de bike e patinete elétrico em São Paulo: comparação em 12 meses")
    print(f"Premissas: {num(p['km_por_dia'], 0)} km por dia, {num(p['dias_uso_ano'], 0)} dias por ano, "
          f"eficiência do carregador {num(p['eficiencia_carregador'] * 100, 0)}%. Tarifas sem tributos.\n")
    for veiculo in ("Bike elétrica", "Patinete elétrico"):
        print(f"== {veiculo} ==")
        for c in (c for c in comp if c["veiculo"] == veiculo):
            payback = f" | retorno em {num(c['payback_anos'])} anos" if c["payback_anos"] != "" else ""
            investimento = f" | investimento {brl(c['investimento_rs'])} ({num(c['potencia_wp'])} Wp)" if c["investimento_rs"] else ""
            print(f"  {c['alternativa']}: {num(c['kwh_ano'])} kWh/ano | {brl(c['custo_ano_rs'])}/ano"
                  f"{investimento}{payback} | {num(c['co2_kg_ano'], 2)} kg CO2/ano")
        print()
    print("Carga completa (0 a 100%), tarifa convencional:")
    for c in cargas:
        print(f"  {c['veiculo']}, bandeira {c['bandeira']}: {num(c['kwh_tomada'], 3)} kWh = {brl(c['custo_rs'])}")
    print(f"\nFator de emissão do SIN em 2025: média anual {num(p['fator_emissao_sin_2025'] * 1000)} g CO2/kWh "
          f"(meses de {num(min(fatores) * 1000)} a {num(max(fatores) * 1000)}).")
    menor = min(mensal, key=lambda m: m["geracao_kwh"])
    print(f"Solar: no mês mais fraco ({menor['mes']}) a parcela gera {num(menor['geracao_kwh'], 2)} kWh "
          f"para um consumo médio de {num(menor['consumo_medio_kwh'], 2)} kWh; o saldo dos outros meses vira crédito.")
    paybacks = [c["payback_pior_caso_anos"] for c in sens_solar]
    print(f"Retorno da parcela solar da bike (pior caso do Fio B), variando preço e desempenho: "
          f"de {num(min(paybacks))} a {num(max(paybacks))} anos.")
    custos = [c["custo_ano_convencional_rs"] for c in sens]
    print(f"Custo anual da bike na tomada, de 2 a 20 km/dia e eficiência de 75% a 95%: "
          f"de {brl(min(custos))} a {brl(max(custos))}.")
    print("\nResultados gravados em resultados/: comparacao.csv, recarga_completa.csv, sensibilidade.csv, "
          "sensibilidade_solar.csv, solar_mensal.csv")
    print("Estimativas, não valores garantidos: ver premissas e limitações no README.")


if __name__ == "__main__":
    main()
