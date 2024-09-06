# Sirve para recibir imagen de la camara y manipularla
import cv2
import pytesseract


ASPECT_RATIO_PATENTE = 2.5

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Crear variable para tener acceso a la camara
camara = cv2.VideoCapture(0)

while True:
    # Leer un fotograma de la camara
    ret, fotograma = camara.read()

    if not ret:
        print("No se pudo leer el fotograma")

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

        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) == 4 and area>10000:
            # print("area=", area)
            
            aspect_ratio = float(w)/h
            if aspect_ratio > ASPECT_RATIO_PATENTE:
                # Extraer placa del fotograma de la camara
                placa = img_gris[y:y+h, x:x+w]

                # Mostrar placa extraida
                cv2.imshow("PLACA", placa)
                cv2.moveWindow("PLACA", 800, 10)

                # Dibujar rectangulo verde en el fotograma de la camara
                cv2.rectangle(canny, (x,y), (x+w, y+h), (0,255,0), 3)

                texto_patente: str = pytesseract.image_to_string(placa, config="--psm 11")
                print("TEXTO PATENTE:", texto_patente)



    cv2.imshow("Camara Web", canny) # Muestra un fotograma en una ventana

    # Comprueba si se presiono la tecla "q"
    if cv2.waitKey(1) == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()

