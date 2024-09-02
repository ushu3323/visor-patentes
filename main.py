# Sirve para recibir imagen de la camara y manipularla
import cv2
import tkinter.messagebox
import tkinter

# Crear variable para tener acceso a la camara
camara = cv2.VideoCapture(0)

while True:
    # Leer un fotograma de la camara
    ret, fotograma = camara.read()

    if not ret:
        print("No se pudo leer el fotograma")
    cv2.imshow("Titulo", fotograma) # Muestra un fotograma en una ventana

    # Comprueba si se presiono la tecla "q"
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('h'):
        tkinter.messagebox.showinfo("Titulo", "Hello world!")

camara.release()
cv2.destroyAllWindows()

#detectar recuadro de patente


