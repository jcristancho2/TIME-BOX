import tkinter as tk  # Librería para crear interfaces gráficas
from tkinter import ttk, messagebox  # Widgets avanzados y mensajes emergentes
from PIL import Image, ImageTk  # Manejo de imágenes con Pillow
import json  # Manejo de archivos JSON para almacenar usuarios
import os  # Interacción con el sistema operativo (verificar archivos)
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
from datetime import datetime
import requests
import threading


DATA_FOLDER = "data"
USUARIOS_FILE = os.path.join(DATA_FOLDER, "usuarios.json")
CODIGO_SECRETO = "0626"  # Código para nuevos registros

API_KEY = "4239470"  # API de CallMeBot
NUMERO_DESTINO = "573012712009"  # Número de destino en formato internacional
MINUTOS_ANTES = 2  # Cuántos minutos antes del evento quieres recibir la notificación

# Asegurar que la carpeta "data" exista
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Función para cargar usuarios desde JSON
def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Función para guardar usuarios en JSON
def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)

def login(): 
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    
    usuarios = cargar_usuarios()

    if usuario in usuarios and usuarios[usuario] == clave:
        root.destroy() 
        mostrar_pantalla_principal()
    else:
        messagebox.showerror("Error", "Usuario no encontrado. Contacte con el administrador.")

