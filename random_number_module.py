import random

def generar_premio():
    numero_aleatorio = random.randint(0,1000)

    return numero_aleatorio

def generar_lista_premios():
    lista_premios = []

    for i in range(0,100):
        lista_premios.append(generar_premio())
    
    return lista_premios

def separar_repetidos(lista_premios):
    lista_de_premios_con_repetidos = lista_premios
    lista_sin_repetidos = []
    repetidos = []

    for i in lista_de_premios_con_repetidos:
        if i in lista_sin_repetidos:
            repetidos.append(i)
        else: lista_sin_repetidos.append(i)

    lista_final = [tuple(lista_sin_repetidos), tuple(repetidos)]

    return lista_final


def calcular_equitatividad(lista_de_tuplas):

    print(lista_de_tuplas)

    tupla1, tupla2 = lista_de_tuplas

    print(len(tupla1))
    print(len(tupla2))
    
    return len(tupla2)/len(tupla1)

print(calcular_equitatividad(separar_repetidos(generar_lista_premios())))


