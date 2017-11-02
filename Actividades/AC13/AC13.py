import os
import json
import pickle


class Cliente:
    def __init__(self, rut, nombre, apellido, fecha_nacimiento, numero_cuenta,
                 tipo_cuenta, clave, balance):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.clave = clave
        self.balance = balance

    def __getstate__(self):
        dict_normal = self.__dict__.copy()
        new_dict = {}
        for key, value in dict_normal.items():
            if isinstance(key, str):
                key = cifrado_alfabeto_desplazado(key)
            if isinstance(value, str):
                value = cifrado_alfabeto_desplazado(value)
            new_dict.update({key: value})
        return new_dict

    def __setstate__(self, state):
        old_dict = {}
        for key, value in state.items():
            if isinstance(key, str):
                key = decifrado_alfabeo_desplazado(key)
            if isinstance(value, str):
                value = decifrado_alfabeo_desplazado(value)
            old_dict.update({key: value})
        self.__dict__ = old_dict

    def __str__(self):
        return self.rut + " " + self.nombre + " " + self.apellido


class ClienteEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Cliente):
            return {'Rut': obj.rut,
                    'Nombre': obj.nombre,
                    'Apellido': obj.apellido,
                    'Fecha de Nacimiento': obj.fecha_nacimiento,
                    'Numero de cuenta': obj.numero_cuenta,
                    'Tipo de cuenta': obj.tipo_cuenta,
                    'Clave': obj.clave,
                    'Balance': obj.balance}
        return super().default(obj)


def obtener_ruts():
    with open("ruts_para_leer.txt", "r") as file:
        ruts = [rut.strip() for rut in file]
        return ruts


def buscar_ruts():
    paths = []
    base = 'base_de_datos_banco'
    folders = os.listdir(base)
    for folder in folders:
        for subfolder in os.listdir(os.path.join(base, folder)):
            for archivo in os.listdir(os.path.join(base, folder, subfolder)):
                if archivo.split('.')[0] in ruts:
                    paths.append(os.path.join(base, folder, subfolder,
                                              archivo))
    return paths


def generar_clientes_afectados(paths):
    afectados = []
    for path in paths:
        with open(path, 'r') as data:
            afectado = json.load(data,
                                 object_hook=lambda dict_obj:
                                 Cliente(**decoder(dict_obj)))
            afectados.append(afectado)

    return afectados


def respaldar_datos(clientes):
    if not os.path.exists('bd_json'):
        os.makedirs('bd_json')
    for persona in clientes:
        path = os.path.join("bd_json", persona.rut + '.json')
        with open(path, "w", encoding='utf-8') as writer:
            json_string = json.dumps(persona, cls=ClienteEncoder)
            writer.write(json_string)


def cifrado_alfabeto_desplazado(string):
    new_string = ""
    for letra in string:
        numero_cambiado = ord(letra) + 22
        letra_cambiada = chr(numero_cambiado)
        new_string += letra_cambiada
    return new_string


def decifrado_alfabeo_desplazado(string):
    old_string = ""
    for letra in string:
        numero_cambiado = ord(letra) - 22
        letra_vieja = chr(numero_cambiado)
        old_string += letra_vieja
    return old_string


def decoder(dict_obj):
    dicc = {}
    dicc.update({"rut": dict_obj["rut"],
                 "nombre": dict_obj["nombre"],
                 "apellido": dict_obj["apellido"],
                 "fecha_nacimiento": dict_obj["fecha_nacimiento"],
                 "numero_cuenta": dict_obj["numero_cuenta"],
                 "tipo_cuenta": dict_obj["tipo_cuenta"],
                 "clave": dict_obj["clave"],
                 "balance": dict_obj["balance"]})
    return dicc


def guardar_encriptados(afectados):
    if not os.path.exists('bd_segura'):
        os.makedirs('bd_segura')
    for persona in afectados:
        path = os.path.join('bd_segura', persona.rut)
        with open(path, 'wb') as file:
            pickle.dump(persona, file)


def abrir_encriptados():
    personas = []
    for archivo in os.listdir('bd_segura'):
        with open(os.path.join('bd_segura', archivo), 'rb') as file:
            persona = pickle.load(file)
            personas.append(persona)
    return personas


if __name__ == '__main__':
    ruts = obtener_ruts()
    paths = buscar_ruts()
    afectados = generar_clientes_afectados(paths)
    respaldar_datos(afectados)
    guardar_encriptados(afectados)
    desencriptados = abrir_encriptados()
