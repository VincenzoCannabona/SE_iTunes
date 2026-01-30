import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G=nx.Graph()
        self.nodes=[]
        self.edges=[]
        self.idMap={}

    def load_albums(self, durata_minima):
        self.albums=DAO.get_all_album_duration(durata_minima)
        #print(self.albums)

    def load_collegamenti(self,durata_minima):
        self.edges=DAO.get_all_connessioni(durata_minima)


    def build_graph(self):
        self.G.clear()
        self.G.add_nodes_from(self.albums)              #i nodi sono gli OGETTI album

        #per archi invce ho id int collegati
        #creo una mappa che colleghi l'id numerico all'oggetto corrispondente
        for a in self.albums:              #a è un oggetto
            self.idMap[a.id] = a           #collego l'id all'oggetto

        for u,v in self.edges:          #creo la coppia di oggetti da passare direttamente al grafo
            if u in self.idMap and v in self.idMap:
                u=self.idMap[u]
                v=self.idMap[v]
                self.G.add_edge(u,v)

    def calcola_c_c(self, id):
        #id è un intero ma io devo passare un oggetto perchè il grafo è fatto di oggetti album
        album=self.idMap[id]
        return list(nx.node_connected_component(self.G, album))             #restituisce un insieme con tutti i nodi collegati al nodo passato e anche quelli collegati ai nodi collegati ....


    def set_massimo(self, nodo_p, durata_massima):
        nodo_partenza = self.idMap[nodo_p]
        self.soluzione_set_massimo=[]                                       #lista di oggetti
        set_corrente=[nodo_partenza]
        componenti=list(nx.node_connected_component(self.G, nodo_partenza))               #nodo di partenza deve essere un oggetto
        self.ricorsione(componenti, set_corrente, nodo_partenza.duration, durata_massima)
        return self.soluzione_set_massimo

    #la ricorsione riceve una durata massima e il nodo di partenza scelto nel dd precedente (a1)
    #restituisce un set
    def ricorsione(self, componenti,set_corrente,durata_corrente, durata_massima ):
        if len(set_corrente)>len(self.soluzione_set_massimo):
            self.soluzione_set_massimo=set_corrente[:]

        #ciclo su tutti gli album della componente
        for a in componenti:
            if a in set_corrente:
                continue
            nuova_durata=durata_corrente + a.duration
            #condizione durata complessiva non superiore a durata massima
            if nuova_durata<=durata_massima:
                set_corrente.append(a)
                self.ricorsione(componenti, set_corrente, nuova_durata, durata_massima)
                set_corrente.pop()
                #pop senza argomenti rimuove l'ultimo elemento inserito (pop(index)  si aspetta un indice numerico)

"""Includa "a1";
Includa solo album appartenenti alla stessa componente connessa di "a1";
Includa il maggior numero possibile di album;
Abbia una durata complessiva, definita come la somma della durata degli album in esso contenuti, non superiore "dTOT"."""