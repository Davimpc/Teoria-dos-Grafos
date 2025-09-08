import sys
import itertools
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

    @abstractmethod
    def is_simples(self):
        pass

    @abstractmethod
    def is_nulo(self):
        pass

    @abstractmethod
    def is_completo(self):
        pass

    @abstractmethod
    def get_vertices(self):
        pass
    
    @abstractmethod
    def get_arestas(self):
        pass

    @abstractmethod
    def is_subgrafo(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_gerador(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_induzido(self, outro_grafo):
        pass

    def _checa_mapeamento_preserva_adjacencia(self, grafo1, grafo2, mapping):
        arestas_1 = grafo1.get_arestas()
        arestas_2 = grafo2.get_arestas()

        for aresta in arestas_1:
            u1, v1 = aresta
            u2 = mapping[u1]
            v2 = mapping[v1]
            if ((u2, v2) not in arestas_2) and ((v2, u2) not in arestas_2):
                return False
        return True

    def is_isomorfo(self, grafo):
        if (self.numero_de_vertices() != grafo.numero_de_vertices()):
            return False
        if (self.numero_de_arestas() != grafo.numero_de_arestas()):
            return False
        if self.sequencia_de_graus() != grafo.sequencia_de_graus():
            return False

        vertices1 = list(self.get_vertices())
        vertices2 = list(grafo.get_vertices())
        for p in itertools.permutations(vertices2):
            mapping = dict(zip(vertices1, p))
            if self._checa_mapeamento_preserva_adjacencia(self, grafo, mapping):
                return True
        return False


class GrafoEsparso(Grafo):
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.vertices = labels
        elif num_vertices:
            self.vertices = [str(i) for i in range(num_vertices)]
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)
        self.lista_adj = {vertice: [] for vertice in self.vertices}

    def numero_de_vertices(self):
        return len(self.vertices)

    def numero_de_arestas(self):
        return (sum([len(vizinhos) for vizinhos in self.lista_adj.values()]) // 2)

    def sequencia_de_graus(self):
        return sorted([len(values) for values in self.lista_adj.values()])

    def _validar_vertice(self, vertice):
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True

    def adicionar_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v, peso=None):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
            for index, ver in enumerate(self.lista_adj[u]):
                if v == ver:
                    del self.lista_adj[u][index]
                    print(f"Aresta removida entre {u} e {v}.")
                    break
            for index, ver in enumerate(self.lista_adj[v]):
                if u == ver:
                    del self.lista_adj[v][index]
                    print(f"Aresta removida entre {v} e {u}.")
                    break
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        print("\nLista de Adjacências:")
        for vertice, vizinhos in self.lista_adj.items():
            saida = [vizinho for vizinho in vizinhos]             
            print(f"  {vertice} -> [ {saida} ]")
        print()

    def is_simples(self):
        for vertice, vizinhos in self.lista_adj.items():
            if vertice in vizinhos:
                return False
            if len(vizinhos) != len(set(vizinhos)):
                return False
        return True

    def is_nulo(self):
        return self.numero_de_arestas() == 0 and self.numero_de_vertices() > 0

    def is_completo(self):
        return (self.is_simples() and 
                self.numero_de_arestas() == (self.numero_de_vertices() *
                                            (self.numero_de_vertices() - 1)) // 2)

    def get_vertices(self):
        return list(self.lista_adj.keys())
    
    def get_arestas(self):
        arestas = []
        for vertice, vizinhos in self.lista_adj.items():
            for vizinho in vizinhos:
                if (vizinho, vertice) not in arestas:
                    arestas.append((vertice, vizinho))
        return arestas
    
    def is_subgrafo(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")
        for vertice in self.get_vertices():
            if vertice not in outro_grafo.get_vertices():
                return False
        for aresta in self.get_arestas():
            if aresta not in outro_grafo.get_arestas():
                return False
        return True

    def is_subgrafo_gerador(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")
        return self.is_subgrafo(outro_grafo) and all(
            vertice in self.get_vertices() for vertice in outro_grafo.get_vertices()
        )

    def is_subgrafo_induzido(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")
        if self.is_subgrafo(outro_grafo):
            lista_arestas = []
            for aresta in outro_grafo.get_arestas():
                if all(v in self.get_vertices() for v in aresta):
                    lista_arestas.append(aresta)
            for aresta in self.get_arestas():
                if aresta not in lista_arestas:
                    return False
            return True
        return False

  
    def colorir_grafo(self):
        cores = {}
        for vertice in self.get_vertices():
            cor_tentativa = 1
            while True:
                print(f"Tentando colorir a aula {vertice} com {cor_tentativa} horários...")
                conflito = False
                for vizinho in self.lista_adj[vertice]:
                    if vizinho in cores and cores[vizinho] == cor_tentativa:
                        conflito = True
                        break
                if not conflito:
                    cores[vertice] = cor_tentativa
                    break
                cor_tentativa += 1
        numero_minimo_horarios = max(cores.values())
        print(f"Número mínimo de horários necessários (Número Cromático x(G)): {numero_minimo_horarios}")
        return numero_minimo_horarios, cores


if __name__ == "__main__": 
    aulas = ['M', 'A', 'C', 'F', 'Q', 'P'] 
    g = GrafoEsparso(labels=aulas) 

    # Os conflitos são as nossas arestas
    g.adicionar_aresta('C', 'F')
    g.adicionar_aresta('C', 'A')
    g.adicionar_aresta('F', 'A')
    g.adicionar_aresta('M', 'P')
    g.adicionar_aresta('M', 'A')
    g.adicionar_aresta('P', 'A')
    g.adicionar_aresta('Q', 'F')

    for v_origin, v_dest in g.get_arestas():
        print(f"- Aula {v_origin} tem conflito com: {v_dest}") 
    print("-" * 30) 

    numero_minimo_horarios, cores_atribuidas = g.colorir_grafo() 
    print(cores_atribuidas)
