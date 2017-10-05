from random import uniform, randint, choice, expovariate

# Estos parametros son algunos de los definidos en el enunciado.
WEIGHT_FACTOR = 1000  # se usa para sacar B
MAX_PERSON_SPEED = 3
MIN_PERSON_SPEED = 1
MAX_PERSON_WEIGHT = 200
MIN_PERSON_WEIGHT = 40

ANIMAL_SPAWN_MIN = 160
ANIMAL_SPAWN_MAX = 200
ANIMAL_RANGE = 90

PEOPLE = 500

MAX_SIMULATION_TIME = 10000
SIMULATIONS = 20


# Pueden modificar y crear las clases que se les antoje.
class Animal:
    # Identificador unico para cada animal.
    # No tiene niguna utilidad mas que para probar el programa
    id = 0

    def __init__(self, prob_ataque, prob_letal, prob_escape_ataque, especie):
        self.especie = especie
        self.prob_ataque = prob_ataque
        self.prob_escape_ataque = prob_escape_ataque
        self.prob_letal = prob_letal
        self.kills = 0
        self.id = Animal.id
        Animal.id += 1
        self.posicion = randint(0, 100)
        # se asume que la tasa no cambia por animal entre eventos
        self.tasa_llegada_ataques = 1 / randint(2, 6)

    def puede_atacar(self, persona):
        # Retorna True si la persona esta dentro del rango de ataque
        if abs(self.posicion - persona.pos_inicial) <= 90:
            return True
        else:
            return False

    def tiempo_siguiente_ataque(self):
        self.siguiente_ataque = expovariate(self.tasa_llegada_ataques)
        return self.siguiente_ataque

    def tasa_ataque(self):
        # Retorna la tasa de ataques
        pass

    def __str__(self):
        imprime = "Animal" + self.especie + str(self.id)
        return imprime


class Person:
    id = 0
    def __init__(self):
        self.pos_inicial = randint(0, 100)  # km
        self.pos_actual = self.pos_inicial
        self.sex = choice(["M", "F"])
        self.weight = uniform(40, 200)
        self.safe = False
        self.is_dead = False
        self.id = Person.id
        Person.id += 1
        self.B = self.weight / 1000

        if self.sex == "M":
            self.coef = self.weight * randint(1, 3) / WEIGHT_FACTOR
        else:
            self.coef = self.weight / WEIGHT_FACTOR

        self.velocity = randint(MIN_PERSON_SPEED, MAX_PERSON_SPEED) #* self.coef

    def has_survived(self):
        # Retorna True si la persona esta en un km mayor a 100
        if self.pos_actual > 100:
            self.safe = True
            return True

    def tiempo_en_escapar(self):
        self.tiempo_safe = (100 - self.pos_actual) / self.velocity
        return self.tiempo_safe


    def move(self, dist):
        # Metodo para avanzar
        self.pos_actual += dist

    def __repr__(self):
        imprime = "Persona " + self.sex + " " + str(self.id)
        return imprime


