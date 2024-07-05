import heapq  # Esto nos ayuda a trabajar con listas de cosas en orden, como si fuera una fila de cosas a hacer.

#----------------Clase Ansi para colorear la matriz----------
class Ansi:
    ESC = '\033['  # Esto es como una palabra mágica para cambiar colores en la pantalla.

    # Aquí tenemos una lista de colores con palabras mágicas que les dicen qué color usar.
    COLORS = {
        'reset': '0',  # "reset" vuelve el texto a su color normal.
        'black': '30',  # "black" es el color negro.
        'red': '31',    # "red" es el color rojo.
        'green': '32',  # "green" es el color verde.
        'yellow': '33', # "yellow" es el color amarillo.
        'blue': '34',   # "blue" es el color azul.
        'magenta': '35',# "magenta" es un color púrpura.
        'cyan': '36',   # "cyan" es un color azul claro.
        'white': '37'   # "white" es el color blanco.
    }

    def __init__(self, text):
        self.text = text  # Guardamos el texto que queremos colorear.

    def colorize(self, color):
        color_code = self.COLORS.get(color, self.COLORS['reset'])  # Buscamos el código del color que queremos.
        return f"{self.ESC}{color_code}m{self.text}{self.ESC}0m"  # Devolvemos el texto con el color cambiado.

#------Constantes para la representacion del mapa y Obstaculos-----------------

CAMINO = 0  
EDIFICIO = 1 
BACHE = 2  
AREA_BLOQUEADA = 3  

#---------------Colores para cada tipo de lugar en el mapa----------------

COLOR_CAMINO = 'blue'  # azul.
COLOR_EDIFICIO = 'green'  # verde.
COLOR_BACHE = 'yellow'  # amarillo.
COLOR_AREA_BLOQUEADA = 'red'  #rojo.
COLOR_CAMINO_ENCONTRADO = 'cyan'  #azul claro.

#-------------Matriz----------------

rutas = [
    [0, 0, 0, 0, 0],  
    [0, 1, 0, 0, 0],  
    [0, 0, 0, 2, 0], 
    [0, 2, 0, 0, 0], 
    [0, 0, 3, 0, 0]   
]

#----------------------------Función para mostrar el mapa------------------------
def mostrar_mapa(rutas, camino=[]):
    simbolos = {CAMINO: '.', EDIFICIO: 'X', BACHE: 'B', AREA_BLOQUEADA: 'A'}  # Aquí definimos símbolos para cada lugar.
    colores = {CAMINO: COLOR_CAMINO, EDIFICIO: COLOR_EDIFICIO, BACHE: COLOR_BACHE, AREA_BLOQUEADA: COLOR_AREA_BLOQUEADA}

    for fila in range(len(rutas)):  # Recorremos cada fila del mapa.
        linea = []  # Empezamos una nueva línea de texto.
        for columna in range(len(rutas[fila])):  # Recorremos cada columna de la fila.
            celda = rutas[fila][columna]  # Obtenemos el valor de la celda actual.
            simbolo = simbolos.get(celda, '?')  # Obtenemos el símbolo correspondiente.
            if (fila, columna) in camino:  # Si esta celda está en el camino encontrado...
                color = COLOR_CAMINO_ENCONTRADO
                simbolo = '*'  # Cambiamos el símbolo a '*'.
            else:
                color = colores.get(celda, 'reset')
            ansi_text = Ansi(simbolo).colorize(color)  # Coloreamos el símbolo.
            linea.append(ansi_text)  # Añadimos el símbolo coloreado a la línea.
        print(' '.join(linea))  # Mostramos la línea entera.
    print()  # Añadimos una línea en blanco al final.

#---------------------Función para ingresar coordenadas------------------------

def ingresar_coordenadas(mensaje):
    while True:
        try:
            fila, columna = map(int, input(mensaje).split(','))  # Pedimos al usuario que ingrese coordenadas.
            if 0 <= fila < len(rutas) and 0 <= columna < len(rutas[0]):  # Verificamos que estén dentro del rango.
                return (fila, columna)  # Devolvemos las coordenadas.
            else:
                print("Coordenadas fuera de rango. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Usa el formato fila,columna. Inténtalo de nuevo.")

#-----------------------Función para agregar un obstáculo--------------------------

