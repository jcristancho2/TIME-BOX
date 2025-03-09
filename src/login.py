import tkinter as tk  # Librería para crear interfaces gráficas
from tkinter import ttk, messagebox  # Widgets avanzados y mensajes emergentes
from PIL import Image, ImageTk  # Manejo de imágenes con Pillow
import json  # Manejo de archivos JSON para almacenar usuarios
import os  # Interacción con el sistema operativo (verificar archivos)

# Archivo donde se guardan los usuarios
DATA_FOLDER = "data"
USUARIOS_FILE = os.path.join(DATA_FOLDER, "usuarios.json")
CODIGO_SECRETO = "0626"  # Código para nuevos registros

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
        frame_login.destroy()
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
    root.state("zoomed")  
    root.configure(bg="#f4f4f4")

    frame_menu = tk.Frame(root, bg="#333", width=200)
    frame_menu.pack(side="left", fill="y")

    opciones = ["Registrar tarea", "Modificar tarea", "Eliminar tarea", "Visualizar tareas", "Configuración de usuarios", "Salir"]

    for opcion in opciones:
        btn = ttk.Button(frame_menu, text=opcion, command=lambda op=opcion: manejar_opcion(op))
        btn.pack(fill="x", padx=10, pady=5)

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