class Zoo:
    def __init__(self, personas):
        self.tiempo_actual = 0
        self.tiempo_maximo = 10000
        self.personas = personas
        self.animales = []
        self.tasa_aparicion_animales = 1 / randint(160, 200)
        self.proximo_animal = expovariate(self.tasa_aparicion_animales)

        # Estadisticas
        self.promedio_sobrevivientes = None
        self.numero_victimas_por_raza = {}
        self.tiempo_ejecucion = 0

    def proximo_animal_aparece(self):
        #tiempo_aparicion = expovariate(self.tasa_aparicion_animales)
        return self.proximo_animal

    def proximo_animal_ataca(self):
        # retorna una tupla
        if len(self.animales) > 0:
            proximo_animal = sorted(self.animales,
                                    key=lambda x: x.tiempo_siguiente_ataque()
                                    )[0]
            return proximo_animal, proximo_animal.siguiente_ataque
        return (None, float("Inf"))

    def proxima_persona_escapa(self): # retorna una tupla
        for persona in self.personas:
            persona.tiempo_en_escapar()

        persona_cercana_a_escapar = sorted(self.personas,
                                           key=lambda x: x.tiempo_safe
                                           )[0]


        return (persona_cercana_a_escapar, persona_cercana_a_escapar.tiempo_safe)

    def proximo_evento(self):
        #print(self.personas, len(self.personas))
        tiempo1 = self.proximo_animal_aparece()

        tiempo2 = self.proximo_animal_ataca()
        tiempo3 = self.proxima_persona_escapa()
        #print(tiempo3)

        tiempos2 = [tiempo1,
                   tiempo2,
                   tiempo3]

        objetos = [None,
                   tiempos2[1][0],
                   tiempos2[2][0]]
        tiempos = [tiempos2[0],
                   tiempos2[1][1],
                   tiempos2[2][1]]
        #print(tiempos)
        tiempo_prox_evento = min(tiempos)
        if tiempo_prox_evento >= self.tiempo_maximo:
            print("fin")
            return None, "fin"
        eventos = ["animal_aparece",
                   "animal_ataca",
                   "persona_escapa"]
        #evento = eventos[tiempos.index(tiempo_prox_evento)]
        indice = tiempos.index(tiempo_prox_evento)
        return objetos[indice], eventos[indice]


    def animal_aparece(self):
        self.tiempo_actual = self.proximo_animal
        self.proximo_animal = self.tiempo_actual + \
                              expovariate(self.tasa_aparicion_animales)
        tipo_animal = [("Leon", 0.2, 0.9, 0.6),
                       ("Hipopotamo", 0.01, 0.95, 0.8),
                       ("Yeti", 0.4, 0.1, 0.5),
                       ("Panda rojo", 0.8, 1, 0.05)]
        animal = choice(tipo_animal)
        especie, ataque, letal, escape = animal[0], animal[1], animal[2], animal[3]
        nuevo_animal = Animal(ataque, letal, escape, especie)
        print("Aparecio un nuevo animal! Es un", nuevo_animal.especie)
        self.animales.append(nuevo_animal)

    def animal_ataca(self, animal):
        self.tiempo_actual += animal.siguiente_ataque
        personas_rango = [persona for persona in self.personas
                          if animal.puede_atacar(persona)]
        for persona in personas_rango:
            ataca = randint(0, 101)
            if persona.sex == "F":
                prob_ataque = animal.prob_ataque * persona.B * 100
            elif persona.sex == "M":
                prob_ataque = animal.prob_ataque * persona.B * 100 * \
                              randint(1, 3)
            if ataca <= prob_ataque:  # ataca
                print("[ATAQUE]: Persona siendo atacada por", animal.especie,
                      animal.id, "en T =", self.tiempo_actual)
                escapa = randint(0, 101)
                if escapa > animal.prob_escape_ataque * 100:  # no escapa
                    sobrevive = randint(0, 101)
                    if sobrevive <= animal.prob_letal:  # no sobrevive
                        print("[LETAL]: Persona murió por",
                          animal.especie,
                          animal.id, "en T =", self.tiempo_actual)
                        self.personas.remove(persona)
                    else:
                        print("[SURVIVE]: Persona sobrevivio el ataque por",
                              animal.especie,
                              animal.id, "en T =", self.tiempo_actual)
                else:
                    print("[ESCAPE]: Persona escapó el ataque por",
                          animal.especie,
                          animal.id, "en T =", self.tiempo_actual)

    def persona_escapa(self, persona):
        self.tiempo_actual += persona.tiempo_safe
        print("[SAFE]: Persona de sexo", persona.sex, "se salvo.")
        self.personas.remove(persona)

    def avance_personas(self, tiempo_anterior):
        # actualiza posicion de personas
        for persona in self.personas:
            distancia = persona.velocity * (self.tiempo_actual - tiempo_anterior)
            persona.move(distancia)

    def run(self):
        while self.tiempo_actual <= self.tiempo_maximo and len(self.personas) > 0:

            tiempo_anterior = self.tiempo_actual  # auxiliar
            objeto, evento = self.proximo_evento()
            if evento == "fin":
                break
            if evento == "animal_aparece":
                self.animal_aparece()
            elif evento == "animal_ataca":
                self.animal_ataca(objeto)
            elif evento == "persona_escapa":
                self.persona_escapa(objeto)
            self.avance_personas(tiempo_anterior)

if __name__ == "__main__":
    personas = []
    for i in range(500):
        personas.append(Person())
    zoo = Zoo(personas)
    zoo.run()





