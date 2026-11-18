"""Cálculos de energia, custo e emissão da recarga de bike e patinete elétrico.

Todas as funções são puras: recebem números e devolvem números. Os dados e as
premissas ficam em dados/*.csv, com fonte e tipo (oficial, fabricante, mercado
ou premissa da equipe). Unidades: Wh, kWh, R$/kWh, kWh/m².dia, tCO2/MWh.
"""

import csv
import os

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA, "dados")


def carregar_premissas(caminho=None):
    """Lê dados/premissas.csv e devolve {chave: valor (float)}."""
    caminho = caminho or os.path.join(PASTA_DADOS, "premissas.csv")
    with open(caminho, encoding="utf-8") as arquivo:
        return {linha["chave"]: float(linha["valor"]) for linha in csv.DictReader(arquivo)}


def carregar_irradiacao(caminho=None):
    """Lê a irradiação mensal de São Paulo (CRESESB SunData)."""
    caminho = caminho or os.path.join(PASTA_DADOS, "irradiacao_sao_paulo.csv")
    with open(caminho, encoding="utf-8") as arquivo:
        return [
            {
                "mes": linha["mes"],
                "hsp": float(linha["inclinado_21_graus_kwh_m2_dia"]),
                "dias": int(linha["dias_no_mes"]),
            }
            for linha in csv.DictReader(arquivo)
        ]


def carregar_fator_emissao(caminho=None):
    """Lê os fatores médios mensais de emissão do SIN (MCTI)."""
    caminho = caminho or os.path.join(PASTA_DADOS, "fator_emissao_sin.csv")
    with open(caminho, encoding="utf-8") as arquivo:
        return [float(linha["tco2_por_mwh"]) for linha in csv.DictReader(arquivo)]


# ---------- energia ----------

def consumo_por_km(bateria_wh, autonomia_km):
    """Energia que sai da bateria por km rodado (Wh/km)."""
    if bateria_wh <= 0 or autonomia_km <= 0:
        raise ValueError("bateria e autonomia precisam ser positivas")
    return bateria_wh / autonomia_km


def energia_da_tomada_kwh(energia_bateria_wh, eficiencia):
    """Energia tirada da tomada para repor energia_bateria_wh na bateria (kWh).

    A tomada fornece mais do que a bateria guarda, porque parte vira calor:
    energia_tomada = energia_bateria / eficiência.
    """
    if not 0 < eficiencia <= 1:
        raise ValueError("eficiência precisa estar entre 0 e 1")
    return energia_bateria_wh / eficiencia / 1000


def energia_anual_kwh(wh_por_km, km_por_dia, dias_por_ano, eficiencia):
    """Energia tirada da tomada em um ano de uso (kWh/ano)."""
    return energia_da_tomada_kwh(wh_por_km * km_por_dia * dias_por_ano, eficiencia)


# ---------- tarifas ----------

def tarifa_r_kwh(tusd_r_mwh, te_r_mwh):
    """Soma TUSD e TE (R$/MWh) e converte para R$/kWh. Não inclui tributos."""
    return (tusd_r_mwh + te_r_mwh) / 1000


def custo(kwh, tarifa, acrescimo_bandeira=0.0):
    """Custo em R$ de kwh pela tarifa (R$/kWh) mais o acréscimo da bandeira."""
    return kwh * (tarifa + acrescimo_bandeira)


# ---------- solar ----------

def potencia_solar_wp(kwh_ano, hsp_media, taxa_desempenho):
    """Potência de pico necessária para gerar kwh_ano (Wp).

    Fórmula do Manual de Engenharia FV do CEPEL/CRESESB (eq. 6.28):
    P = (E / TD) / HSP, com E em Wh/dia (média anual) e HSP em horas/dia.
    """
    if hsp_media <= 0 or not 0 < taxa_desempenho <= 1:
        raise ValueError("HSP positiva e TD entre 0 e 1")
    energia_wh_dia = kwh_ano * 1000 / 365
    return energia_wh_dia / taxa_desempenho / hsp_media


def geracao_mensal_kwh(potencia_wp, irradiacao, taxa_desempenho):
    """Geração estimada mês a mês (kWh) para a potência dada."""
    return [
        {"mes": m["mes"], "kwh": potencia_wp * m["hsp"] * m["dias"] * taxa_desempenho / 1000}
        for m in irradiacao
    ]


def valor_kwh_compensado(tarifa, tusd_r_kwh, percentual_fio_b, regra_antiga=False):
    """Quanto 1 kWh gerado e compensado deixa de ser pago (R$/kWh).

    Sistemas novos em 2026 (art. 27 da Lei 14.300): 60% do Fio B continua sendo
    cobrado sobre a energia compensada. A tabela da Enel não separa o Fio B, então:
    - pior caso: Fio B igual à TUSD inteira (menor valor compensado);
    - melhor caso (regra_antiga=True): compensa a tarifa inteira, como na regra
      antiga do art. 26. O valor real fica entre os dois.
    """
    if regra_antiga:
        return tarifa
    return tarifa - percentual_fio_b * tusd_r_kwh


def payback_anos(investimento, economia_anual):
    """Retorno simples do investimento, em anos (sem juros nem reajuste)."""
    if economia_anual <= 0:
        return float("inf")
    return investimento / economia_anual


# ---------- emissões ----------

def emissao_kg(kwh, fator_tco2_mwh):
    """Emissão de CO2 (kg) da energia tirada da rede. tCO2/MWh = kgCO2/kWh."""
    return kwh * fator_tco2_mwh
