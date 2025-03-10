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

def eliminar_tarea(cargar_datos,guardar_datos,mostrar_formulario,ver_tareas,frame_contenido,mostrar_tareas_dash):
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
