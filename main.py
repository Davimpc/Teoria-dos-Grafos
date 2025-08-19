from abc import ABC, abstractmethod

class Grafo(ABC):
    @abstractmethod
    def numero_de_vertices(self):
        pass

    @abstractmethod
    def numero_de_arestas(self):
        pass

    @abstractmethod
    def sequencia_de_graus(self):
        pass

    @abstractmethod
    def adicionar_aresta(self, u, v):
        pass

    @abstractmethod
    def remover_aresta(self, u, v):
        pass

    @abstractmethod
    def imprimir(self):
        pass


class GrafoDenso(Grafo):
    def __init__(self, vertices):
        if isinstance(vertices, int):
            self.rotulos = list(range(vertices))
        else:
            self.rotulos = list(vertices)

        self.num_vertices = len(self.rotulos)

        self.matriz = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]
        self.num_arestas_total = 0

    def numero_de_vertices(self):
        return self.num_vertices

    def numero_de_arestas(self):
        return self.num_arestas_total

    def sequencia_de_graus(self):
        return [sum(linha) for linha in self.matriz]

    def adicionar_aresta(self, u, v):
        i, j = self.rotulos.index(u), self.rotulos.index(v)
        if self.matriz[i][j] == 0:
            self.matriz[i][j] = 1
            self.matriz[j][i] = 1
            self.num_arestas_total += 1

    def remover_aresta(self, u, v):
        i, j = self.rotulos.index(u), self.rotulos.index(v)
        if self.matriz[i][j] == 1:
            self.matriz[i][j] = 0
            self.matriz[j][i] = 0
            self.num_arestas_total -= 1

    def imprimir(self):
        print("   ", " ".join(map(str, self.rotulos)))
        for i, linha in enumerate(self.matriz):
            print(f"{self.rotulos[i]}: ", " ".join(map(str, linha)))


V = ["A", "B", "C", "D", "E"]
g = GrafoDenso(V)

arestas = [("A", "B"), ("A", "C"), ("C", "D"), ("C", "E"), ("B", "D")]
for u, v in arestas:
    g.adicionar_aresta(u, v)

print("Matriz de Adjacência:")
g.imprimir()
print("Número de vértices:", g.numero_de_vertices())
print("Número de arestas:", g.numero_de_arestas())
print("Sequência de graus:", g.sequencia_de_graus())

g.remover_aresta("A", "C")

print("\nMatriz de Adjacência:")
g.imprimir()
print("Número de vértices:", g.numero_de_vertices())
print("Número de arestas:", g.numero_de_arestas())
print("Sequência de graus:", g.sequencia_de_graus())
