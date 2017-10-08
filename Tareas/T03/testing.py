import unittest
import consultas
import fenotipo


class TestExcepciones(unittest.TestCase):
    def setUp(self):
        self.archivo_genomas1 = open("testing/genomas_error.txt", "r",
                                     encoding="utf-8")
        # cambiamos la base de datos
        consultas.personas = consultas.abrir_genomas(self.archivo_genomas1)
        fenotipo.personas = consultas.personas

    def test_not_acceptable(self):
        respuesta = consultas.valor_característica("CGA", "Nicolás Balbontin")
        self.assertRaises(consultas.NotAcceptable,
                          consultas.determinar_notacceptable, respuesta)

    def test_not_found(self):
        # pondremos un nombre que no esta en la base de datos
        self.assertRaises(consultas.NotFound, consultas.ascendencia,
                          "Max Santamaria")
        self.assertRaises(consultas.NotFound, consultas.pariente_de,
                          "3", "Stephanie Chau")

    def test_bad_request(self):
        # probamos la consulta hermano de
        consulta_deseada = filter(lambda x: x.__name__ == "hermano_de",
                                  consultas.lista_consultas)
        self.assertRaises(consultas.BadRequest, consultas.control_badrequest,
                          consulta_deseada, "")

    def test_genome_error(self):
        # Sterling Archer tiene un '@' en sus genes GTA
        self.assertRaises(consultas.GenomeError,
                          consultas.valor_característica, "GTA",
                          "Sterling Archer")
        self.assertRaises(consultas.GenomeError,
                          consultas.gemelo_genético, "Stephanie Chau")

    def tearDown(self):
        self.archivo_genomas1.close()


class TestConsultas(unittest.TestCase):
    def setUp(self):
        self.archivo_genomas2 = open("testing/genomas_correcto.txt", "r",
                                     encoding="utf-8")
        # cambiamos la base de datos
        consultas.personas = consultas.abrir_genomas(self.archivo_genomas2)
        fenotipo.personas = consultas.personas

    def test_pariente_de(self):
        self.assertEqual(consultas.pariente_de("2", "Sterling Archer"),
                         tuple(["fringles inthestreet"]))

    def test_ascendencia(self):
        self.assertEqual(consultas.ascendencia("Nicolás Balbontin"),
                         ["albina"])

    def test_indice_tamaño(self):
        self.assertEqual(consultas.índice_de_tamaño("Stephanie Chau"),
                         0.5855400437691198)

    def test_gemelo(self):
        self.assertEqual(consultas.gemelo_genético("Felipe Dominguez"),
                         "Nicolás Balbontin")

    def test_valor_caracteristica(self):
        self.assertEqual(consultas.gemelo_genético("Felipe Dominguez"),
                         "Nicolás Balbontin")
        self.assertEqual(consultas.valor_característica("GTA",
                                                        "Sterling Archer"),
                         "aguileña")
        self.assertIn(consultas.valor_característica("TGG",
                                                     "Sterling Archer"),
                      ["atleta", "dieta", "guaton"])

    def test_min(self):
        self.assertEqual(consultas.min2("CTC"), 39.6)
        self.assertEqual(consultas.min2("GTC"), "verdes")

    def test_max(self):
        self.assertEqual(consultas.max2("GGA"), "negro")

    def test_prom(self):
        self.assertEqual(consultas.prom("AAG"), 1.6475000000000002)

    def tearDown(self):
        self.archivo_genomas2.close()
