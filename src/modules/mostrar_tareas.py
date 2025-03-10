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


def mostrar_tareas_dash(frame_contenido,cargar_datos):
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
