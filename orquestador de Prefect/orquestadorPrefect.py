import prefect
from prefect import task, Flow
import random
import json
import matplotlib.pyplot as plt
import statistics

@task
def generar_numeros_aleatorios():
    return [random.randint(1, 100) for _ in range(10)]

@task
def guardar_en_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo_json:
        json.dump(datos, archivo_json)

@task
def cargar_desde_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return None

@task
def calcular_estadisticas(numeros):
    return {
        "media": statistics.mean(numeros),
        "mediana": statistics.median(numeros),
        "desviacion_estandar": statistics.stdev(numeros),
        "minimo": min(numeros),
        "maximo": max(numeros)
    }
@task
def validar_datos():
    numeros_generados = generar_numeros_aleatorios.run() 
    while any(num <= 40 for num in numeros_generados):  
        numeros_generados = generar_numeros_aleatorios.run()  
    return numeros_generados

@task
def visualizar_errores(errores_por_intentos, numeros_validos):
    intentos = range(1, len(errores_por_intentos) + 1)
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Intento')
    ax1.set_ylabel('Número de Números No Válidos', color=color)
    ax1.plot(intentos, errores_por_intentos, marker='o', linestyle='-', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Números Válidos', color=color)
    ax2.plot(intentos, numeros_validos, marker='o', linestyle='-', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.title('Errores en la Validación de Números Aleatorios por Intento')
    plt.show()

nombre_archivo = 'numeros_guardados.json'

with Flow("Procesamiento de Datos") as flow:
    numeros_guardados = cargar_desde_json(nombre_archivo)
    numeros_validos = generar_numeros_aleatorios()
    errores_validacion = validar_datos()
    visualizacion = visualizar_errores(errores_validacion, numeros_validos)
    estadisticas = calcular_estadisticas(numeros_validos)
    
    if numeros_guardados is not None:
        guardar_en_json(numeros_validos, nombre_archivo)

    visualizacion.set_upstream(errores_validacion)
    estadisticas.set_upstream(numeros_validos)

flow.run()