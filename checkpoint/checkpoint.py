import pickle
import os

def guardar_estado(archivo, estado):
    with open(archivo, 'wb') as f:
        pickle.dump(estado, f)

def cargar_estado(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

estado_restaurado = cargar_estado('estado.pkl')

print("Estado restaurado:", estado_restaurado)

contador = int(input("Ingrese el valor del contador: "))
nombre = input("Ingrese su nombre: ")

estado_actual = {'contador': contador, 'nombre': nombre}

estado_combinado = {**estado_restaurado, **estado_actual}

print("Estado actual:", estado_combinado)

guardar_estado('estado.pkl', estado_combinado)
