import threading
import multiprocessing
import os

def calcular_suma_cuadrados(lista, resultado, lock):
    suma = 0
    for num in lista:
        suma += num * num
    with lock:
        resultado.append(suma)

def hilo(lista, resultado, lock):
    calcular_suma_cuadrados(lista, resultado, lock)

def proceso(lista, resultado, lock):
    calcular_suma_cuadrados(lista, resultado, lock)

def demonio():
    print("Soy un demonio con identificador:", os.getpid())

if __name__ == "__main__":
    lista_numeros = [1, 2, 3, 4, 5]

    resultado_hilo = []
    resultado_proceso = []
    lock = multiprocessing.Lock()

    hilo1 = threading.Thread(target=hilo, args=(lista_numeros, resultado_hilo, lock))
    hilo1.start()

    proceso1 = multiprocessing.Process(target=proceso, args=(lista_numeros, resultado_proceso, lock))
    proceso1.start()

    demonio_process = multiprocessing.Process(target=demonio)
    demonio_process.daemon = True
    demonio_process.start()

    hilo1.join()
    proceso1.join()

    print("Resultado calculado por el hilo:", resultado_hilo[0])

    if resultado_proceso:
        print("Resultado calculado por el proceso:", resultado_proceso[0])
    else:
        print("El proceso no pudo completar la tarea correctamente.")

    print("Programa principal terminado.")
