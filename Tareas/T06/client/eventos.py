class ActualizarImagenEvent:
    def __init__(self, nombre, data, num_imagen):
        self.nombre = nombre
        self.data = data
        self.num_imagen = num_imagen


class ImagenEditadaEvent:
    def __init__(self, nombre, new_idat_info):
        self.nombre = nombre
        self.new_idat_info = new_idat_info


class CambioUsuariosEvent:
    def __init__(self, nombre_usuario, entra):  # ENTRA: BOOL
        self.nombre_usuario = nombre_usuario
        self.entra = entra