def agregar_obstaculo():
    obstaculo = ingresar_coordenadas("Ingresa las coordenadas del obstáculo (fila,columna): ")  # Pedimos coordenadas.
    if rutas[obstaculo[0]][obstaculo[1]] == CAMINO:  # Si el lugar es un camino...
        rutas[obstaculo[0]][obstaculo[1]] = EDIFICIO  # Lo cambiamos a edificio.
    else:
        print("La celda ya está ocupada por otro obstáculo. Inténtalo de nuevo.")

#---------------------Función heurística de Manhattan---------------------

def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Calculamos la distancia entre dos puntos.


#----------------------------Implementación del algoritmo A*-------------------------

def a_estrella(rutas, punto_inicio, punto_final):
    filas, columnas = len(rutas), len(rutas[0])  #tenemos el tamaño del mapa.
    lista_abierta = [(0, punto_inicio)]  # se crea una lista con el punto de inicio.
    rastrea = {}  #para guardar el camino que encontramos.
    guarda_costo_camino = {punto_inicio: 0}  # El costo para llegar al inicio es 0.
    guarda_costo_total = {punto_inicio: heuristica_manhattan(punto_inicio, punto_final)}  # Calculamos el costo total.

    while lista_abierta:  # Mientras haya cosas en la lista...
        _, nodo_actual = heapq.heappop(lista_abierta)  # Tomamos el punto con el costo más bajo.

        if nodo_actual == punto_final:  # Si llegamos al final...
            camino = []  # Creamos una lista para el camino.
            while nodo_actual in rastrea:  # Seguimos el camino hacia atrás.
                camino.append(nodo_actual)  # Añadimos el punto al camino.
                nodo_actual = rastrea[nodo_actual]  # Vamos al punto anterior.
            camino.append(punto_inicio)  # Añadimos el punto de inicio.
            return camino[::-1]  # Devolvemos el camino en orden correcto.

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Recorremos los vecinos del punto actual.
            vecino = (nodo_actual[0] + dr, nodo_actual[1] + dc)  # Calculamos las coordenadas del vecino.

            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:  # Si el vecino está en el mapa...
                if rutas[vecino[0]][vecino[1]] == CAMINO:  # Si el vecino es un camino...
                    costo_tentativo = guarda_costo_camino[nodo_actual] + 1  # Calculamos el nuevo costo.
                    if vecino not in guarda_costo_camino or costo_tentativo < guarda_costo_camino[vecino]:  # Si el nuevo costo es menor...
                        rastrea[vecino] = nodo_actual  # Guardamos el camino.
                        guarda_costo_camino[vecino] = costo_tentativo  # Guardamos el nuevo costo.
                        guarda_costo_total[vecino] = costo_tentativo + heuristica_manhattan(vecino, punto_final)  # Calculamos el costo total.
                        heapq.heappush(lista_abierta, (guarda_costo_total[vecino], vecino))  # Añadimos el vecino a la lista.

    return []  # Si no encontramos un camino, devolvemos una lista vacía.

#---------------------------Función para mostrar el camino en el mapa------------------------

def mostrar_camino_en_mapa(rutas, camino):
    mostrar_mapa(rutas, camino)  # Mostramos el mapa con el camino encontrado.

#----------------------Ejecución del programa----------------------

print("Mapa inicial:")
mostrar_mapa(rutas)  # Mostramos el mapa al inicio.

punto_inicio = ingresar_coordenadas("Ingresa las coordenadas del punto de inicio (fila,columna): ")  # Pedimos el punto de inicio.
punto_final = ingresar_coordenadas("Ingresa las coordenadas del punto final (fila,columna): ")  # Pedimos el punto final.

while True:
    agregar_obstaculo()  # Pedimos que agreguen un obstáculo.
    mostrar_mapa(rutas)  # Mostramos el mapa con el nuevo obstáculo.
    continuar = input("¿Quieres agregar otro obstáculo? (si/no): ").lower()  # Preguntamos si quieren agregar otro obstáculo.
    if continuar != 'si':
        break  # Si no quieren, salimos del bucle.

camino = a_estrella(rutas, punto_inicio, punto_final)  # Encontramos el camino con A*.

if camino:
    print(f"El camino más corto de {punto_inicio} a {punto_final} es:")
    mostrar_camino_en_mapa(rutas, camino)  # Mostramos el camino encontrado.
else:
    print("No hay un camino disponible desde el punto de inicio hasta el punto final.")  # Si no hay camino, mostramos un mensaje.
