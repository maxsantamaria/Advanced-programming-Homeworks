import re
import requests
from collections import namedtuple
import json


persona = namedtuple("Persona", ["url", "descripcion", "genero",
                                 "color_de_pelo", "lentes", "sonrisa",
                                 "edad"])


with open('faces.txt', 'r') as file:
    new_lines = []
    #personas = []
    for line in file:
        new_line = re.sub("\$(\d)+", " ", line)
        new_line = re.sub("\$[zA-zZ]{2}", "", new_line)
        #print(new_line)
        url, descripcion = new_line.split(";")
        #personas.append(persona(url, descripcion))
        new_lines.append(new_line)


with open('faces_clean.txt', 'w') as file:
    for line in new_lines:
        file.write(line)


if __name__ == "__main__":
    url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=gender,hair,smile,glasses,age"
    header =  {"Content-Type": "application/json",
               "Ocp-Apim-Subscription-Key": "5c949f29243e4e51bbcf3e2a1c3c4405"}
    personas = []
    for line in new_lines:
        url_user, mensaje = line.split(";")
        data = {"url": url_user}
        data = json.dumps(data)
        diccionario = requests.post(url, data, headers=header).json()[0]
        genero = diccionario["faceAttributes"]["gender"]
        # print(diccionario["faceAttributes"])
        pelo = diccionario["faceAttributes"]["hair"]["hairColor"][0]["color"]
        if diccionario["faceAttributes"]["glasses"] == "NoGlasses":
            lentes = False
        else:
            lentes = True
        if diccionario["faceAttributes"]["smile"] >= 0.5:
            sonrisa = True
        else:
            sonrisa = False
        age = diccionario["faceAttributes"]["age"]

        #genero = diccionario["gender"]
        #pelo = diccionario["hairColor"]
        personas.append(persona(url_user, mensaje, genero,
                                pelo, lentes, sonrisa, age))
    print(personas)

    print("¿Qué género estás buscando? (female/male)")
    genero = input(" ")
    encontradas = []
    for persona in personas:
        if persona.genero == genero:
            encontradas.append(persona)
    print("¿Qué color de pelo estás buscando? (brown/blond/black/gray/other)")
    color_de_pelo = input(" ")
    for persona in encontradas:
        if persona.color_de_pelo != color_de_pelo:
            encontradas.remove(persona)
    print("¿Quieres que tenga lentes? (si/no)")
    lentes = input(" ")
    for persona in encontradas:
        if lentes == "si" and not persona.lentes:
            encontradas.remove(persona)
        elif lentes == "no" and persona.lentes:
            encontradas.remove(persona)
    print("¿Te importa la sonrisa? (si/no)")
    sonrisa = input(" ")
    for persona in encontradas:
        if sonrisa == "si" and not persona.sonrisa:
            encontradas.remove(persona)
        elif sonrisa == "no" and persona.sonrisa:
            encontradas.remove(persona)
    print("¿Qué edad? (female/male)")
    edad = input(" ")
    # se dara un rango de 10 años
    for persona in encontradas:
        if persona.edad >= int(edad) - 5 and persona.edad <= int(edad) + 5:
            pass
        else:
            encontradas.remove(persona)

    for persona in encontradas:
        print("Encontramos a la siguiente persona:")
        print("- Genero: {}".format(persona.genero))
        print("- Color de pelo: {}".format(persona.color_de_pelo))
        print("- Lentes: {}".format(persona.lentes))
        print("- Sonrisa: {}".format(persona.sonrisa))
        print("- Edad: {}".format(persona.edad))
        print(persona.descripcion)
        print(persona.url)
