# Fundamentos de manejo de eventos con Tkinter

## Tema

Semana 15 y extension Semana 15.1: conceptos fundamentales de manejo de eventos en una aplicacion de biblioteca con Tkinter.

## Objetivo

Evolucionar el proyecto de la Semana 14 sin reconstruirlo desde cero. La aplicacion conserva el login, la arquitectura por capas, la persistencia JSON, la consulta de usuarios y el CRUD de libros. En la Semana 15 se agrega una operacion sencilla de venta para observar el flujo entre una accion del usuario, un boton con `command=`, un callback, el servicio, la persistencia y la respuesta visual.

La extension Semana 15.1 agrega la generacion de un reporte de ventas en PDF usando ReportLab. La informacion almacenada por una aplicacion puede reutilizarse para generar documentos automaticos como reportes, comprobantes o facturas simuladas.

## Continuidad desde Semana 14

La interfaz mantiene los mismos colores, estilos, iconos, menu lateral, barra de estado y organizacion general. La nueva seccion `Ventas` se integra como una capacidad adicional de la misma aplicacion.

## Nueva funcionalidad

La venta relaciona:

```text
Usuario + Libro + Fecha -> Venta
```

La seccion `Ventas` permite:

- seleccionar un usuario registrado con `ttk.Combobox`;
- seleccionar un libro registrado con `ttk.Combobox`;
- pulsar el boton `Registrar venta`;
- ejecutar el callback `registrar_venta()` mediante `command=`;
- guardar la venta en `datos/ventas.json`;
- mostrar las ventas registradas en un `ttk.Treeview`;
- pulsar el boton `Generar reporte PDF`;
- seleccionar donde guardar el archivo PDF.

Flujo educativo:

```text
Accion del usuario -> Boton -> command= -> callback -> servicio -> JSON -> Treeview actualizado
```

Flujo educativo del reporte:

```text
Datos de ventas -> Boton -> command= -> generar_reporte_ventas() -> ReporteServicio -> ReportLab -> PDF
```

## Semana 15.1 - Generacion de reportes PDF

ReportLab es una biblioteca de Python utilizada para crear documentos PDF mediante codigo.

La nueva responsabilidad queda aislada en:

```text
biblioteca_app/servicios/reporte_servicio.py
```

`ReporteServicio` recibe las ventas, usuarios y libros que ya estan cargados por `BibliotecaServicio`, organiza los datos y construye el documento PDF. La interfaz solamente valida que existan ventas, solicita la ruta con `filedialog.asksaveasfilename()` y muestra el resultado al usuario.

El reporte incluye:

- encabezado con el logo disponible en `assets/logo/logo.png`, si existe;
- nombre del sistema y titulo `Reporte de Ventas`;
- fecha y hora de generacion;
- total de ventas registradas;
- usuarios relacionados con ventas;
- libros diferentes vendidos;
- tabla con ID de venta, fecha, usuario, libro y codigo.

El modelo actual de venta no contiene precios, por eso el PDF no inventa montos. El reporte resume operaciones de venta registradas en el sistema.

Si no existen ventas, la aplicacion muestra un mensaje y no genera un PDF vacio.

## Estructura del proyecto

```text
biblioteca_app/
├── assets/
│   ├── icons/
│   │   ├── home.png
│   │   ├── users.png
│   │   ├── books.png
│   │   ├── sales.png        # opcional para la seccion Ventas
│   │   ├── logout.png
│   │   ├── add.png
│   │   ├── edit.png
│   │   ├── delete.png
│   │   ├── search.png
│   │   └── clean.png
│   └── logo/
│       ├── logo.png
│       └── icono.png
├── datos/
│   ├── libros.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── usuario.py
│   ├── libro.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   ├── biblioteca_servicio.py
│   └── reporte_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── requirements.txt
```

## Capas

`modelos/`: define las clases `Usuario`, `Libro` y `Venta`, con validaciones basicas para evitar campos vacios.

`servicios/`: contiene la logica de consulta, registro, actualizacion, eliminacion y persistencia. `BibliotecaServicio` tambien registra ventas. `ReporteServicio` genera el reporte PDF de ventas con ReportLab.

