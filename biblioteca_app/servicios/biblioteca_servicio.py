from datetime import date

from modelos.libro import Libro
from modelos.usuario import Usuario
from modelos.venta import Venta


class BibliotecaServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.libros = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        libros_json = self.archivo_servicio.leer_json("libros.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
            )
            for datos in usuarios_json
        ]

        self.libros = [
            Libro(
                datos.get("codigo", ""),
                datos.get("titulo", ""),
                datos.get("autor", ""),
            )
            for datos in libros_json
        ]

        # Semana 15: carga las ventas persistidas para mostrarlas en la interfaz.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("libro_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        # Verifica si las credenciales coinciden con un usuario cargado.
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado

        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_libros(self):
        return len(self.libros)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        # Entrega los usuarios cargados para mostrarlos en la interfaz.
        return self.usuarios

    def listar_libros(self):
        # Entrega los libros cargados para mostrarlos en la interfaz.
        return self.libros

    def listar_ventas(self):
        # Entrega las ventas cargadas para mostrarlas en la interfaz.
        return self.ventas

    def guardar_libros(self):
        datos = [
            {
                "codigo": libro.codigo,
                "titulo": libro.titulo,
                "autor": libro.autor,
            }
            for libro in self.libros
        ]
        self.archivo_servicio.escribir_json("libros.json", datos)

    def buscar_libro_por_codigo(self, codigo):
        codigo = codigo.strip()
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro
        return None

    def buscar_usuario_por_identificador(self, identificador):
        identificador = identificador.strip()
        for usuario in self.usuarios:
            if usuario.identificador == identificador:
                return usuario
        return None

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_libro(self, codigo, titulo, autor):
        nuevo_libro = Libro(codigo, titulo, autor)

        if self.buscar_libro_por_codigo(nuevo_libro.codigo) is not None:
            raise ValueError("Ya existe un libro con ese codigo.")

        self.libros.append(nuevo_libro)
        self.guardar_libros()
        return nuevo_libro

    def actualizar_libro(self, codigo, titulo, autor):
        libro_actual = self.buscar_libro_por_codigo(codigo)

        if libro_actual is None:
            raise ValueError("No existe un libro con ese codigo.")

        datos_validados = Libro(codigo, titulo, autor)
        libro_actual.titulo = datos_validados.titulo
        libro_actual.autor = datos_validados.autor
        self.guardar_libros()
        return libro_actual

    def eliminar_libro(self, codigo):
        libro_actual = self.buscar_libro_por_codigo(codigo)

        if libro_actual is None:
            raise ValueError("No existe un libro con ese codigo.")

        self.libros.remove(libro_actual)
        self.guardar_libros()
        return libro_actual

    def guardar_ventas(self):
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "libro_codigo": venta.libro_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def registrar_venta(self, usuario_id, libro_codigo):
        usuario_id = usuario_id.strip()
        libro_codigo = libro_codigo.strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not libro_codigo:
            raise ValueError("Debe seleccionar un libro.")
        if self.buscar_usuario_por_identificador(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        if self.buscar_libro_por_codigo(libro_codigo) is None:
            raise ValueError("El libro seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            libro_codigo,
            date.today().isoformat(),
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta
