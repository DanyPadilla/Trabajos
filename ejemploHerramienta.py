def calcular_area_rectangulo(base, altura):
    assert base >= 0 and altura >= 0, "Los valores de base y altura deben ser no negativos."
    return base * altura

base = -5
altura = 10
area = calcular_area_rectangulo(base, altura)
print("El área del rectángulo es:", area)
