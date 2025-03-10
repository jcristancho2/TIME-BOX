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

def ver_historial_completados(frame_contenido,cargar_datos,mostrar_tareas_dash):

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
