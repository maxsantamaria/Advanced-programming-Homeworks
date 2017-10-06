from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
import consultas
from excepciones import *


# DECORADORES
def modificar_nombre_funcion(func):
    def _modificar_nombre_funcion(*args):
        args = list(args)
        nombre_funcion = args[1]  # el primero es self
        if nombre_funcion == "min":
            args[1] = "min2"
        elif nombre_funcion == "max":
            args[1] = "max2"
        elif nombre_funcion == "gemelo_genetico":
            args[1] = "gemelo_genético"
        elif nombre_funcion == "indice_de_tamaño":
            args[1] = "índice_de_tamaño"
        return func(*args)
    return _modificar_nombre_funcion
# Fin DECORADORES


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()

    def process_query(self, query_array):
        # Agrega en pantalla la solucion. Muestra los graficos!!
        print(query_array)
        for query in query_array:
            print(query)
            num_consulta = next(consultas.numeros)
            funcion = query[0]
            args = query[1:]
            respuesta = self.llamar_funcion(funcion, *args)
            text = ("Probando funcion\nConsulta " + str(num_consulta) +
                    "\n" + str(respuesta) + "\n")
            self.add_answer(text)


    @modificar_nombre_funcion
    def llamar_funcion(self, funcion, *args):
        consulta_deseada = filter(lambda x: x.__name__ == funcion, consultas.lista_consultas)
        try:
            funcion = control_badrequest(consulta_deseada, args)
            args = [str(arg) for arg in args]
            respuesta = funcion(*args)
            determinar_notacceptable(respuesta)
        except NotFound as err1:
            return err1
        except NotAcceptable as err2:
            return err2
        except BadRequest as err3:
            return err3
        return respuesta


    def save_file(self, query_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        print(query_array)



if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)


    sys.__excepthook__ = hook

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
