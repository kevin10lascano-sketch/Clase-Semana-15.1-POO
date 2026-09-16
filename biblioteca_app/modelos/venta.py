class Venta:
    def __init__(self, identificador, usuario_id, libro_codigo, fecha):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.libro_codigo = libro_codigo
        self.fecha = fecha

    @staticmethod
    def validar_texto(valor, campo):
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return valor.strip()

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        self._usuario_id = self.validar_texto(valor, "usuario")

    @property
    def libro_codigo(self):
        return self._libro_codigo

    @libro_codigo.setter
    def libro_codigo(self, valor):
        self._libro_codigo = self.validar_texto(valor, "libro")

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_texto(valor, "fecha")