`datos/`: guarda la informacion persistente en archivos JSON.

`ui/`: contiene las vistas creadas con Tkinter.

`assets/icons/`: contiene iconos PNG usados por los botones. Si falta un icono, la aplicacion sigue funcionando con texto.

## Icono opcional de Ventas

Para el nuevo boton del menu lateral se espera opcionalmente este archivo:

```text
biblioteca_app/assets/icons/sales.png
```

No es obligatorio incluirlo. La funcion `cargar_icono()` devuelve `None` si no lo encuentra y el boton se muestra solo con texto.

## Pantallas principales

`LoginView`: pantalla de inicio de sesion.

`Inicio`: panel de resumen con usuarios, libros y ventas.

`Usuarios`: pantalla de consulta de usuarios registrados.

`Libros`: pantalla de gestion con formulario, botones y tabla para el CRUD basico.

`Ventas`: pantalla nueva para seleccionar un usuario, seleccionar un libro y registrar una venta simple.

## Componentes Tkinter utilizados

`Label`: textos y titulos.

`Entry`: campos de entrada para login y formulario de libros.

`ttk.Combobox`: selectores de usuario y libro en la vista de ventas.

`ttk.Button`: botones de navegacion y acciones con `command=`.

`ttk.Treeview`: tablas de usuarios, libros y ventas.

`ttk.Scrollbar`: barra de desplazamiento para las tablas.

`messagebox`: mensajes simples de confirmacion o error.

`filedialog`: seleccion de la ruta donde se guardara el reporte PDF.

## Persistencia

Los usuarios, libros y ventas se cargan desde JSON al iniciar la aplicacion.

```text
biblioteca_app/datos/usuarios.json
biblioteca_app/datos/libros.json
biblioteca_app/datos/ventas.json
```

Al registrar una venta, el servicio agrega el objeto a la coleccion en memoria, convierte las ventas a datos serializables y escribe `ventas.json`.

## Que NO se trabaja todavia

En Semana 15 no se utilizan eventos avanzados. No se implementa:

- `bind()`;
- doble clic;
- eventos de teclado;
- eventos de mouse;
- `<<TreeviewSelect>>`;
- carga automatica desde tablas;
- seleccion reactiva de filas.

Estos conceptos quedan para la siguiente semana de manejo de eventos.

## Como ejecutar

Desde la carpeta del proyecto:

```powershell
cd "C:\Users\Usuario\OneDrive\Documentos\Clase Semana 15.1 POO"
pip install -r requirements.txt
cd "biblioteca_app"
py main.py
```

Si `python` esta disponible:

```powershell
python main.py
```

Tambien se puede instalar directamente la dependencia principal:

```powershell
pip install reportlab
```

## Como generar el reporte

1. Inicie sesion con una cuenta de demostracion.
2. Entre en la seccion `Ventas`.
3. Registre al menos una venta seleccionando un usuario y un libro.
4. Pulse `Generar reporte PDF`.
5. Elija la carpeta y el nombre del archivo.
6. Abra el PDF generado para revisar el resumen.

El nombre sugerido sigue este formato:

```text
reporte_ventas_YYYYMMDD_HHMM.pdf
```

El reporte no es facturacion electronica ni comprobante tributario. Es un documento pedagogico para observar como una interfaz puede usar servicios adicionales sin mezclar responsabilidades.

## Credenciales de demostracion

Usuario: `admin`

Contrasena: `1234`

Tambien puede usarse:

Usuario: `docente`

Contrasena: `abcd`

## Nota educativa

El proyecto mantiene una implementacion sencilla para que el estudiante pueda seguir el crecimiento progresivo de la aplicacion:

```text
Semana 14: componentes y contenedores
Semana 15: accion -> command= -> callback -> servicio -> persistencia -> respuesta visual
Semana 15.1: datos -> callback -> servicio de reportes -> ReportLab -> PDF
```

La venta no representa todavia un sistema comercial completo. Solo muestra una relacion clara entre un usuario y un libro para estudiar los fundamentos del manejo de eventos mediante botones.
