import tkinter

ventana = tkinter.Tk()

# Tamaño de la ventana
#ventana.geometry("500x500")

# Obtener el tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Calcular las coordenadas x e y para centrar la ventana
x = (screen_width // 2) - (500 // 2)
y = (screen_height // 2) - (500 // 2)

# Establecer la geometría de la ventana (tamaño + posición)
ventana.geometry(f'800x600+{x}+{y}')

# Dentro de la ventana
etiqueta = tkinter.Label(ventana, text="Hola mundo")
etiqueta.pack(side=tkinter.BOTTOM)

ventana.mainloop()
