from collections import deque
from random import sample, shuffle

class PrograBanner:
    def __init__(self):
        self.oferta_cursos = ()  # lista
        self.alumnos = {}  # diccionario

    def orden_de_llegada(self):
        lista_alumnos = []
        for alumno in self.alumnos.values():
            lista_alumnos.append(alumno)
        shuffle(lista_alumnos)  # random
        return lista_alumnos

    def asignar_curso1(self):
        lista_cursos_con_cupos = []
        lista_alumnos = self.orden_de_llegada()
        for alumno_asignar in lista_alumnos:
            for curso in self.oferta_cursos:
                curso.cupos.sort(key=lambda x : x.numero)
                if len(curso.cupos) > 0:
                    lista_cursos_con_cupos.append(curso)
            curso_asignado = sample(lista_cursos_con_cupos, 3)

            for curso in curso_asignado:
                cupo = curso.cupos.popleft()
                alumno_asignar.cupo.update({curso.sigla : cupo})

    def ajuste(self):
        for curso in self.oferta_cursos:
            for cupo in curso.cupos_extra:
                curso.cupos.append(cupo)
        curso.cupos_extra.clear()


    def asignar_curso2(self):
        lista_cursos_con_cupos = []
        lista_alumnos = self.orden_de_llegada()
        for alumno_asignar in lista_alumnos:
            for curso in self.oferta_cursos:
                curso.cupos.sort(key=lambda x: x.numero)
                if len(curso.cupos) > 0:
                    lista_cursos_con_cupos.append(curso)
            while len(alumno_asignar.cupo) < 5:
                curso_asignado = sample(lista_cursos_con_cupos, 1)
                if curso_asignado.sigla not in alumno_asignar.cupo:
                    cupo = curso_asignado.cupos.popleft()
                    alumno_asignar.cupo.update({curso_asignado.sigla : cupo})

    def botar_ramos(self):
        for alumno in self.alumnos.values():
            if alumno.unidad_academica.controla:
                for llave1, cupo1 in alumno.cupos.items():
                    for llave2, cupo2 in alumno.cupos.items():
                        if cupo1.horario == cupo2.horario and llave1 != llave2:
                            del alumno.cupo[llave1]
                            del alumno.cupo[llave2]

    def alumno_en_curso(self, num_alumno, sigla):
        alumno = self.alumnos[num_alumno]
        if sigla in alumno.cupo:
            num_cupo = alumno.cupo[sigla].numero
            print("El numero del cupo del alumno es:", num_cupo)
        else:
            print("El alumno no esta en el curso")

    def alumnos_en_curso(self, sigla):
        lista_alumno_en_curso = []
        for alumno in self.alumnos.values():
            if sigla in alumno.cupo:
                lista_alumno_en_curso.append(alumno.numero, alumno.cupo[sigla].numero)
        print("Alumnos inscritos en", sigla)
        for elem in lista_alumno_en_curso:
            print(elem[0], elem[1], sep=" - ")

    def cursos_comunes(self, num_alumno1, num_alumno2):
        alumno1 = self.alumnos[num_alumno1]
        alumno2 = self.alumnos[num_alumno2]
        lista_cursos_comunes = []
        for llave1 in alumno1.cupo:
            if llave1 in alumno2.cupo:
                lista_cursos_comunes.append(alumno1.cupo[llave1].sigla)
        print("Cursos comunes de {} y {}".format(num_alumno1, num_alumno2))
        for curso in lista_cursos_comunes:
            print(curso)


class Curso:
    def __init__(self, sigla, horario):
        self.sigla = sigla
        self.horario = horario
        self.cupos = []
        self.cupos_extra = []

    def __eq__(self, otro_curso):
        if self.horario == otro_curso.horario:
            return True
        else:
            return False

class Alumno:
    def __init__(self, numero, unidad_academica):
        self.numero = numero
        self.unidad_academica = unidad_academica
        self.cupo = {}  # key = sigla, value = Cupo


class Cupo:
    def __init__(self, numero, horario, sigla):
        self.numero = numero
        self.horario = horario
        self.sigla = sigla


class UnidadAcademica:
    def __init__(self, nombre, controla):
        self.nombre = nombre
        self._controla = controla

    @property
    def controla(self):
        return self._controla

    @controla.setter
    def controla(self, value):
        if value == "1":
            self._controla = True
        elif value == "0":
            self._controla = False
        else:
            print("Estamos mal cagamos")


sistema = PrograBanner()

with open("unidades.txt", "r") as archivo_unidades:
    diccionario = {}
    for linea in archivo_unidades:
        linea.strip()
        u_academica, controla = linea.split(",")
        unidad = UnidadAcademica(u_academica, controla)
        diccionario.update({u_academica : unidad})

with open("alumnos.txt", "r") as archivo_alumnos:
    for linea in archivo_alumnos:
        num_alumno, u_academica = linea.split(",")
        alumno = Alumno(num_alumno, diccionario[u_academica])
        sistema.alumnos.update({num_alumno : alumno})

with open("cursos.txt", "r") as archivo_cursos:
    for linea in archivo_cursos:
        linea.strip()
        sigla, cupos, cupo_extra, horario = linea.split()
        curso = 
