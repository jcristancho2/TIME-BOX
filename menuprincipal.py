import tkinter as tk
from tkinter import ttk, messagebox

# ======= CONFIGURACIÓN =======
tema_actual = "claro"

# ======= FUNCIÓN PARA MOSTRAR FORMULARIOS EN ÁREA DERECHA =======
def mostrar_contenido(texto):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    tk.Label(frame_contenido, text=texto, font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=20)

# ======= FUNCIÓN PARA CAMBIAR TEMA =======
def cambiar_tema():
    global tema_actual
    tema_actual = "oscuro" if tema_actual == "claro" else "claro"
    actualizar_tema()

# ======= FUNCIÓN PARA ACTUALIZAR COLORES SEGÚN EL TEMA =======
def actualizar_tema():
    global bg_color, fg_color
    
    if tema_actual == "claro":
        bg_color = "white"
        fg_color = "black"
        btn_color = "#f0f0f0"
    else:
        bg_color = "#2c2c2c"
        fg_color = "white"
        btn_color = "#444444"

    root.configure(bg=bg_color)
    frame_menu.configure(bg=bg_color)
    frame_contenido.configure(bg=bg_color)

    for widget in frame_menu.winfo_children():
        if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
            widget.configure(bg=bg_color, fg=fg_color)
        else:
            widget.configure(bg=bg_color)
    for widget in frame_contenido.winfo_children():
        if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
            widget.configure(bg=bg_color, fg=fg_color)
        else:
            widget.configure(bg=bg_color)
    for btn in botones_menu:
        btn.configure(bg=btn_color, fg=fg_color)

# ======= CONFIGURACIÓN DE LA VENTANA PRINCIPAL =======
root = tk.Tk()
root.title("Gestión de Tareas")
root.geometry("1000x600")
root.resizable(True, True)

# ======= MENÚ LATERAL IZQUIERDO =======
frame_menu = tk.Frame(root, width=200)
frame_menu.pack(side="left", fill="y")

frame_contenido = tk.Frame(root)
frame_contenido.pack(side="right", expand=True, fill="both")

botones_menu = []

botones = [
    ("Registrar Tarea", lambda: mostrar_contenido("Registrar Tarea")),
    ("Modificar Tarea", lambda: mostrar_contenido("Modificar Tarea")),
    ("Eliminar Tarea", lambda: mostrar_contenido("Eliminar Tarea")),
    ("Visualizar Tareas", lambda: mostrar_contenido("Visualizar Tareas")),
]

for texto, comando in botones:
    btn = tk.Button(frame_menu, text=texto, command=comando, width=20)
    btn.pack(pady=5)
    botones_menu.append(btn)

# ======= CONFIGURACIÓN DE USUARIOS =======
frame_configuracion = tk.Frame(frame_menu)
tk.Button(frame_configuracion, text="Config (cambiar color)", command=cambiar_tema, width=20).pack(pady=5)
frame_configuracion.pack(pady=20)

# ======= FUNCIÓN PARA CONFIRMAR SALIDA =======
def confirmar_salida():
    respuesta = messagebox.askyesno("Confirmar salida", "¿Estás seguro de que deseas salir?")
    if respuesta:
        root.quit()

# ======= BOTÓN DE SALIR =======
btn_salir = tk.Button(frame_menu, text="Salir", command=confirmar_salida, width=20, bg="red", fg="white")
btn_salir.pack(pady=10)

botones_menu.append(btn_salir)

actualizar_tema()

root.mainloop()