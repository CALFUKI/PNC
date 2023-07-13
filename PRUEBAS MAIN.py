import tkinter as tk
import J_WINDOW
import S_WINDOW
import SPECIAL_WINDOW

#FUNCION DE CHECKEO
def checkeo(valor):
    if valor == "1":
    # Cerrar la ventana principal
        root.destroy()
    # Abrir la segunda ventana
        J_WINDOW.J_WINDOW()
    if valor == "2":
    # Cerrar la ventana principal
        root.destroy()
    # Abrir la tercer ventana
        S_WINDOW.S_WINDOW()
    if valor == "3":
    # Cerrar la ventana principal
        root.destroy()
    # Abrir la tercer ventana
        SPECIAL_WINDOW.SPECIAL_WINDOW()


# Crear la ventana principal
root = tk.Tk()
root.title("Primera ventana")

# Agregar un botón en la ventana principal
button1 = tk.Button(root, text="Click", command=lambda:checkeo("1"))
button1.pack()
button2 = tk.Button(root, text="Click", command=lambda:checkeo("2"))
button2.pack()
button3 = tk.Button(root, text="Click", command=lambda:checkeo("3"))
button3.pack()


# Ejecutar la ventana principal
root.mainloop()
