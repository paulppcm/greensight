"""Pruebas de la lógica de control sin acceder al hardware."""

import unittest

import config
import control


class ControlGreenSightTest(unittest.TestCase):
    def test_luz_baja_enciende_led(self):
        estado = control.controlar_luz(config.LUZ_BAJA)
        self.assertTrue(estado["led"])
        self.assertEqual(estado["estado_luz"], "BAJA")

    def test_luz_normal_apaga_led(self):
        estado = control.controlar_luz(config.LUZ_BAJA + 1)
        self.assertFalse(estado["led"])
        self.assertEqual(estado["estado_luz"], "NORMAL")

    def test_temperatura_alta_enciende_ventilador(self):
        estado = control.controlar_temperatura(config.TEMPERATURA_MAX)
        self.assertTrue(estado["ventilador"])
        self.assertEqual(estado["estado_temperatura"], "ALTA")

    def test_temperatura_sin_dato_mantiene_ventilador_apagado(self):
        estado = control.controlar_temperatura(None)
        self.assertFalse(estado["ventilador"])
        self.assertEqual(estado["estado_temperatura"], "SIN DATO")

    def test_suelo_seco_enciende_bomba(self):
        estado = control.controlar_humedad_suelo(config.HUMEDAD_SUELO_MIN)
        self.assertTrue(estado["bomba"])
        self.assertEqual(estado["estado_suelo"], "SECO")

    def test_suelo_humedo_apaga_bomba(self):
        estado = control.controlar_humedad_suelo(config.HUMEDAD_SUELO_MIN + 1)
        self.assertFalse(estado["bomba"])
        self.assertEqual(estado["estado_suelo"], "NORMAL")

    def test_bomba_funciona_si_no_se_necesita_ventilador(self):
        datos = {
            "temperatura": config.TEMPERATURA_MAX - 1,
            "humedad_aire": 50,
            "valor_suelo": 700,
            "humedad_suelo": config.HUMEDAD_SUELO_MIN - 1,
            "luz": config.LUZ_BAJA + 1,
        }

        estado = control.aplicar_control(datos)

        self.assertTrue(estado["bomba"])
        self.assertFalse(estado["ventilador"])
        self.assertIsNone(estado["restriccion_energia"])

    def test_bomba_tiene_prioridad_si_ambos_son_necesarios(self):
        datos = {
            "temperatura": config.TEMPERATURA_MAX + 1,
            "humedad_aire": 50,
            "valor_suelo": 700,
            "humedad_suelo": config.HUMEDAD_SUELO_MIN - 1,
            "luz": config.LUZ_MUY_BAJA,
        }

        estado = control.aplicar_control(datos)

        self.assertTrue(estado["led"])
        self.assertFalse(estado["ventilador"])
        self.assertTrue(estado["bomba"])
        self.assertEqual(
            estado["restriccion_energia"],
            "BOMBA_PRIORIDAD",
        )


if __name__ == "__main__":
    unittest.main()
