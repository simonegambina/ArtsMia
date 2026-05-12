import copy

import networkx as nx
from networkx.algorithms.traversal import dfs_tree

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n
        self._optPath = []
        self._optCost = 0

    def getOptPath(self, source, lun):
        parziale = [source]

        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()  # Backtracking
        return self._optPath, self._optCost

    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            #condizione di terminazione, allora parziale è lunga esattamente lun
            #per cui verifico che questa parziale sia meglio del mio best
            # (condizione di ottimalità), ed in ogni caso esco.
            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(parziale)
            return

        #se arrivo qui, posso ancora aggiungere nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()  # Backtracking


    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path)-1):
            costo += self._graph[path[i]][path[i+1]]["weight"]
        return costo

    def getInfoCompConnessa(self, id_oggetto):
        # cercare la componente connessa che contiene id_oggetto
        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        # strategia 1
        dfsTree = nx.dfs_tree(self._graph, source)
        print("size connessa con dfs_tree", len(dfsTree.nodes()))

        # strategia 2
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("size connessa con dfs_predecessors", len(dfsPred.values()))

        # strategia 3
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_component", len(conn))

        return len(conn)

    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO

    def getNodeFromId(self, id_oggetto):
        return self._idMapAO[id_oggetto]

    def buildGraph(self):
        # aggiunge i nodi
        self._graph.add_nodes_from(self._nodes)

        # aggiunge gli archi
        self.addEdgesV2()

    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)