def recuperar_contrasena():
    def cambiar_contrasena():
        usuario = entry_usuario_rec.get()
        nueva_clave = entry_nueva_clave.get()
        codigo_ingresado = entry_codigo_rec.get()

        usuarios = cargar_usuarios()

        if usuario not in usuarios:
            messagebox.showerror("Error", "El usuario no existe.")
            return

        if codigo_ingresado != CODIGO_SECRETO:
            messagebox.showerror("Error", "Código secreto incorrecto.")
            return

        usuarios[usuario] = nueva_clave
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
        ventana_recuperar.destroy()

    ventana_recuperar = tk.Toplevel(root)
    ventana_recuperar.title("Recuperar Contraseña")
    ventana_recuperar.geometry("300x220")
    ventana_recuperar.resizable(False, False)

    tk.Label(ventana_recuperar, text="Usuario:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_usuario_rec = ttk.Entry(ventana_recuperar, width=30)
    entry_usuario_rec.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_recuperar, text="Nueva Contraseña:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nueva_clave = ttk.Entry(ventana_recuperar, width=30, show="*")
    entry_nueva_clave.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_recuperar, text="Código Secreto:", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_codigo_rec = ttk.Entry(ventana_recuperar, width=30, show="*")
    entry_codigo_rec.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(ventana_recuperar, text="Cambiar Contraseña", command=cambiar_contrasena).grid(row=3, column=0, columnspan=2, pady=10)

def registrar_usuario():
    def guardar_usuario():
        usuario = entry_usuario_reg.get()
        clave = entry_clave_reg.get()
        codigo_ingresado = entry_codigo_reg.get()

        if codigo_ingresado != CODIGO_SECRETO:
            messagebox.showerror("Error", "Código de registro incorrecto.")
            return

        usuarios = cargar_usuarios()
        if usuario in usuarios:
            messagebox.showerror("Error", "El usuario ya existe.")
            return

        usuarios[usuario] = clave
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        ventana_registro.destroy()

    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("300x220")
    ventana_registro.resizable(False, False)

    tk.Label(ventana_registro, text="Usuario:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_usuario_reg = ttk.Entry(ventana_registro, width=30)
    entry_usuario_reg.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_registro, text="Contraseña:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_clave_reg = ttk.Entry(ventana_registro, width=30, show="*")
    entry_clave_reg.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_registro, text="Código de Registro:", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_codigo_reg = ttk.Entry(ventana_registro, width=30, show="*")
    entry_codigo_reg.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(ventana_registro, text="Registrar", command=guardar_usuario).grid(row=3, column=0, columnspan=2, pady=10)

def mostrar_pantalla_principal():
    global root, frame_contenido, frame_menu, label_bienvenida, tema_claro
# Archivo de la base de datos
    DB_FILE = "data/timebox.json"

    # Asegurar que la carpeta "data" exista
    if not os.path.exists("data"):
        os.makedirs("data")

    # Verificar si el archivo JSON existe, si no, crearlo
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump({"Evento": [], "Task": []}, file, indent=4)

    # Función para cargar datos desde JSON
    def cargar_datos():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"Evento": [], "Task": []}

    # Función para guardar datos en JSON
    def guardar_datos(data):
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    # Función para actualizar la pantalla principal con nuevos formularios
    def mostrar_formulario(funcion):
        for widget in frame_contenido.winfo_children():
            widget.destroy()  # Limpiar el contenido antes de mostrar algo nuevo
        funcion()

    def cambiar_tema():
        global tema_claro, root, frame_contenido, label_bienvenida, frame_menu
        global tema_claro
        tema_claro = not tema_claro
        nuevo_bg = "#333" if not tema_claro else "#f4f4f4"
        nuevo_fg = "white" if not tema_claro else "black"
        root.configure(bg=nuevo_bg)
        frame_contenido.configure(bg=nuevo_bg)
        label_bienvenida.configure(bg=nuevo_bg, fg=nuevo_fg)
        for widget in frame_menu.winfo_children():
            widget.configure(style="Dark.TButton" if not tema_claro else "Light.TButton")

            
    # Función para añadir tarea dentro del área principal
    def anadir_tarea():
        def guardar():
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get()
            fecha = entry_fecha.get()
            prioridad = combo_prioridad.get()
            estado = combo_estado.get()
            
            if not nombre or not fecha or not prioridad or not estado:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            datos = cargar_datos()
            nueva_tarea = {
                "nombre": nombre,
                "descripcion": descripcion,
                "fecha_vencimiento": fecha,
                "prioridad": prioridad,
                "estado": estado
            }

            categoria = "Evento" if var_tipo.get() == 1 else "Task"
            datos[categoria].append(nueva_tarea)
            guardar_datos(datos)

            messagebox.showinfo("Éxito", "Tarea añadida correctamente")
            mostrar_formulario(ver_tareas)  # Actualizar vista después de añadir

        tk.Label(frame_contenido, text="Añadir Nueva Tarea", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(frame_contenido, text="Nombre:").pack()
        entry_nombre = ttk.Entry(frame_contenido, width=40)
        entry_nombre.pack()

        tk.Label(frame_contenido, text="Descripción:").pack()
        entry_descripcion = ttk.Entry(frame_contenido, width=40)
        entry_descripcion.pack()

        tk.Label(frame_contenido, text="Fecha (YYYY-MM-DD HH:MM):").pack()
        entry_fecha = ttk.Entry(frame_contenido, width=40)
        entry_fecha.pack()

        tk.Label(frame_contenido, text="Prioridad:").pack()
        combo_prioridad = ttk.Combobox(frame_contenido, values=["Alta", "Media", "Baja"], width=37)
        combo_prioridad.pack()

        tk.Label(frame_contenido, text="Estado:").pack()
        combo_estado = ttk.Combobox(frame_contenido, values=["Pendiente","En proceso", "Completada"], width=37)
        combo_estado.pack()

        var_tipo = tk.IntVar(value=1)
        tk.Radiobutton(frame_contenido, text="Evento", variable=var_tipo, value=1).pack()
        tk.Radiobutton(frame_contenido, text="Task", variable=var_tipo, value=2).pack()

        ttk.Button(frame_contenido, text="Guardar", command=guardar).pack(pady=10)
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)


    # Función para eliminar tarea dentro del área principal
    def eliminar_tarea():
        datos = cargar_datos()

        if not datos["Evento"] and not datos["Task"]:
            messagebox.showinfo("Información", "No hay tareas registradas.")
            return

        def eliminar():
            categoria = combo_categoria.get()
            tarea = combo_tarea.get()
            if not categoria or not tarea:
                messagebox.showerror("Error", "Debe seleccionar una tarea")
                return

            datos[categoria] = [t for t in datos[categoria] if t["nombre"] != tarea]
            guardar_datos(datos)
            messagebox.showinfo("Éxito", "Tarea eliminada correctamente")
            mostrar_formulario(ver_tareas)  # Actualizar vista después de eliminar

        tk.Label(frame_contenido, text="Eliminar Tarea", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(frame_contenido, text="Seleccione una categoría:").pack()
        combo_categoria = ttk.Combobox(frame_contenido, values=["Evento", "Task"], width=30)
        combo_categoria.pack()
        
        tk.Label(frame_contenido, text="Seleccione una tarea:").pack()
        combo_tarea = ttk.Combobox(frame_contenido, values=[], width=30)
        combo_tarea.pack()

        def actualizar_tareas(event):
            categoria = combo_categoria.get()
            combo_tarea["values"] = [t["nombre"] for t in datos[categoria]]

        combo_categoria.bind("<<ComboboxSelected>>", actualizar_tareas)

        ttk.Button(frame_contenido, text="Eliminar", command=eliminar).pack(pady=10)
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)

    # Función para actualizar el estado de una tarea
    def cambiar_estado(categoria, nombre):
        datos = cargar_datos()

        for tarea in datos[categoria]:
            if tarea["nombre"] == nombre:
                if tarea["estado"] == "Pendiente":
                    tarea["estado"] = "En proceso"
                elif tarea["estado"] == "En proceso":
                    tarea["estado"] = "Completada"
                else:
                    tarea["estado"] = "Pendiente"
                break

        guardar_datos(datos)
        mostrar_tareas_dash()  # Recargar la tabla después de actualizar

    def enviar_whatsapp(numero, mensaje, apikey):
        """
        Envía un mensaje de WhatsApp utilizando la API de CallMeBot.
        """
        url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={mensaje}&apikey={apikey}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Mensaje enviado correctamente.")
            else:
                print(f"❌ Error al enviar mensaje. Código: {response.status_code}")
        except Exception as e:
            print(f"❌ Excepción al enviar mensaje: {e}")

    def programar_notificacion(nombre, fecha_evento, tipo="Recordatorio"):
        """
        Programa una notificación para un evento a través de WhatsApp.
        La notificación se enviará MINUTOS_ANTES minutos antes de la fecha_evento.
        El tipo de notificación puede ser 'Recordatorio' o 'Tarea'.
        """
        def tarea():
            try:
                # Convertir la fecha y hora de la cadena en un objeto datetime
                fecha_obj = datetime.strptime(fecha_evento, "%Y-%m-%d %H:%M")
                tiempo_espera = (fecha_obj - datetime.now()).total_seconds() - (MINUTOS_ANTES * 60)
                
                # Si el tiempo de espera es negativo, significa que la fecha ya pasó
                if tiempo_espera <= 0:
                    print("❌ La fecha ya pasó. No se enviará la notificación.")
                    return

                print(f"⌛ Notificación programada para {fecha_obj.strftime('%Y-%m-%d %H:%M')}...")
                time.sleep(tiempo_espera)

                # El mensaje cambia dependiendo del tipo
                if tipo == "Tarea":
                    mensaje = f"📝 ¡Recordatorio! Tienes una tarea pendiente: {nombre}. ¡Hazlo pronto!"
                else:  # Tipo "Recordatorio" por defecto
                    mensaje = f"🎯 ¡Hola! Solo un recordatorio de que {nombre} está por empezar. ¡Mucho éxito!"

                # Enviar el mensaje por WhatsApp
                enviar_whatsapp(NUMERO_DESTINO, mensaje, API_KEY)

            except ValueError:
                print("❌ Error: El formato de fecha no es válido. Usa 'YYYY-MM-DD HH:MM'.")

        # Se ejecuta en segundo plano sin bloquear el código principal
        threading.Thread(target=tarea, daemon=True).start()


    # Función para ver todas las tareas
    def ver_tareas():
        datos = cargar_datos()
        
        tk.Label(frame_contenido, text="Lista de Tareas", font=("Arial", 16, "bold")).pack(pady=10)

        for categoria, tareas in datos.items():
            tk.Label(frame_contenido, text=f"{categoria}:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
            for tarea in tareas:
                tk.Label(frame_contenido, text=f"- {tarea['nombre']} | {tarea['fecha_vencimiento']} | {tarea['estado']}", font=("Arial", 10)).pack(anchor="w", padx=40)
                
        ttk.Button(frame_contenido, text="historial completas", command=ver_historial_completados).pack(pady=10)
        ttk.Button(frame_contenido, text="prioridad", command=buscar_por_prioridad).pack(pady=10)
        ttk.Button(frame_contenido, text="Exportar", command=abrir_ventana_exportacion).pack(pady=10)
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)

    def buscar_por_prioridad():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        tk.Label(frame_contenido, text="🔍 Buscar Tareas por Prioridad", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(frame_contenido, text="Seleccione Prioridad:").pack()
        combo_prioridad = ttk.Combobox(frame_contenido, values=["Alta", "Media", "Baja"], width=30)
        combo_prioridad.pack()

        frame_tabla = tk.Frame(frame_contenido)
        frame_tabla.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Fecha", "Estado"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Estado", text="Estado")
        tree.pack(fill="both", expand=True)

        def cargar_tareas():
            prioridad_filtro = combo_prioridad.get()
            tree.delete(*tree.get_children())
            datos = cargar_datos()
            for categoria, tareas in datos.items():
                for tarea in tareas:
                    if tarea.get("prioridad") == prioridad_filtro:
                        tree.insert("", "end", values=(tarea["nombre"], tarea["fecha_vencimiento"], tarea["estado"]))
        
        combo_prioridad.bind("<<ComboboxSelected>>", lambda event: cargar_tareas())
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)

    def editar_tarea():
        datos = cargar_datos()

        if not datos["Evento"] and not datos["Task"]:
            messagebox.showinfo("Información", "No hay tareas registradas.")
            return

        def guardar_edicion():
            categoria = combo_categoria.get()
            tarea = combo_tarea.get()
            nuevo_nombre = entry_nombre.get()
            nueva_fecha = entry_fecha.get()
            nuevo_estado = combo_estado.get()

            if not categoria or not tarea or not nuevo_nombre or not nueva_fecha or not nuevo_estado:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            for t in datos[categoria]:
                if t["nombre"] == tarea:
                    t["nombre"] = nuevo_nombre
                    t["fecha_vencimiento"] = nueva_fecha
                    t["estado"] = nuevo_estado
                    break

            guardar_datos(datos)
            messagebox.showinfo("Éxito", "Tarea editada correctamente")
            mostrar_formulario(ver_tareas)

        tk.Label(frame_contenido, text="Modificar Tarea", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(frame_contenido, text="Seleccione una categoría:").pack()
        combo_categoria = ttk.Combobox(frame_contenido, values=["Evento", "Task"], width=30)
        combo_categoria.pack()

        tk.Label(frame_contenido, text="Seleccione una tarea:").pack()
        combo_tarea = ttk.Combobox(frame_contenido, values=[], width=30)
        combo_tarea.pack()

        def actualizar_tareas(event):
            categoria = combo_categoria.get()
            combo_tarea["values"] = [t["nombre"] for t in datos[categoria]]

        combo_categoria.bind("<<ComboboxSelected>>", actualizar_tareas)

        tk.Label(frame_contenido, text="Nuevo Nombre:").pack()
        entry_nombre = ttk.Entry(frame_contenido, width=40)
        entry_nombre.pack()

        tk.Label(frame_contenido, text="Nueva Fecha (YYYY-MM-DD HH:MM):").pack()
        entry_fecha = ttk.Entry(frame_contenido, width=40)
        entry_fecha.pack()

        tk.Label(frame_contenido, text="Nuevo Estado:").pack()
        combo_estado = ttk.Combobox(frame_contenido, values=["Pendiente", "En progreso", "Completada"], width=37)
        combo_estado.pack()

        ttk.Button(frame_contenido, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)

    def mostrar_tareas_dash():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        tk.Label(frame_contenido, text="📌 Dashboard de Tareas", font=("Arial", 16, "bold")).pack(pady=10)

        # Filtro por categoría
        tk.Label(frame_contenido, text="Filtrar por categoría:").pack()
        combo_categoria = ttk.Combobox(frame_contenido, values=["Todas", "Evento", "Task"], width=30)
        combo_categoria.pack()
        combo_categoria.set("Todas")

        # Contenedor de tabla con scrollbar
        frame_tabla = tk.Frame(frame_contenido)
        frame_tabla.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
        tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Fecha", "Estado"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side="right", fill="y")

        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Estado", text="Estado")

        tree.column("Nombre", width=200)
        tree.column("Fecha", width=150)
        tree.column("Estado", width=100)

        tree.pack(fill="both", expand=True)

        datos = cargar_datos()

        # Función para cargar datos en la tabla
        def cargar_datos_tabla():
            tree.delete(*tree.get_children())  # Limpiar la tabla

            categoria_filtro = combo_categoria.get()

            for categoria, tareas in datos.items():
                if categoria_filtro != "Todas" and categoria != categoria_filtro:
                    continue

                tareas_ordenadas = sorted(tareas, key=lambda x: x["fecha_vencimiento"])

                for tarea in tareas_ordenadas:
                    estado_texto = (
                        "✅ Completada" if tarea["estado"] == "Completada" else
                        "🔄 En proceso" if tarea["estado"] == "En proceso" else
                        "❌ Pendiente"
                    )
                    tree.insert("", "end", values=(tarea["nombre"], tarea["fecha_vencimiento"], estado_texto))

        combo_categoria.bind("<<ComboboxSelected>>", lambda event: cargar_datos_tabla())
        cargar_datos_tabla()
        
        #Sección para agregar un botón para programar notificación
        tk.Label(frame_contenido, text="Programar Notificación de Evento o Tarea", font=("Arial", 12, "bold")).pack(pady=10)

        # Entrada para el nombre del evento o tarea
        tk.Label(frame_contenido, text="Nombre del Evento/Tarea:").pack()
        entry_nombre = tk.Entry(frame_contenido, width=30)
        entry_nombre.pack()

        # Entrada para la fecha del evento o tarea
        tk.Label(frame_contenido, text="Fecha (YYYY-MM-DD HH:MM):").pack()
        entry_fecha = tk.Entry(frame_contenido, width=30)
        entry_fecha.pack()

        # Opción para seleccionar el tipo de notificación
        tk.Label(frame_contenido, text="Tipo de Notificación:").pack()
        combo_tipo = ttk.Combobox(frame_contenido, values=["Recordatorio", "Tarea"], width=30)
        combo_tipo.pack()
        combo_tipo.set("Recordatorio")

        # Función para manejar el botón y programar la notificación
        def programar_notificacion_evento():
            nombre = entry_nombre.get()
            fecha = entry_fecha.get()
            tipo = combo_tipo.get()

            if nombre and fecha:
                # Llamar a la función programar_notificacion (asumiendo que ya la tienes definida)
                programar_notificacion(nombre, fecha, tipo)
            else:
                print("❌ Por favor, ingresa un nombre y una fecha válidos.")

        # Botón para programar la notificación
        btn_programar = ttk.Button(frame_contenido, text="Programar Notificación", command=programar_notificacion_evento)
        btn_programar.pack(pady=10)

    def ver_historial_completados():

        """Muestra solo las tareas y eventos que están en estado 'Completada'."""
        
        for widget in frame_contenido.winfo_children():
            widget.destroy()  # Limpiar la ventana antes de mostrar la tabla

        tk.Label(frame_contenido, text="✅ Historial de Tareas Completadas", font=("Arial", 16, "bold")).pack(pady=10)

        # Crear la tabla con scrollbar
        frame_tabla = tk.Frame(frame_contenido)
        frame_tabla.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
        tree = ttk.Treeview(frame_tabla, columns=("Categoría", "Nombre", "Fecha"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side="right", fill="y")

        tree.heading("Categoría", text="Categoría")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha", text="Fecha de Finalización")

        tree.column("Categoría", width=120)
        tree.column("Nombre", width=250)
        tree.column("Fecha", width=150)

        tree.pack(fill="both", expand=True)

        datos = cargar_datos()

        # 🚀 **LIMPIAR LA TABLA ANTES DE INSERTAR NUEVOS DATOS**
        tree.delete(*tree.get_children())

        completadas = []

        for categoria, tareas in datos.items():
            for tarea in tareas:
                if tarea.get("estado", "").strip().lower() == "completada":  # Solo mostrar "Completada"
                    completadas.append((categoria, tarea["nombre"], tarea.get("fecha_vencimiento", "Desconocida")))

        # Si no hay tareas completadas, mostrar un mensaje
        if not completadas:
            tk.Label(frame_contenido, text="📭 No hay tareas ni eventos completados.", font=("Arial", 12)).pack(pady=10)
            return

        # Insertar datos en la tabla
        for item in completadas:
            tree.insert("", "end", values=item)

        # Botón para regresar al menú principal
        ttk.Button(frame_contenido, text="Regresar", command=mostrar_tareas_dash).pack(pady=10)

    def export_to_csv():
        CSV_FILE = "tareas.csv"
        try:
            with open(DB_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Categoría", "Nombre", "Descripción", "Fecha Vencimiento", "Prioridad", "Estado"])

                for categoria, items in data.items():
                    for item in items:
                        writer.writerow([
                            categoria, 
                            item.get("nombre", ""), 
                            item.get("descripciontrabajo", item.get("descripcion", "")), 
                            item.get("fecha_vencimiento", ""), 
                            item.get("prioridad", ""), 
                            item.get("estado", "")
                        ])

            messagebox.showinfo("Exportación Exitosa", f"✅ CSV guardado como {CSV_FILE}")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al exportar CSV: {e}")

    def export_to_pdf():
        PDF_FILE = "tareas.pdf"
        try:
            with open(DB_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            c = canvas.Canvas(PDF_FILE, pagesize=letter)
            width, height = letter
            y = height - 50

            c.setFont("Helvetica-Bold", 16)
            c.drawString(180, y, "📋 Lista de Todas las Tareas")
            y -= 30
            c.setFont("Helvetica", 12)

            for categoria, items in data.items():
                c.drawString(50, y, f"📌 Categoría: {categoria}")
                y -= 20

                for item in items:
                    c.drawString(70, y, f"📝 Nombre: {item.get('nombre', 'No name')}")
                    c.drawString(70, y - 15, f"📌 Descripción: {item.get('descripciontrabajo', item.get('descripcion', '') )}")
                    c.drawString(70, y - 30, f"📅 Fecha Vencimiento: {item.get('fecha_vencimiento', '')}")
                    c.drawString(70, y - 45, f"⚡ Prioridad: {item.get('prioridad', '')}")
                    c.drawString(70, y - 60, f"📌 Estado: {item.get('estado', '')}")
                    y -= 80

                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y = height - 50

            c.save()
            messagebox.showinfo("Exportación Exitosa", f"✅ PDF guardado como {PDF_FILE}")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al exportar PDF: {e}")

    def abrir_ventana_exportacion():
        ventana = tk.Toplevel(root)
        ventana.title("Exportar Tareas")
        ventana.geometry("300x200")

        ttk.Label(ventana, text="📤 Exportar todas las tareas", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Button(ventana, text="⬇ Exportar a CSV", command=export_to_csv).pack(pady=5)
        ttk.Button(ventana, text="📄 Exportar a PDF", command=export_to_pdf).pack(pady=5)
        ttk.Button(ventana, text="❌ Cancelar", command=ventana.destroy).pack(pady=10)

    def salir():
        # Aquí colocas el código para salir de la aplicación
        print("Saliendo...")
        exit()  # Esto cerrará la aplicación

    # Crear ventana principal
    root = tk.Tk()
    root.title("TIME-BOX")
    root.geometry("1000x600")
    root.state("zoomed")  
    tema_claro = True
    
    style = ttk.Style()
    style.configure("Light.TButton", background="#ccc", foreground="black")
    style.configure("Dark.TButton", background="#666", foreground="white")

    # Crear el menú lateral
    frame_menu = tk.Frame(root, bg="#333", width=200)
    frame_menu.pack(side="left", fill="y")

    opciones = [
        ("Registrar Tarea", lambda: mostrar_formulario(anadir_tarea)),
        ("Modificar Tarea", lambda: mostrar_formulario(editar_tarea)), 
        ("Eliminar Tarea", lambda: mostrar_formulario(eliminar_tarea)),
        ("Ver Tareas", lambda: mostrar_formulario(ver_tareas)),
        ("Cambiar Tema", cambiar_tema),
        ("Salir", salir )
    ]

    for texto, funcion in opciones:
        btn = ttk.Button(frame_menu, text=texto, command=funcion, style="Light.TButton")
        btn.pack(fill="x", padx=20, pady=10)


    # Crear un área de trabajo principal
    frame_contenido = tk.Frame(root, bg="white")
    frame_contenido.pack(side="right", expand=True, fill="both")

    label_bienvenida = tk.Label(frame_contenido, text="Bienvenido a TIME-BOX", font=("Arial", 18, "bold"), bg="white", fg="black")
    label_bienvenida.pack(pady=20)

    mostrar_tareas_dash(frame_contenido)
    root.mainloop()


def manejar_opcion(opcion):
    if opcion == "Salir":
        confirmar_salida()
    else:
        messagebox.showinfo("Opción", f"Seleccionaste: {opcion}")

def confirmar_salida():
    respuesta = messagebox.askyesno("Confirmar salida", "¿Estás seguro de que deseas salir?")
    if respuesta:
        root.destroy()

def toggle_password():
    if entry_clave.cget("show") == "*":
        entry_clave.config(show="")
        btn_toggle.config(text="🙈")
    else:
        entry_clave.config(show="*")
        btn_toggle.config(text="👁")




root = tk.Tk()
root.title("Login - Gestión de Tareas")
root.geometry("800x400")
root.resizable(False, False)

frame_login = tk.Frame(root, bg="white")
frame_login.pack(expand=True, fill="both")

imagen_path = "image/image.png"  # Asegúrate de que la imagen esté en la misma carpeta
imagen = Image.open(imagen_path)
imagen = imagen.resize((300, 300))  # Ajusta el tamaño según sea necesario
imagen_tk = ImageTk.PhotoImage(imagen)

# Crear frame a la izquierda para la imagen
frame_izq = tk.Frame(frame_login, bg="white")
frame_izq.grid(row=0, column=0, padx=20, pady=50)

# Agregar la imagen al frame izquierdo
label_imagen = tk.Label(frame_izq, image=imagen_tk, bg="white")
label_imagen.pack()

# Mantener la referencia de la imagen
label_imagen.image = imagen_tk

frame_der = tk.Frame(frame_login, bg="white")
frame_der.grid(row=0, column=1, padx=50, pady=50)

tk.Label(frame_der, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_der, text="Usuario:", bg="white", anchor="w").grid(row=1, column=0, sticky="w")
entry_usuario = ttk.Entry(frame_der, width=30)
entry_usuario.grid(row=1, column=1, pady=5)

tk.Label(frame_der, text="Contraseña:", bg="white", anchor="w").grid(row=2, column=0, sticky="w")
frame_clave = tk.Frame(frame_der, bg="white")
frame_clave.grid(row=2, column=1)
entry_clave = ttk.Entry(frame_clave, width=27, show="*")
entry_clave.grid(row=0, column=0, pady=5)
btn_toggle = ttk.Button(frame_clave, text="👁", width=3, command=toggle_password)
btn_toggle.grid(row=0, column=1, padx=2)

# Crear un Frame para los botones
frame_botones = tk.Frame(frame_der, bg="white")
frame_botones.grid(row=4, column=0, columnspan=2, pady=10)

# Botón Iniciar Sesión
btn_login = ttk.Button(frame_botones, text="Iniciar Sesión", command=login)
btn_login.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Botón Salir
btn_salir = ttk.Button(frame_botones, text="Salir", command=root.destroy)
btn_salir.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Botón Recuperar Contraseña
btn_recuperar = ttk.Button(frame_botones, text="Recuperar Contraseña", command=recuperar_contrasena)
btn_recuperar.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Botón Registrarse
btn_registrarse = ttk.Button(frame_botones, text="Registrarse", command=registrar_usuario)
btn_registrarse.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Expande el frame para que ocupe el espacio
frame_botones.columnconfigure(0, weight=1)
frame_botones.columnconfigure(1, weight=1)


root.mainloop() 