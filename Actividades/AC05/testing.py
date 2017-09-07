import unittest


class Chequear(unittest.TestCase):

    def test_digito_rut(self):
        self.assertFalse(check_rut(rut))

    def test_formato_rut(self):
        self.assertRaises(Exception, check_rut(rut_incorrecto))
        self.assertTrue(check_rut(rut_correcto))

    def test_archivo_salida(self):
        pass

    def test_info_personas(self):
        pass

    