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

def anadir_tarea(cargar_datos,guardar_datos,mostrar_formulario,ver_tareas,frame_contenido,mostrar_tareas_dash):
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