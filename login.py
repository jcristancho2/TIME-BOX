import tkinter as tk  # Librería para crear interfaces gráficas
from tkinter import ttk, messagebox  # Widgets avanzados y mensajes emergentes
from PIL import Image, ImageTk  # Manejo de imágenes con Pillow
import json  # Manejo de archivos JSON para almacenar usuarios
import os  # Interacción con el sistema operativo (verificar archivos)


USUARIOS_FILE = "usuarios.json" 
CODIGO_SECRETO = "0626" # CODIGO DE ACCESO PARA NUEVOS USUARIOS


def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r") as file:
            return json.load(file)
    return {}


def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as file:
        json.dump(usuarios, file, indent=4)


def login():
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    
    usuarios = cargar_usuarios()

    if usuario in usuarios and usuarios[usuario] == clave:
        frame_login.destroy()
        mostrar_pantalla_principal()
    else:
        messagebox.showerror("Error", "Usuario no encontrado. Contacte con el administrador.")

def ventana_registro():
    def registrar_usuario():
        usuario_nuevo = entry_usuario_nuevo.get()
        clave_nueva = entry_clave_nueva.get()
        telefono = entry_telefono.get()
        codigo_ingresado = entry_codigo.get()
        
        if not usuario_nuevo or not clave_nueva or not codigo_ingresado or not telefono:
            messagebox.showwarning("Aviso", "Debe completar todos los campos.")
            return
        
        if codigo_ingresado != CODIGO_SECRETO:
            messagebox.showerror("Error", "Código secreto incorrecto.")
            return

        usuarios = cargar_usuarios()
        
        if usuario_nuevo in usuarios:
            messagebox.showwarning("Aviso", "El usuario ya existe.")
        else:
            usuarios[usuario_nuevo] = (clave_nueva)
            guardar_usuarios(usuarios)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana_registro.destroy()

    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrar Usuario")
    ventana_registro.geometry("300x300")
    ventana_registro.resizable(False, False)

    tk.Label(ventana_registro, text="Usuario Nuevo:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_usuario_nuevo = ttk.Entry(ventana_registro, width=30)
    entry_usuario_nuevo.pack(padx=10, pady=5)

    tk.Label(ventana_registro, text="Teléfono:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_telefono = ttk.Entry(ventana_registro, width=30)
    entry_telefono.pack(padx=10, pady=5)

    tk.Label(ventana_registro, text="Contraseña:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_clave_nueva = ttk.Entry(ventana_registro, width=30, show="*")
    entry_clave_nueva.pack(padx=10, pady=5)

    tk.Label(ventana_registro, text="Código Secreto:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_codigo = ttk.Entry(ventana_registro, width=30, show="*")
    entry_codigo.pack(padx=10, pady=5)

    ttk.Button(ventana_registro, text="Registrar", command=registrar_usuario).pack(pady=10)
    
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
    ventana_recuperar.geometry("300x300")
    ventana_recuperar.resizable(False, False)

    tk.Label(ventana_recuperar, text="Usuario:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_usuario_rec = ttk.Entry(ventana_recuperar, width=30)
    entry_usuario_rec.pack(padx=10, pady=5)

    tk.Label(ventana_recuperar, text="Nueva Contraseña:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_nueva_clave = ttk.Entry(ventana_recuperar, width=30, show="*")
    entry_nueva_clave.pack(padx=10, pady=5)

    tk.Label(ventana_recuperar, text="Código Secreto:", anchor="w").pack(fill="x", padx=10, pady=5)
    entry_codigo_rec = ttk.Entry(ventana_recuperar, width=30, show="*")
    entry_codigo_rec.pack(padx=10, pady=5)

    ttk.Button(ventana_recuperar, text="Cambiar Contraseña", command=cambiar_contrasena).pack(pady=10)
    

# ======= FUNCIÓN PARA MOSTRAR PANTALLA PRINCIPAL =======(MODIFICAR PARA MENU)
def mostrar_pantalla_principal():
    root.state("zoomed")  
    root.configure(bg="#f4f4f4")

    label_bienvenida = tk.Label(root, text="Bienvenido a TIME-BOX", font=("Arial", 16, "bold"), bg="#f4f4f4")
    label_bienvenida.pack(pady=20)

# ======= MOSTRAR CONTRASEÑA =======
def toggle_password():
    if entry_clave.cget("show") == "*":
        entry_clave.config(show="")
        btn_toggle.config(text="🙈")
    else:
        entry_clave.config(show="*")
        btn_toggle.config(text="👁")
        

# ======= CONFIGURACIÓN DE LA VENTANA PRINCIPAL =======
root = tk.Tk()
root.title("Login - Gestión de Tareas")
root.geometry("800x400")
root.resizable(False, False)

# ======= MARCO PRINCIPAL =======
frame_login = tk.Frame(root, bg="white")
frame_login.pack(expand=True, fill="both")

# ======= MARCO DE LA IMAGEN (IZQUIERDA) =======
frame_izq = tk.Frame(frame_login, bg="white")
frame_izq.grid(row=0, column=0, padx=20, pady=20)

try:
    imagen = Image.open("timebox.png")  
    imagen = imagen.resize((400, 400), Image.Resampling.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)
    label_imagen = tk.Label(frame_izq, image=imagen, bg="white")
    label_imagen.pack()
except Exception as e:
    print(f"Error cargando imagen: {e}")

# ======= MARCO DEL FORMULARIO (DERECHA) =======
frame_der = tk.Frame(frame_login, bg="white")
frame_der.grid(row=0, column=1, padx=50, pady=50)

tk.Label(frame_der, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

tk.Label(frame_der, text="Usuario:", bg="white", anchor="w").pack(fill="x")
entry_usuario = ttk.Entry(frame_der, width=30)
entry_usuario.pack(pady=5)

tk.Label(frame_der, text="Contraseña:", bg="white", anchor="w").pack(fill="x")
frame_clave = tk.Frame(frame_der, bg="white")
frame_clave.pack()
entry_clave = ttk.Entry(frame_clave, width=27, show="*")
entry_clave.pack(side="left", pady=5)
btn_toggle = ttk.Button(frame_clave, text="👁", width=3, command=toggle_password)
btn_toggle.pack(side="right", padx=2)

# Botón de inicio de sesión
ttk.Button(frame_der, text="Iniciar Sesión", command=login).pack(pady=10)

ttk.Button(frame_der, text="Olvidé mi contraseña", command=recuperar_contrasena).pack(pady=5)

# Botón para registrar usuario
ttk.Button(frame_der, text="Registrar Usuario", command=ventana_registro).pack(pady=5)

# Botón para salir desde el login
ttk.Button(frame_der, text="Salir", command=root.destroy).pack(pady=5)

# Iniciar la interfaz gráfica
root.mainloop()