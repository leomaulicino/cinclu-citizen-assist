import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.assistant_sers import responder_assistente_sers
from src.sers_engine import (
    calcular_energia_kwh,
    calcular_linha_base,
    simular_eficiencia_energetica,
    simular_solar_ongrid,
)


class TestSersEngineAndAssistant(unittest.TestCase):
    def setUp(self):
        self.base = calcular_linha_base()
        self.alt1 = simular_eficiencia_energetica(self.base)
        self.alt2 = simular_solar_ongrid(self.base)

    def test_linha_base_epe_exata(self):
        self.assertEqual(self.base["consumo_mensal_kwh"], 179.1)
        self.assertEqual(self.base["custo_mensal_brl"], 141.38)
        self.assertEqual(self.base["emissao_anual_co2_kg"], 85.97)

    def test_alternativa_1_eficiencia(self):
        self.assertEqual(self.alt1["economia_mensal_kwh"], 35.2)
        self.assertEqual(self.alt1["novo_consumo_mensal_kwh"], 143.9)
        self.assertEqual(self.alt1["capex_brl"], 80.0)
        self.assertEqual(self.alt1["payback_meses"], 2.88)
        self.assertEqual(self.alt1["co2_evitado_anual_kg"], 16.9)

    def test_alternativa_2_solar(self):
        self.assertEqual(self.alt2["geracao_mensal_kwh"], 149.85)
        self.assertEqual(self.alt2["capex_brl"], 5430.0)
        self.assertEqual(self.alt2["fatura_residual_mensal_brl"], 39.68)
        self.assertEqual(self.alt2["economia_liquida_anual_brl"], 1070.4)
        self.assertEqual(self.alt2["payback_anos"], 5.07)
        self.assertEqual(self.alt2["co2_evitado_anual_kg"], 71.93)

    def test_validacao_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            calcular_energia_kwh(-100, 5)
        with self.assertRaises(ValueError):
            calcular_energia_kwh(100, 25)
        with self.assertRaises(ValueError):
            calcular_linha_base(tarifa_brl_kwh=0)
        with self.assertRaises(ValueError):
            calcular_linha_base(tarifa_brl_kwh=-0.5)

    def test_integracao_assistente_fontes_e_limitacoes(self):
        for consulta in ["consumo", "solar", "alugado", "compare", "lgbt"]:
            resp = responder_assistente_sers(consulta, self.base, self.alt1, self.alt2)
            self.assertIn("ANEEL", resp)
            self.assertIn("estimativ", resp.lower())


if __name__ == "__main__":
    unittest.main()