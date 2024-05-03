import networkx as nx
import matplotlib.pyplot as plt

def mostrar_grafo(grafo):
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray", width=2)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.title("Mapa de rutas")
    plt.show()
    
def crear_grafo():
    grafo = nx.Graph()
    with open('rutas.txt', 'r', encoding='utf-8') as file:
        for line in file:
            estacion_salida, estacion_destino, costo = line.strip().split(', ')
            costo = int(costo)
            grafo.add_edge(estacion_salida, estacion_destino, weight=costo)
    return grafo

def mostrar_destinos(grafo, estacion_salida):
    destinos = list(grafo.neighbors(estacion_salida))
    print(f"Posibles destinos desde {estacion_salida}:")
    for destino in destinos:
        costo = grafo[estacion_salida][destino]['weight']
        print(f"{destino} - Costo: {costo}")

def dijkstra(grafo, estacion_salida):
    distancias = {estacion_salida: 0}
    anteriores = {}
    estaciones_restantes = set(grafo.nodes)

    while estaciones_restantes:
        nodo_actual = None
        for estacion in estaciones_restantes:
            if estacion in distancias:
                if nodo_actual is None:
                    nodo_actual = estacion
                elif distancias[estacion] < distancias[nodo_actual]:
                    nodo_actual = estacion

        if nodo_actual is None:
            break

        estaciones_restantes.remove(nodo_actual)
        peso_actual = distancias[nodo_actual]

        for vecino in grafo.neighbors(nodo_actual):
            peso = peso_actual + grafo[nodo_actual][vecino]['weight']
            if vecino not in distancias or peso < distancias[vecino]:
                distancias[vecino] = peso
                anteriores[vecino] = nodo_actual

    return distancias, anteriores

if __name__ == "__main__":
    grafo = crear_grafo()
    mostrar_grafo(grafo)
    
    # Mostrar destinos desde una estación de salida
    mostrar_destinos(grafo, "Pueblo Paleta")
    
    # Encontrar las mejores rutas usando Dijkstra
    distancias, anteriores = dijkstra(grafo, "Pueblo Paleta")
    print("\nMejores rutas:")
    for destino, distancia in distancias.items():
        print(f"A {destino} con costo de {distancia}")
    mostrar_grafo(grafo)