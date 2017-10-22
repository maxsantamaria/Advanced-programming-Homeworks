from entidades import Alumno, Funcionario, Vendedor, Carabinero, Producto
import csv


def hola():
    pass

#def parsear_personas():
with open("personas.csv", newline="", encoding="utf-8") as csvfile:
    personas_reader = csv.reader(csvfile, delimiter=";")
    reader = csv.DictReader(csvfile, delimiter=";", skipinitialspace=True)
    personas = []
    #header = next(csvfile)
    for row in reader:
        if row["Entidad"] == "Alumno":
            new_person = Alumno(row["Nombre"].strip(),
                                row["Apellido"].strip(),
                                row["Edad"].strip())
            lista = row["Vendedores de Preferencia"].strip().split(" - ")
            new_person.preferencias = lista
        elif row["Entidad"] == "Funcionario":
            new_person = Funcionario(row["Nombre"],
                                     row["Apellido"],
                                     row["Edad"])
            lista = row["Vendedores de Preferencia"].strip().split(" - ")
            new_person.preferencias = lista
        elif row["Entidad"] == "Vendedor":
            new_person = Vendedor(row["Nombre"],
                                  row["Apellido"],
                                  row["Edad"],
                                  row["Tipo Comida"])
        elif row["Entidad"] == "Carabinero":
            new_person = Carabinero(row["Nombre"],
                                    row["Apellido"],
                                    row["Edad"],
                                    row["Personalidad"])
        personas.append(new_person)
#        return personas

def parsear_parametros():
    with open("parametros_iniciales.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            print(row["personalidad_jekyll"], row["personalidad_hide"])
            pass
        #print(row)


#personas = parsear_personas()
parsear_parametros()
