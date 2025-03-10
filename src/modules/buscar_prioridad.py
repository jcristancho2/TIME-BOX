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

def buscar_por_prioridad(frame_contenido,cargar_datos,mostrar_tareas_dash):
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
