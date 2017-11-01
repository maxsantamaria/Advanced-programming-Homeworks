import time
from math import cos, sin, radians
from threading import Thread, Condition, Lock
from random import random, randint, choice
import numpy


class Character:
    def __init__(self, parent, x, y, tamaño=1):
        self.parent = parent
        self._x = x
        self._y = y
        self.image = None
        self._rotation = 0
        self.tamaño = tamaño
        self.velocidad = 0
        self.i = 9

    def avanzar2(self, QKeyEvent):
        if QKeyEvent.text() == "w":
            # time.sleep(0.05)  # para ajustar velocidad
            self.x -= cos(radians(self.rotation))
            self.y -= sin(radians(self.rotation))
        elif QKeyEvent.text() == "s":
            self.x += cos(radians(self.rotation))
            self.y += sin(radians(self.rotation))

    @property
    def centro(self):
        self._centro = (self.x + self.image.width() / 2,
                        self.y + self.image.height() / 2)
        return self._centro

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value == 360 or value == -360:
            self._rotation = 0
        else:
            self._rotation = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, posicion):  # colision borde izq y der
        if posicion < 0:
            self._x = 0
        elif posicion + self.image.width() > 1000:
            self._x = 1000 - self.image.width()
        else:
            self._x = posicion

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, posicion):  # colision borde arr y aba
        if posicion < 0:
            self._y = 0
        elif posicion + self.image.height() > 600:
            self._y = 600 - self.image.height()  # 450
        else:
            self._y = posicion

class Enemy(Thread):
    def __init__(self, parent, x, y, tamaño=10):
        super().__init__()
        self.parent = parent
        self.trigger = parent.threads_response3
        self.victima = parent.jug_principal
        self.image = None
        self._x = x
        self._y = y
        self._rotation = randint(0, 359)
        self.tamaño = tamaño
        self.velocidad = 0
        self._rango_vision = None
        self._rango_escape = None
        self._centro = None
        self.paused = False
        self.state = Condition(Lock())

    @property
    def centro(self):
        self._centro = (self.x + self.image.width() / 2,
                        self.y + self.image.height() / 2)
        return self._centro

    @property
    def rango_vision(self):
        self._rango_vision = self.tamaño * 30
        return self._rango_vision

    @property
    def rango_escape(self):
        self._rango_escape = self.rango_vision * 1.5
        return self._rango_escape

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value == 360 or value == -360:
            self._rotation = 0
        else:
            self._rotation = value

    def avanzar(self):
        # time.sleep(1)  # para ajustar velocidad
        self.x -= cos(radians(self.rotation))
        self.y -= sin(radians(self.rotation))
        self.trigger.emit(self)

    def escape(self):  # INTELIGENCIA
        time.sleep(0.1)
        a = numpy.array(self.victima.centro)
        b = numpy.array(self.centro)
        norma = numpy.linalg.norm(b - a)
        v = (b - a) / norma  # se normaliza
        if v[1] >= 0:
            self.rotation = - 90 - numpy.degrees(numpy.arcsin(v[0]))
        else:
            self.rotation = 90 + numpy.degrees(numpy.arcsin(v[0]))
        self.avanzar()

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()
            # time.sleep(0.1)
            #print(self.centro, self.victima.centro )
            #print("DISTANCE", euclidean_distance(self.centro, self.victima.centro),
            #      "\nRANGO", self.rango_vision)
            if euclidean_distance(self.centro,
                                  self.victima.centro) < self.rango_vision:
                #print("Esta escapando!!")
                self.esta_escapando = True
                self.escape()
            else:
                self.esta_escapando = False
                now = time.time()
                while time.time() - now <= 1:
                    time.sleep(0.1)
                    self.avanzar()
                prob = random()
                if prob < 0.25:
                    self.rotation = randint(0, 360)

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, posicion):  # colision borde izq y der
        if posicion < 0:
            self._x = 0
        elif posicion + self.image.width() > 1000:
            self._x = 1000 - self.image.width()
        else:
            self._x = posicion

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, posicion):  # colision borde arr y aba
        if posicion < 0:
            self._y = 0
            self.rotation = 0
            if self.x == 0:
                self.rotation = choice([0, 180])
            elif self.x == 1000 - self.image.width():
                self.rotation = choice([90, -90])
        elif posicion + self.image.height() > 600:
            self._y = 600 - self.image.height()
            if self.x == 0:
                self.rotation = choice([90, -90])
            elif self.x == 1000 - self.image.width():
                self.rotation = choice([0, 180])

        else:
            self._y = posicion



def euclidean_distance(v1, v2):  # 2 tuplas
    x1 = v1[0]
    x2 = v2[0]
    y1 = v1[1]
    y2 = v2[1]
    a = numpy.array((x1, y1))
    b = numpy.array((x2, y2))
    dist = numpy.linalg.norm(a - b)
    return dist