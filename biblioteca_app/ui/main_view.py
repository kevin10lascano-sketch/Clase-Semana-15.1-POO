import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from servicios.reporte_servicio import ReporteServicio


class MainView(tk.Frame):
    def __init__(self, master, biblioteca_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f7fafc")
        self.biblioteca_servicio = biblioteca_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        ruta_base = Path(__file__).resolve().parent.parent
        self.reporte_servicio = ReporteServicio(ruta_base / "assets" / "logo" / "logo.png")

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}
        self.logo_sidebar = None

        self.libro_codigo_entry = None
        self.libro_titulo_entry = None
        self.libro_autor_entry = None
        self.tabla_libros = None
        self.tabla_usuarios = None
        self.usuario_venta_combo = None
        self.libro_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_libros_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

    # -------------------------------------------------------------------------
    # Configuracion general: identidad visual heredada de Semana 14.
    # -------------------------------------------------------------------------
    def definir_estilos(self):
        self.color_fondo = "#f7fafc"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1f2a44"
        self.color_texto = "#243447"
        self.color_secundario = "#dbeafe"
        self.color_resaltado = "#2563eb"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background="#334155",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w",
        )
        estilo.map("MenuApp.TButton", background=[("active", "#475569")])
        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w",
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Secundario.TButton",
            background="#1f2a44",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#334155")])
        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Eliminar.TButton",
            background="#e11d48",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#be123c")])
        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )

    def cargar_icono(self, nombre_archivo):
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_icono = ruta_base / "assets" / "icons" / nombre_archivo

        if not ruta_icono.exists():
            return None

        icono = tk.PhotoImage(file=str(ruta_icono))
        self.iconos[nombre_archivo] = icono
        return icono

    def crear_boton(self, contenedor, texto, comando, estilo, icono=None):
        imagen = self.cargar_icono(icono) if icono else None

        if imagen is not None:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left",
            )
        else:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
            )

        return boton

    # -------------------------------------------------------------------------
    # Menu principal: conecta cada opcion con su pantalla correspondiente.
    # -------------------------------------------------------------------------
    def construir_interfaz(self):
        frame_sidebar = tk.Frame(self, bg=self.color_encabezado, width=190, padx=16, pady=18)
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        tk.Label(
            frame_sidebar,
            text="BIBLIOTECA",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            frame_sidebar,
            text=self.usuario_actual.nombre,
            bg=self.color_encabezado,
            fg="#dbeafe",
            font=("Arial", 10),
            wraplength=150,
            justify="left",
        ).pack(anchor="w", pady=(0, 24))

        self.crear_boton_menu(frame_sidebar, "Inicio", self.mostrar_inicio, "home.png")
        self.crear_boton_menu(frame_sidebar, "Usuarios", self.mostrar_usuarios, "users.png")
        self.crear_boton_menu(frame_sidebar, "Libros", self.mostrar_libros, "books.png")
        self.crear_boton_menu(frame_sidebar, "Ventas", self.mostrar_ventas, "sales.png")

        tk.Frame(frame_sidebar, bg=self.color_encabezado).pack(fill="both", expand=True)

        self.crear_boton(
            frame_sidebar,
            "Cerrar sesion",
            self.cerrar_sesion,
            "Eliminar.TButton",
            "logout.png",
        ).pack(fill="x", pady=(16, 0))

        frame_principal = tk.Frame(self, bg=self.color_fondo)
        frame_principal.pack(side="left", fill="both", expand=True)

        self.contenido = tk.Frame(frame_principal, bg=self.color_fondo, padx=28, pady=24)
        self.contenido.pack(fill="both", expand=True)

        barra_estado = tk.Frame(frame_principal, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")

        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono):
        boton = self.crear_boton(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(fill="x", pady=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            estilo = "MenuActivo.TButton" if texto == seccion else "MenuApp.TButton"
            boton.configure(style=estilo)

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None

        self.etiqueta_estado.config(
            text=(
                f"Libros: {self.biblioteca_servicio.cantidad_libros()} | "
                f"Usuarios: {self.biblioteca_servicio.cantidad_usuarios()} | "
                f"Ventas: {self.biblioteca_servicio.cantidad_ventas()} | "
                "Datos JSON locales"
            )
        )

    # -------------------------------------------------------------------------
    # Inicio: resumen general del sistema.
    # -------------------------------------------------------------------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido,
            text="Consulte usuarios, gestione libros y registre ventas desde el menu lateral.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")
        self.crear_tarjeta_resumen(resumen, "Usuarios registrados", self.biblioteca_servicio.cantidad_usuarios())
        self.crear_tarjeta_resumen(resumen, "Libros registrados", self.biblioteca_servicio.cantidad_libros())
        self.crear_tarjeta_resumen(resumen, "Ventas registradas", self.biblioteca_servicio.cantidad_ventas())

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # -------------------------------------------------------------------------
    # Usuarios: seccion de consulta trabajada antes de Semana 15.
    # -------------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Usuarios registrados")
        listado = self.crear_listado(self.contenido, "Consulta de usuarios")
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificador", "nombre", "usuario"),
            ("Identificador", "Nombre", "Usuario"),
        )
        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.biblioteca_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(usuario.identificador, usuario.nombre, usuario.usuario),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------------
    # Libros: seccion CRUD trabajada antes de Semana 15.
    # -------------------------------------------------------------------------
    def mostrar_libros(self):
        self.marcar_seccion("Libros")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de libros")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del libro",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.libro_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.libro_titulo_entry = self.crear_campo(formulario, "Titulo", 1)
        self.libro_autor_entry = self.crear_campo(formulario, "Autor", 2)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_libro, "Accion.TButton", "add.png"),
            ("Cargar por codigo", self.cargar_libro_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_libro, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_libro, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_libro, "Secundario.TButton", "clean.png"),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton(acciones, texto, comando, estilo, icono).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Libros registrados", usar_grid=True)
        self.tabla_libros = self.crear_tabla(
            listado,
            ("codigo", "titulo", "autor"),
            ("Codigo", "Titulo", "Autor"),
        )
        self.refrescar_libros()

    def obtener_datos_libro(self):
        assert self.libro_codigo_entry is not None
        assert self.libro_titulo_entry is not None
        assert self.libro_autor_entry is not None

        return (
            self.libro_codigo_entry.get(),
            self.libro_titulo_entry.get(),
            self.libro_autor_entry.get(),
        )

    def registrar_libro(self):
        try:
            self.biblioteca_servicio.registrar_libro(*self.obtener_datos_libro())
            self.limpiar_formulario_libro()
            self.refrescar_libros()
            messagebox.showinfo("Libros", "Libro registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Libros", str(error))

    def cargar_libro_en_formulario(self):
        assert self.libro_codigo_entry is not None
        assert self.libro_titulo_entry is not None
        assert self.libro_autor_entry is not None

        libro = self.biblioteca_servicio.buscar_libro_por_codigo(self.libro_codigo_entry.get())
        if libro is None:
            messagebox.showerror("Libros", "No existe un libro con ese codigo.")
            return

        self.limpiar_formulario_libro()
        self.libro_codigo_entry.insert(0, libro.codigo)
        self.libro_titulo_entry.insert(0, libro.titulo)
        self.libro_autor_entry.insert(0, libro.autor)

    def actualizar_libro(self):
        try:
            self.biblioteca_servicio.actualizar_libro(*self.obtener_datos_libro())
            self.refrescar_libros()
            messagebox.showinfo("Libros", "Libro actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Libros", str(error))

    def eliminar_libro(self):
        assert self.libro_codigo_entry is not None

        try:
            self.biblioteca_servicio.eliminar_libro(self.libro_codigo_entry.get())
            self.limpiar_formulario_libro()
            self.refrescar_libros()
            messagebox.showinfo("Libros", "Libro eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Libros", str(error))

    def limpiar_formulario_libro(self):
        for entrada in (self.libro_codigo_entry, self.libro_titulo_entry, self.libro_autor_entry):
            assert entrada is not None
            entrada.delete(0, tk.END)

    def refrescar_libros(self):
        assert self.tabla_libros is not None

        self.limpiar_tabla(self.tabla_libros)
        for libro in self.biblioteca_servicio.listar_libros():
            self.tabla_libros.insert("", tk.END, values=(libro.codigo, libro.titulo, libro.autor))

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------------
    # Ventas: seccion nueva de Semana 15 para estudiar command= y callbacks.
    # -------------------------------------------------------------------------
    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Registrar venta",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_venta_combo = self.crear_selector_venta(
            formulario,
            "Usuario",
            0,
            self.obtener_opciones_usuarios_venta(),
        )
        self.libro_venta_combo = self.crear_selector_venta(
            formulario,
            "Libro",
            1,
            self.obtener_opciones_libros_venta(),
        )

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # El boton usa command= para ejecutar este callback al hacer clic.
        self.crear_boton(
            acciones,
            "Registrar venta",
            self.registrar_venta,
            "Accion.TButton",
            "add.png",
        ).pack(fill="x", pady=(0, 7))

        self.crear_boton(
            acciones,
            "Generar reporte PDF",
            self.generar_reporte_ventas,
            "Secundario.TButton",
            "sales.png",
        ).pack(fill="x")

        listado = self.crear_listado(cuerpo, "Ventas registradas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(
            listado,
            ("identificador", "usuario", "libro", "fecha"),
            ("Venta", "Usuario", "Libro", "Fecha"),
        )
        self.refrescar_ventas()

    def crear_selector_venta(self, contenedor, etiqueta, fila, opciones):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        selector = ttk.Combobox(contenedor, values=list(opciones.keys()), state="readonly", width=34)
        selector.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return selector

    def obtener_opciones_usuarios_venta(self):
        self.opciones_usuarios_venta = {
            f"{usuario.identificador} - {usuario.nombre}": usuario.identificador
            for usuario in self.biblioteca_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_libros_venta(self):
        self.opciones_libros_venta = {
            f"{libro.codigo} - {libro.titulo}": libro.codigo
            for libro in self.biblioteca_servicio.listar_libros()
        }
        return self.opciones_libros_venta

    def registrar_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.libro_venta_combo is not None

        usuario_id = self.opciones_usuarios_venta.get(self.usuario_venta_combo.get(), "")
        libro_codigo = self.opciones_libros_venta.get(self.libro_venta_combo.get(), "")

        try:
            # Relaciona el usuario y el libro seleccionados antes de registrar la venta.
            self.biblioteca_servicio.registrar_venta(usuario_id, libro_codigo)
            self.limpiar_formulario_venta()
            self.refrescar_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Ventas", str(error))

    def generar_reporte_ventas(self):
        ventas = self.biblioteca_servicio.listar_ventas()
        if not ventas:
            messagebox.showinfo("Ventas", "No existen ventas registradas para generar el reporte.")
            return

        nombre_archivo = datetime.now().strftime("reporte_ventas_%Y%m%d_%H%M.pdf")
        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar reporte de ventas",
            defaultextension=".pdf",
            filetypes=(("Archivos PDF", "*.pdf"),),
            initialfile=nombre_archivo,
        )

        if not ruta_salida:
            return

        try:
            # La interfaz solicita la ruta; el servicio construye el PDF.
            ruta_generada = self.reporte_servicio.generar_reporte_ventas(
                ruta_salida,
                ventas,
                self.biblioteca_servicio.listar_usuarios(),
                self.biblioteca_servicio.listar_libros(),
            )
            messagebox.showinfo("Ventas", f"Reporte generado correctamente.\n{ruta_generada}")
        except ImportError:
            messagebox.showerror(
                "Ventas",
                "No fue posible generar el reporte. Instale ReportLab con: pip install reportlab",
            )
        except Exception:
            messagebox.showerror("Ventas", "No fue posible generar el reporte.")

    def limpiar_formulario_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.libro_venta_combo is not None

        self.usuario_venta_combo.set("")
        self.libro_venta_combo.set("")

    def refrescar_ventas(self):
        assert self.tabla_ventas is not None

        self.limpiar_tabla(self.tabla_ventas)
        for venta in self.biblioteca_servicio.listar_ventas():
            usuario = self.biblioteca_servicio.buscar_usuario_por_identificador(venta.usuario_id)
            libro = self.biblioteca_servicio.buscar_libro_por_codigo(venta.libro_codigo)
            texto_usuario = venta.usuario_id if usuario is None else f"{usuario.identificador} - {usuario.nombre}"
            texto_libro = venta.libro_codigo if libro is None else f"{libro.codigo} - {libro.titulo}"
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(venta.identificador, texto_usuario, texto_libro, venta.fecha),
            )

        # Refresca la tabla para mostrar la respuesta de la aplicacion.
        self.actualizar_barra_estado()

    # -------------------------------------------------------------------------
    # Utilidades de interfaz compartidas por las vistas.
    # -------------------------------------------------------------------------
    def crear_titulo_seccion(self, texto):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 16))

    def crear_campo(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        entrada = tk.Entry(contenedor, width=28, font=("Arial", 10))
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)

        return listado

    def crear_tabla(self, contenedor, columnas, encabezados):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=150, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
