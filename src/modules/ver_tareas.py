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

def ver_tareas(cargar_datos,frame_contenido,buscar_por_prioridad,abrir_ventana_exportacion,ver_historial_completados,mostrar_tareas_dash):
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
