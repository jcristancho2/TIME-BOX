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
