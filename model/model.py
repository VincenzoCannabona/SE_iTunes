import networkx as nx
from networkx.algorithms.richclub import rich_club_coefficient

from database.dao import DAO


class Model:
    def __init__(self):
        self.G=nx.Graph()
        self.nodes=[]
        self.idMap={}





    def load_albums(self, durata):
        self.nodes=DAO.get_album_by_durata(durata)          #lista di oggetti

    def load_collegamenti(self, durata):
        self.collegamenti=DAO.get_collegamenti(durata)      #lista di tuple id album

    def build_graph(self):
        self.G.add_nodes_from(self.nodes)

        for a in self.nodes:
            self.idMap[a.id]=a

        for u,v in self.collegamenti:
            u=self.idMap[u]
            v=self.idMap[v]
            self.G.add_edge(u,v)

    def calcola_componente_connessa(self, album):
        a=self.idMap[album]
        lista=list(nx.node_connected_component(self.G, a))          #nx.connected_components(G) restituisce tutte le componenti connesse del grafo
        durata=0
        for i in lista:
            durata+=i.durata

        return len(lista),lista, durata

    def calcola_percorso_con_piu_nodi(self, durata, album):
        self.a1=self.idMap[album]
        self.percorso_massimo=()
        self.lunghezza_massima=0
        x,componente_connessa,y=self.calcola_componente_connessa(self.a1)
        percorso=[self.a1]
        self.ricorsione(percorso,componente_connessa,self.a1.durata,durata)

    def ricorsione(self,percorso,componente_connessa, durata_corrente,durata_max):
        if durata_corrente>durata_max:
            return
        if len(percorso)>len(self.percorso_massimo):
            self.percorso_massimo=percorso[:]


        for v in componente_connessa:
            if v not in percorso:
                percorso.append(v)
                self.ricorsione(percorso,componente_connessa,durata_corrente+v.durata,durata_max)
                percorso.pop()


"""Permettere all’utente di inserire una durata complessiva "dTOT" (nel campo "Durata Totale"), espressa in minuti. Alla pressione del pulsante “Set di Album”, utilizzare un algoritmo ricorsivo per estrarre un set di album dal grafo che abbia le seguenti caratteristiche:

- Includa "a1";

Includa solo album appartenenti alla stessa componente connessa di "a1";
Includa il maggior numero possibile di album;

-Abbia una durata complessiva, definita come la somma della durata degli album in esso contenuti, non superiore "dTOT"."""
