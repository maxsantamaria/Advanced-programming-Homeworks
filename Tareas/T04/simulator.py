from entidades import *
from variables import *
import sys


class MercadoUC:
    def __init__(self, c_llegada, personas, alpha, beta, lambda_traslado,
                 alpha_stock, beta_stock, base_mesada, alpha_paciencia,
                 beta_paciencia, prob_permiso, distribucion_almuerzo, pconcha,
                 lambda_carabineros, quickdevil, personalidad_jekyll,
                 personalidad_hyde, dias_susto, dinero_funcionarios):
        # parametros
        self.c_llegada = float(c_llegada)
        self.alpha_paciencia = float(alpha_paciencia)
        self.beta_paciencia = float(beta_paciencia)
        self.alpha_stock = float(alpha_stock)
        self.beta_stock = float(beta_stock)
        self.pconcha = float(pconcha)
        self.base_mesada = float(base_mesada)
        self.lambda_carabineros = float(lambda_carabineros)
        self.personalidad_jekyll = personalidad_jekyll
        self.personalidad_hyde = personalidad_hyde
        self.dias_susto = float(dias_susto)
        self.lambda_traslado = float(lambda_traslado)
        # base de datos
        self.quickdevil = quickdevil
        self.personas = personas
        self.miembrosuc = []
        self.vendedores = []
        self.carabineros = []
        self.tiempo_actual = 0  # 11:00, quizas conviene cambiarlo a 8:00
        self.fechahora = datetime(year=2017, month=3, day=1, hour=11, minute=0,
                                  second=0)
        self.tiempo_maximo = TIEMPO_MAXIMO_DIA  # 15:00
        self.tiempo_llegada_carabinero = TIEMPO_LLEGADA_CARABINEROS
        # 13:00 va a ir aumentando a medida que se cambia de puesto
        # eventos no programados
        self.frio_intenso = False
        self.calor_intenso = False
        self._proxima_temperatura_extrema = None
        self.ultima_temperatura_extrema = datetime(year=2017, month=3, day=1,
                                                   hour=11, minute=0, second=0)
        self._proxima_lluvia_de_hamburguesas = None
        self.lluvia = False
        self.dia_anterior_lluvia = False
        self.ultima_concha = self.fechahora
        self.concha = False
        self.generar_proxima_temperatura_extrema()
        self.generar_proxima_lluvia_de_hamburguesas()
        self.carabinero = None
        self.generar_llamada_carabinero()
        # estadisticas
        self.productos_vendidos_un_dia = 0
        self.productos_vendidos_cada_dia = []
        self.num_llamadas = 0
        self.num_conchas = 0
        self.num_temperaturas = 0
        self.num_lluvias = 0
        self.cantidad_almuerzos12_dias = []
        self.cantidad_almuerzos12_dia = 0
        self.cantidad_almuerzos13_dias = []
        self.cantidad_almuerzos13_dia = 0
        self.cantidad_almuerzos14_dias = []
        self.cantidad_almuerzos14_dia = 0
        self.cantidad_no_almuerzan = {"March": 0, "April": 0, "May": 0,
                                      "June": 0}  # key = mes
        self.calidades = []
        self.productos_descompuestos = 0
        self.abandonos_cola_dia = 0
        self.abandonos_cola_dias = []
        self.vendedores_sin_stock_dias = []

        for persona in self.personas:
            if isinstance(persona, MiembroUC):
                persona.generar_tiempo_llegada_universidad(self.c_llegada)
                if isinstance(persona, Alumno):
                    persona.generar_mesada(self.base_mesada)
                    persona.generar_tiempo_paciencia(self.alpha_paciencia,
                                                     self.beta_paciencia)
                    persona.generar_pesos_diarios()
                elif isinstance(persona, Funcionario):
                    persona.generar_pesos_diarios(dinero_funcionarios)
                self.miembrosuc.append(persona)

            elif isinstance(persona, Vendedor):
                persona.generar_rapidez_atencion(float(alpha), float(beta))
                persona.generar_stock(self.alpha_stock, self.beta_stock)
                persona.generar_permisos(float(prob_permiso))
                persona.generar_tiempo_instalacion()
                self.vendedores.append(persona)

            elif isinstance(persona, Carabinero):
                self.carabineros.append(persona)
        self.posibles_vendedores = self.vendedores
        for i, miembro in enumerate(self.miembrosuc):
            porcentaje2 = float(distribucion_almuerzo[0]) + \
                          float(distribucion_almuerzo[1])
            if i < len(self.miembrosuc) * distribucion_almuerzo[0]/100:
                miembro.distribucion_almuerzo = 120
                miembro.generar_tiempo_decidir_almorzar()
                miembro.generar_tiempo_llegada_a_puestos2(lambda_traslado)
            elif i >= len(self.miembrosuc) * distribucion_almuerzo[0]/100 and \
                    i < len(self.miembrosuc) * porcentaje2 / 100:
                miembro.distribucion_almuerzo = 180
                miembro.generar_tiempo_decidir_almorzar()
                miembro.generar_tiempo_llegada_a_puestos2(lambda_traslado)
            else:
                miembro.distribucion_almuerzo = 60
                miembro.generar_tiempo_decidir_almorzar()
                miembro.generar_tiempo_llegada_a_puestos2(lambda_traslado)

    def comprobar_cambio_de_cola(self, persona):
        """
        Comprueba si una persona puede cambiarse a la siguiente cola o no,
        dependiendo de las características del vendedor y la cola
        (tiempo_paciencia, stock, precio, fiscalizando, ausente)
        :param persona: Persona
        :return: Booleano
        """
        vendedor = next((ven for ven in self.vendedores if persona in
                         ven.cola))
        if vendedor.fiscalizando or not vendedor.instalado or vendedor.ausente:
            # print("Aun no se instala", vendedor)
            return True
        if vendedor.stock < vendedor.cola.index(persona) + 1:
            return True
        precio_minimo = min([int(producto.precio) for producto in
                             vendedor.productos])
        if self.concha:
            precio_minimo = min([int(producto.precio) * 1.25 for producto in
                                vendedor.productos])
        if precio_minimo > persona.pesos_diarios:
            return True
        if persona.tiempo_paciencia < (vendedor.cola.index(persona)) * \
                vendedor.rapidez_atencion:
            return True
        if isinstance(persona, Funcionario):
            no_repetir = persona.vendedores_dia_anterior_snack + \
                         persona.vendedores_dia_anterior_almuerzo
            if vendedor.nombrecompleto in no_repetir:
                return True

    def actualizar_colas(self, cola_actual):
        """
        Se usa para actualizar los cambios de cola cuando llega un
        funcionario a comprar un snack
        :param cola_actual: decorador que entrega el atributo cola
        :return:
        """
        cola = cola_actual()
        compradores_en_cola = [compr for compr in cola
                               if isinstance(compr, Alumno)]
        for persona in compradores_en_cola:
            if self.comprobar_cambio_de_cola(persona):
                # solo la primera vale oomo cambio de cola
                persona.numero_de_rechazos += 1
                self.abandonos_cola_dia += 1
            while self.comprobar_cambio_de_cola(persona):
                if persona.cambiar_de_cola1() is not None:
                    # print("La persona", persona,
                    #      "no tiene más opciones que ir a Quick Devil")
                    break
                # print("2 :", persona, "se cambió de cola")

    def actualizar_colas2(self, cola_actual):
        """Lo mismo que arriba pero para colas de almuerzo"""
        cola = cola_actual()
        compradores_en_cola = [compr for compr in cola
                               if isinstance(compr, Alumno)]
        for persona in compradores_en_cola:
            if self.comprobar_cambio_de_cola(persona):
                # solo la primera vale oomo cambio de cola
                persona.numero_de_rechazos += 1
                self.abandonos_cola_dia += 1
            while self.comprobar_cambio_de_cola(persona):
                if persona.cambiar_de_cola2() is not None:
                    # print("La persona", persona,
                    #      "no tiene más opciones que ir a Quick Devil")
                    if persona.pesos_diarios < (self.quickdevil.
                                                almuerzos[0].precio):
                        # print("\tNo tiene dinero para almorzar")
                        self.cantidad_no_almuerzan += 1
                    else:
                        # print("\tTiene dinero para comprar en el local")
                        pass
                    break
                # print("2 :", persona, "se cambió de cola")

    def persona_esta_comprando(self, persona):
        """
        Verifica si una persona que ha llegado a los puestos, ya estaba ahí
        comprando un snack o almuerzo
        :param persona: Objeto persona
        :return: Booleano
        """
        for vendedor in self.vendedores:
            if persona in vendedor.cola:
                # print("Debería haber llegado", persona,
                # "a puestos, pero ya está comprando.")
                persona.comprando = True
                return True
        return False

    def generar_llamada_carabinero(self):  # Descriptiva
        dias = round(expovariate(self.lambda_carabineros))
        self.dia_llegada_carabinero = self.fechahora + timedelta(days=dias)

    def generar_carabinero(self):
        """
        Elige al azar una de las 2 personalidades y elige al carabinero que
        va a ir a fiscalizar ese día. Se generan además sus distintas probs.
        """
        personalidad = choice(["Mr. Hyde", "Dr. Jekyll"])
        opciones = [cab for cab in self.carabineros
                    if cab.personalidad == personalidad]
        self.carabinero = choice(opciones)
        if self.carabinero.personalidad == "Mr. Hyde":
            self.carabinero.prob_engaño = float(self.personalidad_hyde[1])
            self.carabinero.tasa_productos_revisar = float(self.
                                                           personalidad_hyde
                                                           [0])
        elif self.carabinero.personalidad == "Dr. Jekyll":
            self.carabinero.prob_engaño = float(self.personalidad_jekyll[1])
            self.carabinero.tasa_productos_revisar = float(self.
                                                           personalidad_jekyll
                                                           [0])

    def generar_proxima_temperatura_extrema(self):  # Descriptivo
        dias = randint(2, 20)
        self._proxima_temperatura_extrema = self.fechahora + \
            timedelta(days=dias)

    def generar_proxima_lluvia_de_hamburguesas(self):  # Descriptivo
        n = (self.fechahora.date() - self.ultima_temperatura_extrema.date()).\
            days
        dias = round(expovariate(1 / (21 - n)))
        self._proxima_lluvia_de_hamburguesas = self.fechahora + \
            timedelta(days=dias)
        # print(self._proxima_lluvia_de_hamburguesas)

    @property
    def prob_enfermarse(self):
        """
        Si hay lluvia el dia antes esta probabilidad es el doble
        :return: float
        """
        if self.dia_anterior_lluvia:
            return PROBABILIDAD_ENFERMARSE * 2
        else:
            return PROBABILIDAD_ENFERMARSE

    @property
    def proxima_persona_llega_universidad(self):
        """
        Entrega la próxima persona en llegar entre las que no han llegado
        :return: Tupla(Objeto persona, float)
        """
        no_han_llegado = [persona for persona in self.miembrosuc if
                          persona.tiempo_llegada_universidad >
                          self.tiempo_actual]
        if len(no_han_llegado) > 0:
            persona = sorted(no_han_llegado,
                             key=lambda x: x.tiempo_llegada_universidad)[0]
            return persona, persona.tiempo_llegada_universidad
        return None, float("Inf")

    @property
    def proxima_persona_es_atendida(self):
        """
        Entrega próxima persona que ya fue atendida, es decir ya compró.
        :return:  Tupla(Objeto Persona, float)
        """
        vendedores_con_cola = [vendedor for vendedor in self.vendedores
                               if len(vendedor.cola) > 0]
        if len(vendedores_con_cola) > 0:
            vendedor = sorted(vendedores_con_cola, key=lambda
                              x: x.tiempo_atencion_primer_cliente)[0]
            return vendedor, vendedor.tiempo_atencion_primer_cliente
        return None, float("Inf")

    @property
    def proxima_persona_llega_a_puestos(self):
        """
        Proxima persona que llega a puestos a comprar snack
        :return: Tupla(Objeto MiembroUC, float)
        """
        miembrosuc_disponibles = [persona for persona in self.miembrosuc
                                  if persona._tiempo_llegada_a_puestos
                                  is not None]
        if len(miembrosuc_disponibles) > 0:
            comprador = sorted(miembrosuc_disponibles, key=lambda x:
                               x._tiempo_llegada_a_puestos)[0]
            tiempo_llegada = comprador._tiempo_llegada_a_puestos
            if not self.persona_esta_comprando(comprador):
                return comprador, tiempo_llegada
            else:
                comprador._tiempo_llegada_a_puestos = None
        return None, float("Inf")

    @property
    def proxima_persona_llega_a_puestos_almuerzo(self):
        """
        Proxima persona que llega a puestos a comprar almuerzo
        :return: Tupla(Objeto MiembroUC, float)
        """
        miembrosuc_disponibles = [persona for persona in self.miembrosuc
                                  if persona._tiempo_llegada_a_puestos2
                                  is not None]
        if len(miembrosuc_disponibles) > 0:
            comprador = sorted(miembrosuc_disponibles, key=lambda x:
                               x._tiempo_llegada_a_puestos2)[0]
            tiempo_llegada = comprador._tiempo_llegada_a_puestos2
            if not self.persona_esta_comprando(comprador):
                return comprador, tiempo_llegada
            else:
                comprador._tiempo_llegada_a_puestos2 = None
        return None, float("Inf")

    @property
    def proximo_carabinero_llega(self):
        """
        Proximo carabinero que llega a algún puesto a fiscalizar
        :return: Tupla(Objeto Carabinero, float)
        """
        if self.tiempo_actual < TIEMPO_IRSE_CARABINEROS and \
                self.carabinero is not None:
            # if hour < 13:40
            return self.carabinero, self.tiempo_llegada_carabinero
        return None, float("Inf")

    @property
    def proximo_vendedor_se_instala(self):
        """
        Proximo vendedor que instala su puesto. Vendedores que ya empezaron
        instalados no aparecerán acá
        :return: Tupla(Objeto Vendedor, float)
        """
        vendedores_sin_instalar = [ven for ven in self.vendedores
                                   if not ven.instalado]
        if len(vendedores_sin_instalar) > 0:
            prox_vendedor = sorted(vendedores_sin_instalar,
                                   key=lambda x: x._tiempo_instalacion)[0]
            return prox_vendedor, prox_vendedor._tiempo_instalacion
        return None, float("Inf")

    @property
    def proximo_dia(self):
        """Cuando termina el día retorna ese minuto de cierre."""
        return TIEMPO_MAXIMO_DIA

    @property
    def proxima_temperatura_extrema(self):  # Descriptivo
        if self.fechahora == self._proxima_temperatura_extrema:
            return 0
        return float("Inf")

    @property
    def proxima_lluvia_de_hamburguesas(self):  # Descriptivo
        if self.fechahora == self._proxima_lluvia_de_hamburguesas:
            return 0
        return float("Inf")

    @property
    def proximo_fin_de_semana(self):  # Descriptivo
        if self.fechahora.strftime("%A") == "Saturday" or \
                        self.fechahora.strftime("%A") == "Sunday":
            return 0
        return float("Inf")

    @property
    def proximo_evento(self):
        """
        Toma los tiempos de todos los posibles eventos y elige el más próximo
        :return: String con el nombre del evento
        """
        tiempos = [self.proxima_persona_llega_universidad[1],
                   self.proxima_persona_es_atendida[1],
                   self.proxima_persona_llega_a_puestos[1],
                   self.proxima_persona_llega_a_puestos_almuerzo[1],
                   self.proximo_carabinero_llega[1],
                   self.proximo_vendedor_se_instala[1],
                   self.proximo_dia,
                   self.proxima_temperatura_extrema,
                   self.proxima_lluvia_de_hamburguesas,
                   self.proximo_fin_de_semana]

        tiempo_prox_evento = min(tiempos)

        eventos = ["llegada_persona_universidad",
                   "persona_compra_snack",
                   "persona_llega_a_puestos",
                   "persona_llega_a_puestos_almuerzo",
                   "carabinero_llega",
                   "vendedor_instala",
                   "nuevo_dia",
                   "temperatura_extrema",
                   "lluvia_de_hamburguesas",
                   "fin_de_semana"]

        return eventos[tiempos.index(tiempo_prox_evento)]

    def llegada_universidad(self):
        """
        Verifica si es posible que almuerce ese día y también genera su hora
        de ir a comprar snack de ser necesario
        """
        persona, tiempo = self.proxima_persona_llega_universidad
        self.tiempo_actual = tiempo
        fechahora = self.fechahora + timedelta(minutes=tiempo)
        # print("1 : Ha llegado", persona,
        #      "a la Universidad en la hora", self.tiempo_actual, fechahora)
        if persona._tiempo_decidir_almorzar == float("Inf"):
            self.cantidad_no_almuerzan[str(fechahora.strftime("%B"))] += 1
            # print("\tNo almuerza ese día")
        elif persona._tiempo_decidir_almorzar != float("Inf"):
            pass
            # print("\tSI almuerza")
        compra_snack = choice([0, 1])
        if compra_snack == 1 and len(persona.colas_snack) > 0:
            # print("\t", persona, "quiere comprar snack ese dia")
            persona.generar_tiempo_decidir_comprar_snack2(tiempo)
            persona.generar_tiempo_llegada_a_puestos(self.lambda_traslado)

    def persona_compra_snack(self):
        """
        Se saca al comprador de la cola donde estaba, se decide qué producto
        comprar. Alumno buscará el más barato, Funcionario el de mejor calidad
        y que pueda pagar. También se restringe que Funcionario le compre al
        mismo el proximo dia. Se resta el precio del dinero del comprador,
        se resta del stock del vendedor y se actualiza el comienzo de atencion
        del siguiente en la cola. Finalmente se revisa si se enfermó con el
        producto y si es que es necesario que almuerce o compre un snack
        inmediatamente después de esta compra
        """
        vendedor, tiempo = self.proxima_persona_es_atendida
        self.tiempo_actual = tiempo
        fechahora = self.fechahora + timedelta(minutes=tiempo)
        comprador = vendedor.cola.popleft()
        # print(comprador, comprador.preferencias_almuerzo)
        # print(comprador, comprador.preferencias_snack)
        for producto in vendedor.productos:
            producto.actualizar_putrefaccion(tiempo, self.calor_intenso)
            producto.actualizar_calidad(self.frio_intenso)
            self.calidades.append(producto.calidad)
        if isinstance(comprador, Alumno):  # compra el mas barato
            producto_comprado = vendedor.productos[0]
            if vendedor.tipo_de_comida != "Snack":
                comprador.almuerza = True
        elif isinstance(comprador, Funcionario):  # mejor calidad
            opciones = [prod for prod in vendedor.productos
                        if prod.precio <= comprador.pesos_diarios]
            if self.concha:
                opciones = [prod for prod in vendedor.productos
                            if prod.precio * FACTOR_CONCHA <=
                            comprador.pesos_diarios]
            producto_comprado = sorted(opciones,
                                       key=lambda x: x.calidad,
                                       reverse=True)[0]
            if vendedor.tipo_de_comida == "Snack":
                # se agrega la cola que se estaba ignorando y se guarda la que
                # se ignorara el siguiente dia
                if len(comprador.vendedores_dia_anterior_snack) > 0:
                    comprador.vendedores_dia_anterior_snack.pop(0)
                comprador.vendedores_dia_anterior_snack.append(vendedor.
                                                               nombrecompleto)
            else:
                if len(comprador.vendedores_dia_anterior_almuerzo) > 0:
                    comprador.vendedores_dia_anterior_almuerzo.pop(0)
                name = vendedor.nombrecompleto
                comprador.vendedores_dia_anterior_almuerzo.append(name)
                comprador.almuerza = True
        if self.concha:
            comprador.pesos_diarios -= float(producto_comprado.precio) * \
                                       FACTOR_CONCHA
        else:
            comprador.pesos_diarios -= float(producto_comprado.precio)

        vendedor.stock -= 1
        vendedor.dias_sin_ventas = -1
        vendedor.unidades_vendidas[producto_comprado.nombre] += 1
        self.productos_vendidos_un_dia += 1
        # ahora se empieza a atender al siguiente
        if len(vendedor.cola) > 0:
            vendedor.cola[0].tiempo_comienzo_atencion = tiempo
        # print("4 :", comprador, "le ha comprado un snack a",
        #       vendedor.nombrecompleto, "en la hora", self.tiempo_actual)

        if producto_comprado.calidad < CALIDAD_LIMITE:
            prob = random()

            if prob < self.prob_enfermarse:
                # print("    5 :", comprador, "se ha enfermado. Nunca más le"
                #                        "comprará a", vendedor)
                vendedor.enfermados += 1
                if vendedor.tipo_de_comida == "Snack":
                    comprador.colas_snack.pop(comprador.ind_cola_actual)
                    #comprador.preferencias_snack.remove(vendedor.nombre)  # BORRAR DESPUES
                else:
                    comprador.colas_almuerzo.pop(comprador.ind_cola_actual2)
                    # comprador.preferencias_almuerzo.remove(
                    #    vendedor.nombre)  # BORRAR DESPUES
        if comprador.comprando:
            if vendedor.tipo_de_comida == "Snack":
                comprador._tiempo_llegada_a_puestos2 = tiempo
            else:
                comprador._tiempo_llegada_a_puestos = tiempo
            comprador.comprando = False
        if vendedor.tipo_de_comida != "Snack":
            if fechahora.hour == 12:
                self.cantidad_almuerzos12_dia += 1
            elif fechahora.hour == 13:
                self.cantidad_almuerzos13_dia += 1
            elif fechahora.hour == 14:
                self.cantidad_almuerzos14_dia += 1

    def persona_llega_a_puestos(self):
        """
        Se ingresa el comprador de snack a la cola correcta (según el orden y
        restricciones)
        """
        comprador, tiempo = self.proxima_persona_llega_a_puestos
        comprador.ind_cola_actual = 0
        self.tiempo_actual = tiempo
        fechahora = self.fechahora + timedelta(minutes=tiempo)
        if len(comprador.colas_snack) > 0:
            comprador.ingresar_a_cola_snack(tiempo)
            # print("3 :", comprador,
            #     "llegó a los puestos de comida y quiere comprar un snack en",
            #      tiempo, fechahora)
            while self.comprobar_cambio_de_cola(comprador):
                if comprador.cambiar_de_cola1() is not None:
                    # print("La persona", comprador, "se cambia y",
                    #      "no tiene más opciones que ir a Quick Devil")
                    comprador.quick = True
                    break
                # print("2 :", comprador.nombrecompleto, "se cambió de cola")
            if not comprador.quick and isinstance(comprador, Funcionario):
                # hay que ver el efecto
                self.actualizar_colas(comprador
                                      .colas_snack[comprador.ind_cola_actual])
                comprador.colas_usadas = []
        else:
            # print("La persona", comprador, "llegó a los puestos y",
            #      "no tiene más opciones que ir a Quick Devil")
            pass

        comprador.quick = False
        comprador._tiempo_llegada_a_puestos = None  # se reinicia

    def persona_llega_a_puestos_almuerzo(self):
        """
        Se ingresa el comprador de almuerzo a la cola correcta (según el orden,
        restricciones)
        """
        comprador, tiempo = self.proxima_persona_llega_a_puestos_almuerzo
        comprador.ind_cola_actual2 = 0
        self.tiempo_actual = tiempo
        fechahora = self.fechahora + timedelta(minutes=tiempo)
        if len(comprador.colas_almuerzo) > 0:
            comprador.ingresar_a_cola_almuerzo(tiempo)
            # print("3 :", comprador,
            #     "llegó a los puestos de comida y quiere comprar ALMUERZO en",
            #      tiempo, fechahora)
            while self.comprobar_cambio_de_cola(comprador):
                if comprador.cambiar_de_cola2() is not None:
                    # print("La persona", comprador, "se cambia y",
                    #      "no tiene más opciones que ir a Quick Devil")
                    if comprador.pesos_diarios < (self.quickdevil.
                                                  almuerzos[0].precio):
                        # print("\tNo tiene dinero para almorzar")
                        self.cantidad_no_almuerzan += 1
                    else:
                        # print("\tTiene dinero para comprar en el local")
                        pass
                    comprador.quick = True
                    break
            if not comprador.quick and isinstance(comprador, Funcionario):
                # hay que ver el efecto
                self.actualizar_colas2(comprador
                                       .colas_almuerzo[comprador.
                                                       ind_cola_actual2])
                comprador.colas_usadas = []
        else:
            # print("La persona", comprador, "llegó a los puestos y",
            #      "no tiene más opciones que ir a Quick Devil")
            if comprador.pesos_diarios < (self.quickdevil.
                                          almuerzos[0].precio):
                # print("\tNo tiene dinero para almorzar")
                self.cantidad_no_almuerzan += 1
            else:
                # print("\tTiene dinero para comprar en el local")
                pass

        comprador.quick = False
        comprador._tiempo_llegada_a_puestos = None  # se reinicia
        comprador._tiempo_llegada_a_puestos2 = None  # se reinicia

    def carabinero_comienza_a_fiscalizar(self):
        """
        Se deja de fiscalizar al vendedor anterior y se ve si se escapó o
        si se confiscó (para actualizar colas). Luego se comienza a fiscalizar
        al siguiente (aleatorio) y se actualiza el tiempo de atención del
        primero en la cola
        """
        carabinero, tiempo = self.proximo_carabinero_llega
        self.tiempo_actual = tiempo
        if carabinero.vendedor_actual is not None:  # el anterior
            if carabinero.vendedor_actual.ausente:
                carabinero.vendedor_actual.dias_ausente = self.dias_susto + 1
                if carabinero.vendedor_actual.tipo_de_comida == "Snack":
                    self.actualizar_colas(carabinero.vendedor_actual.
                                          entrega_cola())
                else:
                    self.actualizar_colas2(carabinero.vendedor_actual.
                                           entrega_cola())
            elif carabinero.vendedor_actual.confiscado:
                if carabinero.vendedor_actual.tipo_de_comida == "Snack":
                    self.actualizar_colas(carabinero.vendedor_actual.
                                          entrega_cola())
                else:
                    self.actualizar_colas2(carabinero.vendedor_actual.
                                           entrega_cola())
            carabinero.vendedor_actual.fiscalizando = False
            carabinero.fiscalizados.append(carabinero.vendedor_actual)
            # print("Se terminó de fiscalizar a", carabinero.vendedor_actual)
        if len(self.vendedores) > len(carabinero.fiscalizados):
            vendedor = choice(list(set(self.vendedores) -
                                   set(carabinero.fiscalizados)))
            carabinero.fiscalizar(vendedor, tiempo, self.calor_intenso)
            # print("-" * 30, carabinero, "está fiscalizando a", vendedor)
            if len(vendedor.cola) > 0:  # si hay cola
                vendedor.cola[0].tiempo_comienzo_atencion = tiempo + \
                                                            40/len(self.
                                                                   vendedores)
        self.tiempo_llegada_carabinero += 40/len(self.vendedores)

    def vendedor_instala(self):
        """ Vendedor instala su puesto, está disponible para vender"""
        vendedor, tiempo = self.proximo_vendedor_se_instala
        self.tiempo_actual = tiempo
        fechahora = self.fechahora + timedelta(minutes=tiempo)
        # print("El vendedor", vendedor, "se instaló a las", tiempo, fechahora)
        vendedor.instalado = True

    def nuevo_dia(self):
        """
        Muchos cambios para empezar el siguiente día. Lo primero es sumar en
        los contadores de las distintas estadísticas, ya que varias son
        diarias. Luego se ve la posibilidad de concha acústica si el siguiente
        día será viernes. Después para los miembros UC, se resetea que no
        hayan llegado a la universidad, se generan los nuevos tiempos de
        almuerzo, paciencias y en caso de cambio de mes se actualiza mesada.
        Más adelante se ven los vendedores, se van de la universidad, se
        actualizan sus stocks, se
        cambian los dias sin ventas o dias de ausencia de ser necesario, se
        vacían las colas y se hace el cambio de precios al cambiar mes.
        Finalmente se ven los eventos no programados, se recalcula llegada
        de carabinero de ser necesario o se resetea temperaturas o lluvia.
        """
        if self.fechahora.strftime("%A") != "Saturday" and \
                self.fechahora.strftime("%A") != "Sunday":
            self.productos_vendidos_cada_dia.append(self.
                                                    productos_vendidos_un_dia)
            self.productos_vendidos_un_dia = 0
            self.abandonos_cola_dias.append(self.abandonos_cola_dia)
            for vendedor in self.vendedores:
                if not vendedor.ausente:
                    for producto in vendedor.productos:
                        producto.actualizar_putrefaccion(240,
                                                         self.calor_intenso)
                        if producto.putrefaccion > PUTREFACCION_DESCOMPUESTO:
                            self.productos_descompuestos += 1
            self.cantidad_almuerzos12_dias.append(
                self.cantidad_almuerzos12_dia)
            self.cantidad_almuerzos13_dias.append(
                self.cantidad_almuerzos13_dia)
            self.cantidad_almuerzos14_dias.append(
                self.cantidad_almuerzos14_dia)
        self.abandonos_cola_dia = 0
        self.cantidad_almuerzos12_dia = 0
        self.cantidad_almuerzos13_dia = 0
        self.cantidad_almuerzos14_dia = 0
        mes_anterior = self.fechahora.strftime("%B")
        self.fechahora += timedelta(days=1)
        self.tiempo_actual = 0
        # print("\n", "-" * 100, "Cambió el día a", self.fechahora)
        dif = (self.fechahora.date() -
               datetime(year=2017, month=3, day=1).date()).days
        percent = dif / 120
        if percent == 0.25 or percent == 0.5 or percent == 0.75 \
                or percent == 1:
            drawProgressBar(percent)  # Para mostrar Progreso
        self.concha = False
        if self.fechahora.strftime("%A") == "Friday":
            p = random()
            if p < self.pconcha:
                self.num_conchas += 1
                self.concha = True
                # print("HAY CONCHA ESTÉREO")
                self.ultima_concha = self.fechahora
            elif (self.fechahora.date() -
                    self.ultima_concha.date()).days > MAXIMO_DIAS_SIN_CONCHA:
                self.num_conchas += 1
                self.concha = True
                self.ultima_concha = self.fechahora
                # print("HAY CONCHA ESTÉREO")
            else:
                # print("NO HAY CONCHA")
                pass

        for persona in self.miembrosuc:
            persona.numero_de_rechazos = 0
            persona.generar_tiempo_llegada_universidad(self.c_llegada)
            persona._tiempo_decidir_comprar_snack = None
            persona.comprando = False
            persona.quick = False
            persona.almuerza = False
            persona.generar_tiempo_decidir_almorzar()
            persona.generar_tiempo_llegada_a_puestos2(self.lambda_traslado)
            persona.colas_usadas = []

            if isinstance(persona, Alumno):
                persona.generar_tiempo_paciencia(self.alpha_paciencia,
                                                 self.beta_paciencia)
                if mes_anterior != self.fechahora.strftime("%B"):
                    persona.generar_mesada(self.base_mesada)
                    # print("RECALCULAMOS MESADA")
                    persona.generar_pesos_diarios()
            else:
                persona.cambios_de_cola = 0

        self.vendedores_sin_stock = 0
        self.posibles_vendedores = []
        for persona in self.vendedores:
            if persona.tipo_de_comida != "Snack":
                for comprador in persona.cola:
                    self.cantidad_no_almuerzan[mes_anterior] += 1
                    # print(comprador, "no pudo almorzar")
            for producto, cantidad in persona.unidades_vendidas.items():
                if cantidad == 0:
                    persona.contador_sin_ventas[producto] += 1
                persona.unidades_vendidas[producto] = 0
            if not persona.ausente:
                persona.dias_sin_ventas += 1
            if persona.dias_sin_ventas == DIAS_BANCARROTA:
                # print(persona, "se fue a la BANCARROTA, no venderá más.")
                persona.ausente = True
                persona.dias_ausente = float("Inf")  # no vuelve
            if persona.stock == 0 and not persona.confiscado:
                persona.contador_stock_out += 1  # se reinicia a 0 cada mes
                self.vendedores_sin_stock += 1
            if mes_anterior != self.fechahora.strftime("%B"):
                # cambiamos precios
                nuevos_productos = []
                for producto in persona.productos:
                    P = producto.precio
                    N1 = persona.contador_sin_ventas[producto.nombre]
                    N2 = persona.contador_stock_out
                    precio = P - P * 5 * N1 / 100 + P * 6 * N2 / 100
                    if precio < producto.precio_minimo:
                        precio = producto.precio_minimo
                    # print("El precio cambiaría de", P, "a", precio, N1, N2)
                    # new = Producto()
            self.vendedores_sin_stock_dias.append(self.vendedores_sin_stock)
            persona.cola = deque()
            persona.generar_stock(self.alpha_stock, self.beta_stock)
            persona.instalado = False
            persona.confiscado = False
            if persona.ausente:
                persona.dias_ausente -= 1
                if persona.dias_ausente == 0:
                    persona.ausente = False
            if not persona.ausente:
                persona.generar_tiempo_instalacion()
                self.posibles_vendedores.append(persona)
        if self.carabinero is not None:
            self.num_llamadas += 1
            self.carabinero.fiscalizados = []
            self.vendedor_actual = None
            self.carabinero = None
        self.tiempo_llegada_carabinero = TIEMPO_LLEGADA_CARABINEROS
        if self.fechahora.date() == self.dia_llegada_carabinero.date():
            self.generar_carabinero()
            # print("HOY", self.fechahora, "VIENE UN CARABINERO")
            self.generar_llamada_carabinero()
        self.frio_intenso = False
        self.calor_intenso = False
        if self.lluvia:
            self.dia_anterior_lluvia = True
        else:
            self.dia_anterior_lluvia = False
        self.lluvia = False
        # print(self.prob_enfermarse)

    def temperatura_extrema(self):
        """
        Se decide si será frio o calor intenso y se calcula el proximo de
        estos eventos
        """
        self.num_temperaturas += 1
        self.tiempo_actual = self.proxima_temperatura_extrema
        self.ultima_temperatura_extrema = self.fechahora
        situacion = choice(["frio", "calor"])
        # print("HOY", self.fechahora, "HAY TEMPERATURA EXTREMA", situacion)
        if situacion == "frio":
            self.frio_intenso = True
        else:
            self.calor_intenso = True
        self.generar_proxima_temperatura_extrema()

    def lluvia_de_hamburguesas(self):
        """
        Se activa la opción de lluvia y se genera la proxima
        """
        self.num_lluvias += 1
        self.tiempo_actual = self.proxima_lluvia_de_hamburguesas
        # print("HOY", self.fechahora, "HAY LLUVIA DE HAMBURGUESAS")
        self.lluvia = True
        self.generar_proxima_lluvia_de_hamburguesas()
        self.nuevo_dia()

    def run(self):
        """
        Corre la simulacion, busca los eventos que van a ocurri en el orden
        correspondiente. Sigue en ejecución hasta llegar a Julio. Dura 40 seg
        """
        while self.fechahora < datetime(year=2017, month=7, day=1):
            evento = self.proximo_evento
            if evento == "llegada_persona_universidad":
                self.llegada_universidad()
            elif evento == "persona_compra_snack":
                self.persona_compra_snack()
            elif evento == "persona_llega_a_puestos":
                self.persona_llega_a_puestos()
            elif evento == "persona_llega_a_puestos_almuerzo":
                self.persona_llega_a_puestos_almuerzo()
            elif evento == "carabinero_llega":
                self.carabinero_comienza_a_fiscalizar()
            elif evento == "vendedor_instala":
                self.vendedor_instala()
            elif evento == "nuevo_dia":
                self.nuevo_dia()
            elif evento == "temperatura_extrema":
                self.temperatura_extrema()
            elif evento == "lluvia_de_hamburguesas":
                self.lluvia_de_hamburguesas()
            elif evento == "fin_de_semana":
                for persona in self.vendedores:
                    persona.dias_sin_ventas -= 1  # para mantenerse
                self.nuevo_dia()
        self.estadisticas = [self.promedio_dinero_confiscado,
                             self.productos_vendidos_durante_un_dia[0],
                             self.productos_vendidos_durante_un_dia[1],
                             self.productos_vendidos_durante_un_dia[2],
                             self.confiscaciones_por_tipo[0],
                             self.confiscaciones_por_tipo[1],
                             self.num_llamadas,
                             self.num_conchas,
                             self.num_temperaturas,
                             self.num_lluvias,
                             self.promedio_horario_almuerzo[0],
                             self.promedio_horario_almuerzo[1],
                             self.promedio_horario_almuerzo[2],
                             self.cantidad_no_almuerzan,
                             self.promedio_calidad,
                             self.enfermados,
                             self.productos_descompuestos,
                             self.promedio_abandono_colas,
                             self.promedio_vendedores_sin_stock,
                             self.engaños_por_tipo[0],
                             self.engaños_por_tipo[1]]
        # self.mostrar_estadisticas()

    @property
    def productos_vendidos_durante_un_dia(self):
        """
        Usa los contadores que estaban a lo largo del programa
        :return: Tupla(float minimo, float maximo, float promedio)
        """
        promedio = sum(self.productos_vendidos_cada_dia) / \
            len(self.productos_vendidos_cada_dia)
        minimo = min(self.productos_vendidos_cada_dia)
        maximo = max(self.productos_vendidos_cada_dia)
        return minimo, maximo, promedio

    @property
    def promedio_horario_almuerzo(self):
        """
        Usa los contadores que estaban a lo largo del programa para dar el
        promedio de los que comen entre 12 y 1, 1 y 2 o 2 y 3
        :return: Tupla(float promedio 12-1, float promedio 1-2, float 2-3)
        """
        promedio12 = sum(self.cantidad_almuerzos12_dias) / \
            len(self.cantidad_almuerzos12_dias)
        promedio13 = sum(self.cantidad_almuerzos13_dias) / \
            len(self.cantidad_almuerzos13_dias)
        promedio14 = sum(self.cantidad_almuerzos14_dias) / \
            len(self.cantidad_almuerzos14_dias)
        return promedio12, promedio13, promedio14

    @property
    def promedio_calidad(self):  # Descriptivo
        promedio = sum(self.calidades) / len(self.calidades)
        return promedio

    @property
    def promedio_abandono_colas(self):  # Descriptivo
        promedio = sum(self.abandonos_cola_dias) / len(self.
                                                       abandonos_cola_dias)
        return promedio

    @property
    def promedio_vendedores_sin_stock(self):  # Descriptivo
        promedio = sum(self.vendedores_sin_stock_dias) \
                   / len(self.vendedores_sin_stock_dias)
        return promedio

    @property
    def promedio_dinero_confiscado(self):  # Descriptivo
        suma = 0
        total = 0
        for carabinero in self.carabineros:
            suma += sum(carabinero.cantidad_confiscada)
            total += len(carabinero.cantidad_confiscada)
        if total == 0:
            return 0
        return suma / total

    @property
    def confiscaciones_por_tipo(self):
        """
        Entrega las confiscaciones para los Jekyll y los Hyde
        :return: Tupla(int de confiscaciones jek, int de confiscaciones hyde)
        """
        confiscaciones_jekyll = 0
        confiscaciones_hyde = 0
        for carabinero in self.carabineros:
            if carabinero.personalidad == "Dr. Jekyll":
                confiscaciones_jekyll += len(carabinero.cantidad_confiscada)
            else:
                confiscaciones_hyde += len(carabinero.cantidad_confiscada)
        return confiscaciones_jekyll, confiscaciones_hyde

    @property
    def engaños_por_tipo(self):
        """
            Entrega los engaños para los Jekyll y los Hyde
            :return: Tupla(int de engaños jek, int de engaños hyde)
            """
        engaños_jekyll = 0
        engaños_hyde = 0
        for carabinero in self.carabineros:
            if carabinero.personalidad == "Dr. Jekyll":
                engaños_jekyll += carabinero.engaños
            else:
                engaños_hyde += carabinero.engaños
        return engaños_jekyll, engaños_hyde

    @property
    def enfermados(self):
        total = 0
        for ven in self.vendedores:
            total += ven.enfermados
        return total

    def mostrar_estadisticas(self):
        """Muestra las estadisticas de la simulacion"""
        print("\n")
        print("-" * 50, "Estadisticas", "-" * 50)
        print("1- Promedio dinero confiscado: {}".
              format(self.promedio_dinero_confiscado))
        print("2- Productos vendidos durante el día:\n\t..Minimo: {}\n\t.."
              "Maximo: {}\n\t..Promedio: {}".
              format(*self.productos_vendidos_durante_un_dia))
        print("3- Cantidad confiscaciones:\n\t..Dr Jekyll: {}"
              "\n\t..Mr Hyde: {}".format(*self.confiscaciones_por_tipo))
        print("4- Llamadas a carabineros: {}".format(self.num_llamadas))
        print("5- Numero de Conchas Estéreo: {}".format(self.num_conchas))
        print("6- Numero de temperaturas extremas: {}".
              format(self.num_temperaturas))
        print("7- Numero de lluvias de hamburguesas: {}".format(self.
                                                                num_lluvias))
        print("8- Numero promedio de personas almorzando por horario\n\t.."
              "12:00-12:59: {}\n\t..13:00-13:59: {}\n\t..14:00-14:59: {}".
              format(*self.promedio_horario_almuerzo))
        print("9- Cantidad alumnos que no almorzaron por mes:")
        for month, cantidad in self.cantidad_no_almuerzan.items():
            print("\t..{} no almorzaron {} personas".format(month, cantidad))
        print("10- Calidad promedio: {}".format(self.promedio_calidad))
        print("11- Cantidad de miembros UC enfermados por vendedor:")
        for vendedor in self.vendedores:
            print("\t..{} enfermó a {} personas".format(vendedor,
                                                        vendedor.enfermados))
        print("12- Productos descompuestos: {}".
              format(self.productos_descompuestos))
        print("13- Promedio abandono colas diario: {}".
              format(self.promedio_abandono_colas))
        print("14- Promedio vendedores sin stock diario: {}".format(
              self.promedio_vendedores_sin_stock))
        print("15- Cantidad de engaños:\n\t..Dr. Jekyll: {}\n\t..Mr. Hyde: {}".
              format(*self.engaños_por_tipo))


# sacado de https://stackoverflow.com/questions/3002085/
# python-to-print-out-status-bar-and-percentage
def drawProgressBar(percent, barLen=20):
    """
    Muestra el progreso de la simulación
    :param percent: float del porcentaje
    :param barLen: int del largo de la barra de progreso
    :return:
    """
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


# uc = MercadoUC(30, personas, 1, 3, 0.33, 80, 150, 3000, 20, 35, 0.5, (60, 20)
#               , 0.15, 0.0714, quickdevil, (0.25, 0.1), (0.1, 0.4), 3, 7000)
# uc.run()
