import cv2
import pytesseract
import tkinter as tk
from tkinter import Label, LabelFrame
from PIL import Image, ImageTk, ImageDraw, ImageOps # para el logo

# Constantes
ASPECT_RATIO_PATENTE = 2.5

#controlar tamaños de la ventana y camara
TAMANO_VENTANA = (900, 700)
ANCHO_CAMARA = 500
ALTO_CAMARA = 300

# Base de datos de patentes y textos asociados
base_de_datos = [
    ["CE 350 NT", '"La vida es muy peligrosa. No por las personas que hacen el mal, sino por la que se sientan a ver lo que pasa"\n- Albert Einstein'],
    ["MA 112 PI", 'Hola Mundo']
]

# Función para procesar el fotograma y detectar la patente
def procesar_fotograma():
    ret, fotograma = camara.read()

    if not ret:
        print("No se pudo leer el fotograma")
        return

    # ---- Detectar recuadro de patente ----
    
    # Aplicar escala de grises para optimizar la detección
    img_gris = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
    
    # Aplicar blur a la imagen para mejorar la deteccion de bordes
    img_gris = cv2.blur(img_gris, (2,2))
    
    # Resaltar bordes de la imagen usando algoritmo Canny
    canny = cv2.Canny(img_gris, 150, 200)
    
    # Hacer que los bordes sean mas gruesos
    canny = cv2.dilate(canny, None, iterations=1)
    
    # Detectar contornos
    resultado = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contornos = resultado[0]
    _ = resultado[1]
    
    
    # Dibujar lineas de color verde
    # cv2.drawContours(fotograma, contornos, -1, (0,255,0), 2)


    for c in contornos:
        area = cv2.contourArea(c)
        
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.09 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) == 4 and area > 10000:
            aspect_ratio = float(w) / h
            if aspect_ratio > ASPECT_RATIO_PATENTE:
                placa = img_gris[y:y+h, x:x+w]

                # Leer texto de la patente
                texto_patente = pytesseract.image_to_string(placa, config="--psm 11")
                texto_patente = texto_patente.strip()
                print(f"> {texto_patente} <")

                for fila in base_de_datos:
                    patente = fila[0]
                    if patente in texto_patente:
                        lbl_patente_detectada.config(text=texto_patente)
                        lbl_texto_asociado.config(text=fila[1])

    # Mostrar la imagen de la cámara en la interfaz
    img_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        
    img_rgb = cv2.resize(img_rgb, (ANCHO_CAMARA, ALTO_CAMARA))  # Redimensionar para ajustar a la caja
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    lbl_camara.img_tk = img_tk
    lbl_camara.config(image=img_tk)

    ventana.after(10, procesar_fotograma)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("VISOR DE PATENTES")
ventana.geometry(f"{TAMANO_VENTANA[0]}x{TAMANO_VENTANA[1]}")  # Establecer el tamaño de la ventana o puedes tocar la linea 11

# Centrar ventana en la pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

centrar_ventana(ventana)

# Función para redondear el logo
def redondear_logo(ruta):
    img = Image.open(ruta)
    img = img.resize((120, 120), Image.Resampling.LANCZOS)  # Ajusta el tamaño del logo
    img = ImageOps.fit(img, (120, 120), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
    img.putalpha(mask)
    return img

# Cargar la imagen del logo
logo_img = redondear_logo("C:/Users/aguer/Desktop/visor-patentes/Head.png")
logo_tk = ImageTk.PhotoImage(logo_img)

# Crear encabezado
encabezado = tk.Frame(ventana, bg='lightgrey')
encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")

logo_label = Label(encabezado, image=logo_tk, bg='lightgrey')
logo_label.grid(row=0, column=0, padx=80, pady=5, sticky="w")

encabezado_texto = tk.Label(encabezado, text="CENT 35 - PROF. JULIAN JOSÉ GODOY\nINSTITUTO DE EDUCACIÓN SUPERIOR TÉCNICA", 
font=("Arial", 14), bg='lightgrey', anchor="center", justify="center")
encabezado_texto.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Agregar texto adicional
texto_adicional = tk.Label(ventana, text="CURSO 1° AÑO\nCARRERA: DISEÑO DE SOFTWARE", 
                           font=("Arial", 12, 'bold'), bg='lightgrey', anchor="center", justify="center")
texto_adicional.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Crear widgets de la interfaz
frame_camara = tk.Frame(ventana, bg='white')
frame_camara.grid(row=2, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

lbl_camara = Label(frame_camara, bg='white')
lbl_camara.pack(fill="both", expand=True)

frame_patente = LabelFrame(ventana, text="PATENTE DETECTADA", padx=10, pady=10)
lbl_patente_detectada = Label(frame_patente, text="No detectada aún", anchor="center", font=("Arial", 12))
lbl_patente_detectada.pack(fill="both")
frame_patente.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

frame_texto = LabelFrame(ventana, text="TEXTO ASOCIADO", padx=10, pady=10)
lbl_texto_asociado = Label(frame_texto, text="Esperando detección...", anchor="center", font=("Arial", 12))
lbl_texto_asociado.pack(fill="both")
frame_texto.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Crear pie de página
pie_pagina = tk.Label(ventana, text="ESTUDIANTES:\n• PAVÓN, Carlos Eduardo\n• PAVÓN, Matías Ignacio\n• AGÜERO, Luis\n• Omar", 
                      font=("Arial", 10), padx=10, pady=10, bg='lightgrey', anchor="w")
pie_pagina.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

# Ajustar el tamaño de las columnas y filas
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=2)
ventana.grid_rowconfigure(2, weight=1)
ventana.grid_rowconfigure(3, weight=1)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Crear variable para tener acceso a la camara
camara = cv2.VideoCapture(0)


# Iniciar el procesamiento de la cámaras
procesar_fotograma()


# evitar que se toque el tamaño de la ventana
ventana.resizable(False, False)         


# Ejecutar la ventana de Tkinter
ventana.mainloop()

# Liberar la cámara al cerrar
camara.release()
cv2.destroyAllWindows()
