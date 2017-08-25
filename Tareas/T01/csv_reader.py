def read(csv_file):  # csv_file as string
    with open(csv_file, "r", encoding='utf-8') as file:
        primera_linea = file.readline()
        header = []
        type = False
        columna = ""
        for letra in primera_linea:
            if letra == ":":
                type = True
                header.append(columna)
            if letra == ";":
                type = False
                columna = ""
            elif type == False:
                columna += letra

        lista_diccionarios = []
        for line in file:
            diccionario = {}
            line = line.strip()
            lista_linea = line.split(";")
            contador = 0
            for contador in range(0, len(lista_linea)):
                diccionario.update({header[contador] : lista_linea[contador]})
            lista_diccionarios.append(diccionario)
        #for dicc in lista_diccionarios:
            #print(dicc)
        if csv_file == "users.csv":
            for user in lista_diccionarios:
                user["orders"] = user["orders"].split(":")
        return lista_diccionarios

def write_ordenado(lista_diccionarios):
    lista_diccionarios = sorted(lista_diccionarios, key=lambda elem: int(elem["order_id"]))
    with open("orders_ordenadas.csv", "w") as data:
        data.write("order_id: int;ticker: string;amount: float;price: float;type: string;date_created: string"
                   ";date_match: string\n")
        for diccionario in lista_diccionarios:
            data.write(diccionario["order_id"] + ";" + diccionario["ticker"] + ";" + diccionario["amount"] +  ";" +
                       diccionario["price"] + ";" +
                       diccionario["type"] + ";" + diccionario["date_created"] + ";" + diccionario["date_match"] + "\n")
    return lista_diccionarios

def write_ordenado_users(lista_diccionarios):
    with open("users_ordenados.csv", "w") as data:
        data.write("username: string;name: string;lastname: string;birthday: string;orders: list\n")
        for diccionario in  lista_diccionarios:
            if "birthdate" in diccionario:
                cumpleaños = "birthdate"  # error en csv
            else:
                cumpleaños = "birthday"
            orders = diccionario["orders"]
            orders = ":".join(orders)
            escribir = (diccionario["username"], diccionario["name"], diccionario ["lastname"],
                       diccionario[cumpleaños], orders + "\n")
            escribir = ";".join(escribir)
            data.write(escribir)



lista = read("orders.csv")
#print(len(lista))
contador = 0
write_ordenado(lista)


