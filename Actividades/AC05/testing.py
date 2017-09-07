import unittest
import form

class Chequear(unittest.TestCase):
    def setUp(self):
        self.form = form.FormRegister()

    def test_digito_rut(self):
        prueba = self.form.check_rut("19246885-A")
        self.assertFalse(prueba)

    def test_formato_rut(self):
        self.assertRaises(TypeError, self.form.check_rut,("19.239.399-2"))
        self.assertTrue(self.form.check_rut,("19246885-6"))  # rut correcto


    def test_archivo_salida(self):
        with open("result.txt", "r") as file:
            lineas = file.readlines()
            self.assertIn("Student", lineas[0])
            self.assertIn("Gender", lineas[1])
            self.assertIn("Comment", lineas[2])
            self.assertIn("#####", lineas[3])

    def test_info_personas(self):
        name = "Hugo Navarrete"
        gender = "Error 404-Not found"
        comment = "Dicen que es mejor que avanzada o.o"
        self.form.register_people_info(name, gender, comment)
        self.assertIn(name, self.form.register_list[-1])
        self.assertIn(gender, self.form.register_list[-1])
        self.assertIn(comment, self.form.register_list[-1])

    def tearDown(self):
        #file.close()
        pass  # se podria usar para cerrar el archivo pero al usar contexto
              # con with, no es necesario cerrarlo
if __name__ == "__main__":
     unittest.main()