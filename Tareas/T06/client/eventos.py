class ActualizarImagenEvent:
    def __init__(self, nombre, data, num_imagen, comentarios):
        self.nombre = nombre
        self.data = data
        self.num_imagen = num_imagen
        self.comentarios = comentarios


class ImagenEditadaEvent:
    def __init__(self, nombre, new_idat_info):
        self.nombre = nombre
        self.new_idat_info = new_idat_info


class CambioUsuariosEvent:
    def __init__(self, nombre_usuario, entra):  # ENTRA: BOOL
        self.nombre_usuario = nombre_usuario
        self.entra = entra


class CambiarBotonEditarEvent:
    def __init__(self, nombre, editable):  # editable es bool
        self.nombre = nombre
        self.editable = editable


class ActualizarComentarioEvent:
    def __init__(self, nombre, comentario):
        self.nombre = nombre  # de la imagen
        self.comentario = comentario