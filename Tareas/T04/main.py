from simulator import *


def parsear_parametros(archivo, comparacion, repeticiones, metrica):
    with open(archivo, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        metricas_por_escenario = []
        metrica -= 1
        for row in reader:
            personas = poblar_personas()
            productos = poblar_productos()
            quickdevil = QuickDevil()
            union_vendedores_compradores(personas)
            union_vendedores_productos(personas, productos, quickdevil)
            rapidez = row["rapidez_vendedores"].split(";")
            paciencia = row["limite_paciencia"].split(";")
            personalidad_hide = row["personalidad_hide"].split(";")
            personalidad_jek = row["personalidad_jekyll"].split(";")
            dist_almuerzo = row["distribución_almuerzo"].split(";")
            dist_almuerzo[0] = float(dist_almuerzo[0])
            dist_almuerzo[1] = float(dist_almuerzo[1])

            stock = row["stock_vendedores"].split(";")
            if not comparacion:
                mercado = MercadoUC(personas=personas, quickdevil=quickdevil,
                                    dias_susto=row["días_susto"],
                                    personalidad_jekyll=personalidad_jek,
                                    lambda_carabineros=row["llamado_policial"],
                                    pconcha=row["concha_estéreo"],
                                    c_llegada=row["moda_llegada_campus"],
                                    alpha_paciencia=paciencia[0],
                                    beta_paciencia=paciencia[1],
                                    alpha=float(rapidez[0]),
                                    beta=float(rapidez[1]),
                                    lambda_traslado=row["traslado_campus"],
                                    prob_permiso=row["probabilidad_permiso"],
                                    distribucion_almuerzo=dist_almuerzo,
                                    base_mesada=row["base_mesada"],
                                    personalidad_hyde=personalidad_hide,
                                    dinero_funcionarios=row
                                    ["dinero_funcionarios"],
                                    alpha_stock=stock[0],
                                    beta_stock=stock[1])
                mercado.run()
                mercado.mostrar_estadisticas()
            else:
                print("\nAvance escenario: {}".format(row["escenario"]))
                sumatoria = 0
                for _ in range(repeticiones):
                    personas = poblar_personas()
                    productos = poblar_productos()
                    quickdevil = QuickDevil()
                    union_vendedores_compradores(personas)
                    union_vendedores_productos(personas, productos, quickdevil)
                    print("\n\tAvance replica: ", end="")
                    mercado = MercadoUC(personas=personas,
                                        quickdevil=quickdevil,
                                        dias_susto=row["días_susto"],
                                        personalidad_jekyll=personalidad_jek,
                                        lambda_carabineros=row[
                                            "llamado_policial"],
                                        pconcha=row["concha_estéreo"],
                                        c_llegada=row["moda_llegada_campus"],
                                        alpha_paciencia=paciencia[0],
                                        beta_paciencia=paciencia[1],
                                        alpha=float(rapidez[0]),
                                        beta=float(rapidez[1]),
                                        lambda_traslado=row["traslado_campus"],
                                        prob_permiso=row[
                                            "probabilidad_permiso"],
                                        distribucion_almuerzo=dist_almuerzo,
                                        base_mesada=row["base_mesada"],
                                        personalidad_hyde=personalidad_hide,
                                        dinero_funcionarios=row
                                        ["dinero_funcionarios"],
                                        alpha_stock=stock[0],
                                        beta_stock=stock[1])
                    mercado.run()
                    # mercado.mostrar_estadisticas()
                    sumatoria += mercado.estadisticas[metrica]
                metricas_por_escenario.append(sumatoria)
        if comparacion:
            relacion = list(enumerate(metricas_por_escenario))
            ordenado = sorted(relacion, key=lambda x: x[1], reverse=True)
            for lugar in ordenado:
                print("Escenario {} con métrica {}".format(lugar[0], lugar[1]))


def interaccion():
    print("Bienvenido al Simulador de almuerzos de la PUC")
    print("Ingresa el número de la opción y ENTER:"
          "\n\t 1- Obtener estadísticas para un escenarios particular"
          "\n\t 2- Comparar varios escenarios de acuerdo a una medida"
          " de desempeño ")
    eleccion = "a"
    while eleccion not in ("1", "2"):
        eleccion = input("")
        if eleccion == "1":
            parsear_parametros("parametros_iniciales.csv", False, 1, 0)
        elif eleccion == "2":
            print("Metricas:")
            print("1- Cantidad promedio de dinero confiscado a los "
                  "vendedores debido a llegada de carabineros.")
            print("2- Cantidad minima, maxima y promedio por productos "
                  "vendidos durante un dia.")
            print("3- Cantidad maxima de productos vendidos durante un dia.")
            print("4- Cantidad promedio de productos vendidos durante un dia")
            print("5- Cantidad de confiscaciones que realizo Jekyll.")
            print("6- Cantidad de confiscaciones que realizo Hyde.")

            print("7- Numero de llamadas que realizo Quick Devil a los "
                  "Carabineros.")
            print("8- Numero de veces que se realizo la Concha Estereo.")
            print("9- Numero de veces donde hubo Temperaturas extremas.")
            print("10- Numero de veces donde hubo una Lluvia de hamburguesas.")
            print("11- Cantidad promedio de personas que almorzo entre las "
                  "12:00-12:59")
            print("12- Cantidad promedio de personas que almorzo entre las "
                  "13:00-13:59")
            print("13- Cantidad promedio de personas que almorzo entre las "
                  "14:00-14:59")
            print("14- Cantidad de alumnos que no almorzaron por mes.")
            print("15- Calidad promedio de productos de todos los vendedores"
                  " por escenario.")
            print("16- Cantidad de MiembrosUC que se intoxicaron.")
            print("17- Cantidad de Productos que se descompone.")
            print("18- Cantidad promedio de miembros de la PUC que abandonaron"
                  " una cola de espera por dia.")
            print("19. Cantidad promedio de vendedores por dia que se quedaron"
                  " sin stock.")
            print("20- Cantidad de veces que se engaño a los carabineros de "
                  "personalidad Dr. Jekyll")
            print("21- Cantidad de veces que se engaño a los carabineros de "
                  "personalidad Mr. Hyde")
            metrica = "mal"
            while not isinstance(metrica, int) or metrica > 21:
                metrica = int(input("Ingrese el número de la métrica a"
                                    " considerar: "))
            print("Ingrese la cantidad de repeticiones por escenario "
                  "(considere que hay una demora de aprox 35 segundos por "
                  "réplica)")
            repeticiones = 0
            while not isinstance(repeticiones, int) or repeticiones <= 0:
                repeticiones = int(input("Numero de repeticiones: "))
            parsear_parametros("escenarios.csv", True, repeticiones,
                               int(metrica))


if __name__ == "__main__":
    interaccion()
