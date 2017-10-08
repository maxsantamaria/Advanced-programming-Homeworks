
class BadRequest(Exception):
    def __init__(self):
        super().__init__("Error: Bad Request. Consulta no válida.")


class NotFound(Exception):
    def __init__(self):
        super().__init__("Error: Not Found. Parámetros mal ingresados.")


class NotAcceptable(Exception):
    def __init__(self):
        super().__init__("Error: Not Acceptable."
                         " Resultado de consulta es vacío.")


class GenomeError(Exception):
    def __init__(self):
        super().__init__("Error: Genome Error. Error en genoma.")


def determinar_notacceptable(respuesta):
    if len(respuesta) == 0:
        raise NotAcceptable


def control_badrequest(func, args):  # func es un generador, args de funcion
    try:
        funcion_real = next(func)
    except StopIteration:
        raise BadRequest
    else:
        return funcion_real
