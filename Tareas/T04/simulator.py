from entidades import *


class MercadoUC:
    def __init__(self, c_llegada, personas, alpha, beta, lambda_traslado, alpha_stock, beta_stock, base_mesada, alpha_paciencia, beta_paciencia, prob_permiso):
        self.personas = personas
        self.miembrosuc = []
        self.vendedores = []
        self.carabineros = []
        self.tiempo_actual = 0  # 11:00, quizas conviene cambiarlo a 8:00
        self.tiempo_maximo = 4 * 60  # 15:00
        self.tiempo_llegada_carabinero = 120  # 13:00 va a ir aumentando a medida que se cambia de puesto
        self.lambda_traslado = lambda_traslado
        for persona in self.personas:
            if isinstance(persona, MiembroUC):
                persona.generar_tiempo_llegada_universidad(c_llegada)
                if isinstance(persona, Alumno):
                    persona.generar_mesada(base_mesada)
                    persona.generar_tiempo_paciencia(alpha_paciencia,
                                                     beta_paciencia)
                persona.generar_pesos_diarios()
                self.miembrosuc.append(persona)

            elif isinstance(persona, Vendedor):
                persona.generar_rapidez_atencion(alpha, beta)
                persona.generar_stock(alpha_stock, beta_stock)
                persona.generar_permisos(prob_permiso)
                self.vendedores.append(persona)

            elif isinstance(persona, Carabinero):
                self.carabineros.append(persona)
        self.generar_carabinero()  # poner esto despues en la funcion de que Devil llame a los carab

    def comprobar_cambio_de_cola(self, persona):  # True si se cambia, False si no
        vendedor = next((ven for ven in self.vendedores if persona in
                         ven.cola))
        if vendedor.fiscalizando:
            return True
        if vendedor.stock < vendedor.cola.index(persona) + 1:
            return True
        precio_minimo = min([int(producto.precio) for producto in
                             vendedor.productos])
        if precio_minimo > persona.pesos_diarios:
            return True
        if persona.tiempo_paciencia < (vendedor.cola.index(persona)) * vendedor.rapidez_atencion:
            print("SE AGOTO LA PACIENCIA DE", persona, "VENDEDOR", vendedor, vendedor.cola)
            return True
        # Falta limite de paciencia
        return False

    def actualizar_colas(self, cola_actual):
        # se usa para actualizar los cambios de cola cuando llega
        # un funcionario
        cola = cola_actual()
        compradores_en_cola = [compr for compr in cola
                               if isinstance(compr, Alumno)]
        for persona in compradores_en_cola:

            while self.comprobar_cambio_de_cola(persona):
                if persona.cambiar_de_cola1() is not None:
                    print("La persona", persona,
                          "no tiene más opciones que ir a Quick Devil")
                    persona.generar_tiempo_decidir_comprar_snack(self.tiempo_actual)
                    persona.generar_tiempo_llegada_a_puestos(
                        self.lambda_traslado)
                    break
                print("2 :", persona, "se cambió de cola")

    def generar_carabinero(self):
        self.carabinero = choice(self.carabineros)

    @property
    def proxima_persona_llega_universidad(self):
        no_han_llegado = [persona for persona in self.miembrosuc if
                          persona.tiempo_llegada_universidad >
                          self.tiempo_actual]
        if len(no_han_llegado) > 0:
            persona = sorted(no_han_llegado,
                             key=lambda x: x.tiempo_llegada_universidad)[0]
            return (persona, persona.tiempo_llegada_universidad)
        return (None, float("Inf"))

    @property
    def proxima_persona_es_atendida(self):
        vendedores_con_cola = [vendedor for vendedor in self.vendedores
                               if len(vendedor.cola) > 0]
        if len(vendedores_con_cola) > 0:
            vendedor = sorted(vendedores_con_cola, key=lambda
                              x: x.tiempo_atencion_primer_cliente)[0]
            return (vendedor, vendedor.tiempo_atencion_primer_cliente)
        return (None, float("Inf"))

    @property
    def proxima_persona_llega_a_puestos(self):
        miembrosuc_disponibles = [persona for persona in self.miembrosuc
                                  if persona._tiempo_llegada_a_puestos
                                  is not None]
        if len(miembrosuc_disponibles) > 0:
            comprador = sorted(miembrosuc_disponibles, key=lambda x:
                               x._tiempo_llegada_a_puestos)[0]
            tiempo_llegada = comprador._tiempo_llegada_a_puestos
            return (comprador, tiempo_llegada)
        return (None, float("Inf"))

    @property
    def proximo_carabinero_llega(self):
        if self.tiempo_actual < 160:  # despues se arreglara con datetime
            # if hour < 13:40
            return (self.carabinero, self.tiempo_llegada_carabinero)
        return (None, float("Inf"))

    @property
    def proximo_evento(self):
        tiempos = [self.proxima_persona_llega_universidad[1],
                   self.proxima_persona_es_atendida[1],
                   self.proxima_persona_llega_a_puestos[1],
                   self.proximo_carabinero_llega[1]]

        tiempo_prox_evento = min(tiempos)

        eventos = ["llegada_persona_universidad",
                   "persona_compra_snack",
                   "persona_llega_a_puestos",
                   "carabinero_llega"]

        return eventos[tiempos.index(tiempo_prox_evento)]

    def llegada_universidad(self):
        persona, tiempo = self.proxima_persona_llega_universidad
        self.tiempo_actual = tiempo
        print("1 : Ha llegado", persona,
              "a la Universidad en la hora", self.tiempo_actual)
        compra_snack = choice([0, 1])
        if compra_snack == 1 and len(persona.colas_snack) > 0:
            print(persona, "quiere comprar snack al llegar")
            #self.proxima_persona_compra_snack = self.tiempo_actual
            persona.ingresar_a_cola_snack(tiempo)
            while self.comprobar_cambio_de_cola(persona):
                #persona.numero_de_rechazos += 1
                if persona.cambiar_de_cola1() is not None:
                    print("La persona", persona,
                          "no tiene más opciones que ir a Quick Devil")
                    persona.generar_tiempo_decidir_comprar_snack(tiempo)
                    persona.generar_tiempo_llegada_a_puestos(
                        self.lambda_traslado)
                    break
                print("2 :", persona, "se cambió de cola")
            if isinstance(persona, Funcionario):
                self.actualizar_colas(persona.
                                      colas_snack[persona.ind_cola_actual])
                persona.colas_usadas = []
        else:
            persona.generar_tiempo_decidir_comprar_snack(tiempo)
            persona.generar_tiempo_llegada_a_puestos(self.lambda_traslado)

    def persona_compra_snack(self):
        vendedor, tiempo = self.proxima_persona_es_atendida
        self.tiempo_actual = tiempo
        comprador = vendedor.cola.popleft()
        for producto in vendedor.productos:
            producto.actualizar_putrefaccion(tiempo)
            producto.actualizar_calidad()
        if isinstance(comprador, Alumno):  # compra el mas barato
            producto_comprado = vendedor.productos[0]
            comprador.pesos_diarios -= int(producto_comprado.precio)
        elif isinstance(comprador, Funcionario):  # mejor calidad
            opciones = [prod for prod in vendedor.productos
                        if prod.precio <= comprador.pesos_diarios]
            producto_comprado = sorted(opciones,
                                       key=lambda x: x.calidad,
                                       reverse=True)[0]

            comprador.pesos_diarios -= int(producto_comprado.precio)
        vendedor.stock -= 1
        #vendedor.unidades_vendidas += 1
        # ahora se empieza a atender al siguiente
        if len(vendedor.cola) > 0:
            vendedor.cola[0].tiempo_comienzo_atencion = tiempo
        print("4 :", comprador, "le ha comprado un snack a",
              vendedor.nombrecompleto, "en la hora", self.tiempo_actual)
        print(comprador.ind_cola_actual, comprador.preferencias_snack)
        if producto_comprado.calidad < 0.2:
            prob = random()
            if prob < 0.35:
                print("5 :", comprador, "se ha enfermado. Nunca más le"
                                        "comprará a", vendedor)
                print(comprador.ind_cola_actual, len(comprador.colas_snack))
                comprador.colas_snack.pop(comprador.ind_cola_actual)
                comprador.preferencias_snack.remove(vendedor.nombre)  # BORRAR DESPUES

        comprador.generar_tiempo_decidir_comprar_snack(tiempo)
        comprador.generar_tiempo_llegada_a_puestos(self.lambda_traslado)

    def persona_llega_a_puestos(self):
        comprador, tiempo = self.proxima_persona_llega_a_puestos
        comprador.ind_cola_actual = 0
        self.tiempo_actual = tiempo
        if len(comprador.colas_snack) > 0:
            comprador.ingresar_a_cola_snack(tiempo)
            print("3 :", comprador,
                  "llegó a los puestos de comida y quiere comprar un snack en",
                  tiempo)
            while self.comprobar_cambio_de_cola(comprador):
                #comprador.numero_de_rechazos += 1
                if comprador.cambiar_de_cola1() is not None:
                    print("La persona", comprador, "se cambia y",
                          "no tiene más opciones que ir a Quick Devil")
                    comprador.quick = True
                    break
                print("2 :", comprador.nombrecompleto, "se cambió de cola")
            if not comprador.quick and isinstance(comprador, Funcionario):  # hay que ver el efecto
                self.actualizar_colas(comprador
                                      .colas_snack[comprador.ind_cola_actual])
                comprador.colas_usadas = []
        else:
            print("La persona", comprador, "llegó a los puestos y",
                  "no tiene más opciones que ir a Quick Devil")

        comprador.quick = False
        comprador._tiempo_llegada_a_puestos = None  # se reinicia

    def carabinero_comienza_a_fiscalizar(self):
        carabinero, tiempo = self.proximo_carabinero_llega
        self.tiempo_actual = tiempo
        if carabinero.vendedor_actual is not None:  # el anterior
            carabinero.vendedor_actual.fiscalizando = False
            carabinero.fiscalizados.append(carabinero.vendedor_actual)
            print("Se terminó de fiscalizar a", carabinero.vendedor_actual)
        if len(self.vendedores) > len(carabinero.fiscalizados):
            vendedor = choice(list(set(self.vendedores) -
                                     set(carabinero.fiscalizados)))
            carabinero.fiscalizar(vendedor, tiempo)
            print("-" * 30, carabinero, "está fiscalizando a", vendedor)
            for comp in vendedor.cola:
                print(comp)
            if len(vendedor.cola) > 0:  # si hay cola
                vendedor.cola[0].tiempo_comienzo_atencion = tiempo + 40/len(self.vendedores)
        self.tiempo_llegada_carabinero += 40/len(self.vendedores)  # siguiente fiscalizacion

    def run(self):
        for persona in self.miembrosuc:
            print(persona, len(persona.colas_snack))
        while self.tiempo_actual < self.tiempo_maximo:
            evento = self.proximo_evento
            if evento == "llegada_persona_universidad":
                self.llegada_universidad()
            elif evento == "persona_compra_snack":
                self.persona_compra_snack()
            elif evento == "persona_llega_a_puestos":
                self.persona_llega_a_puestos()
            elif evento == "carabinero_llega":
                self.carabinero_comienza_a_fiscalizar()

        for persona in self.vendedores:
            print(persona.stock)

uc = MercadoUC(30, personas, 1, 3, 0.33, 80, 150, 3000, 20, 35, 0.5)
uc.run()


