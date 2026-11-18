"""Testes dos cálculos de energia. Execute com: python -m unittest -v"""

import csv
import os
import tempfile
import unittest

import analise
import energia as e

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestFormulas(unittest.TestCase):
    def test_consumo_por_km(self):
        self.assertAlmostEqual(e.consumo_por_km(630, 80), 7.875)
        self.assertAlmostEqual(e.consumo_por_km(221, 25), 8.84)

    def test_consumo_por_km_invalido(self):
        with self.assertRaises(ValueError):
            e.consumo_por_km(0, 80)
        with self.assertRaises(ValueError):
            e.consumo_por_km(630, 0)

    def test_tomada_fornece_mais_que_a_bateria_guarda(self):
        # 630 Wh com eficiência de 85% = 741,2 Wh tirados da tomada
        self.assertAlmostEqual(e.energia_da_tomada_kwh(630, 0.85), 0.74118, places=4)
        self.assertGreater(e.energia_da_tomada_kwh(630, 0.85), 0.630)

    def test_eficiencia_fora_da_faixa(self):
        for valor in (0, -0.1, 1.2):
            with self.assertRaises(ValueError):
                e.energia_da_tomada_kwh(630, valor)

    def test_tarifa_convencional_b1(self):
        # (472,42 + 316,96) R$/MWh = 0,78938 R$/kWh
        self.assertAlmostEqual(e.tarifa_r_kwh(472.42, 316.96), 0.78938)

    def test_bandeira_soma_por_kwh(self):
        self.assertAlmostEqual(e.custo(10, 0.78938, 0.07877), 8.6815)

    def test_potencia_solar_formula_cresesb(self):
        # 365 kWh/ano = 1000 Wh/dia; (1000 / 0,75) / 4,66 = 286,1 Wp
        self.assertAlmostEqual(e.potencia_solar_wp(365, 4.66, 0.75), 286.123, places=2)

    def test_geracao_anual_fecha_com_o_consumo(self):
        irradiacao = e.carregar_irradiacao()
        wp = e.potencia_solar_wp(100, 4.66, 0.75)
        total = sum(m["kwh"] for m in e.geracao_mensal_kwh(wp, irradiacao, 0.75))
        # a média mensal ponderada pelos dias é ~4,66, então a geração anual ~ 100 kWh
        self.assertAlmostEqual(total, 100, delta=1.0)

    def test_valor_compensado_entre_pior_e_melhor_caso(self):
        tarifa, tusd = 0.78938, 0.47242
        pior = e.valor_kwh_compensado(tarifa, tusd, 0.60)
        melhor = e.valor_kwh_compensado(tarifa, tusd, 0.60, regra_antiga=True)
        self.assertAlmostEqual(pior, 0.78938 - 0.6 * 0.47242)
        self.assertEqual(melhor, tarifa)
        self.assertLess(pior, melhor)

    def test_payback_sem_economia(self):
        self.assertEqual(e.payback_anos(100, 0), float("inf"))
        self.assertAlmostEqual(e.payback_anos(100, 25), 4)

    def test_emissao(self):
        # 1 kWh com 0,0461 tCO2/MWh = 0,0461 kg
        self.assertAlmostEqual(e.emissao_kg(1, 0.0461), 0.0461)


class TestDados(unittest.TestCase):
    def test_toda_premissa_tem_tipo_e_fonte_ou_justificativa(self):
        with open(os.path.join(PASTA, "dados", "premissas.csv"), encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                self.assertIn(linha["tipo"], ("dado oficial", "dado do fabricante", "dado de mercado",
                                              "referência técnica", "premissa da equipe"), linha["chave"])
                if linha["tipo"] == "premissa da equipe":
                    self.assertTrue(linha["observacao"], f"{linha['chave']} sem justificativa")
                else:
                    self.assertTrue(linha["fonte"].startswith("https://"), linha["chave"])
                float(linha["valor"])

    def test_irradiacao_doze_meses_e_media_confere(self):
        irradiacao = e.carregar_irradiacao()
        self.assertEqual(len(irradiacao), 12)
        self.assertEqual(sum(m["dias"] for m in irradiacao), 365)
        media = sum(m["hsp"] for m in irradiacao) / 12
        self.assertAlmostEqual(media, e.carregar_premissas()["irradiacao_inclinada_media"], places=2)

    def test_fator_emissao_media_anual_coerente(self):
        fatores = e.carregar_fator_emissao()
        self.assertEqual(len(fatores), 12)
        anual = e.carregar_premissas()["fator_emissao_sin_2025"]
        self.assertTrue(min(fatores) <= anual <= max(fatores))


class TestComparacao(unittest.TestCase):
    def setUp(self):
        self.p = e.carregar_premissas()
        self.comp = analise.comparar(self.p)

    def bike(self, letra):
        return [c for c in self.comp if c["veiculo"] == "Bike elétrica" and c["alternativa"].startswith(letra)]

    def test_mesma_necessidade_em_todas_as_alternativas(self):
        for veiculo in ("Bike elétrica", "Patinete elétrico"):
            kwh = {round(c["kwh_ano"], 6) for c in self.comp if c["veiculo"] == veiculo}
            self.assertEqual(len(kwh), 1, veiculo)

    def test_ordem_de_custo(self):
        a, b, c_pior, c_melhor = self.bike("A")[0], self.bike("B")[0], self.bike("C")[0], self.bike("C")[1]
        self.assertGreater(a["custo_ano_rs"], b["custo_ano_rs"])
        self.assertGreater(b["custo_ano_rs"], c_pior["custo_ano_rs"])
        self.assertAlmostEqual(c_melhor["custo_ano_rs"], 0)

    def test_solar_sem_emissao_na_operacao_e_rede_com(self):
        self.assertGreater(self.bike("A")[0]["co2_kg_ano"], 0)
        self.assertEqual(self.bike("C")[0]["co2_kg_ano"], 0)

    def test_valores_de_referencia_da_bike(self):
        a = self.bike("A")[0]
        self.assertAlmostEqual(a["kwh_ano"], 14.675, places=2)
        self.assertAlmostEqual(a["custo_ano_rs"], 11.58, places=2)

    def test_carga_completa_bike_bandeira_verde(self):
        cargas = analise.recarga_completa(self.p)
        verde = [c for c in cargas if c["veiculo"] == "Bike elétrica" and c["bandeira"] == "verde"][0]
        self.assertAlmostEqual(verde["custo_rs"], 0.585, places=3)

    def test_toda_alternativa_tem_viabilidade(self):
        for c in self.comp:
            self.assertTrue(c["viabilidade"], c["alternativa"])

    def test_csv_gravado_e_legivel(self):
        with tempfile.TemporaryDirectory() as pasta:
            original = analise.PASTA_RESULTADOS
            analise.PASTA_RESULTADOS = pasta
            try:
                caminho = analise.gravar_csv("teste", self.comp)
            finally:
                analise.PASTA_RESULTADOS = original
            with open(caminho, encoding="utf-8-sig") as arquivo:
                linhas = list(csv.DictReader(arquivo))
            self.assertEqual(len(linhas), len(self.comp))
            self.assertIn("viabilidade", linhas[0])


if __name__ == "__main__":
    unittest.main()
