import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        durata=self._view.txt_durata.value
        if durata:
            try:
                durata = int(durata)
                self._model.load_albums(durata)
                self._model.load_collegamenti(durata)
                self._model.build_graph()
                self._view.lista_visualizzazione_1.clean()
                self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{self._model.G}"))
                for a in self._model.G.nodes:
                    nuova_opzione = ft.dropdown.Option(key=str(a.id), text=a.title)
                    self._view.dd_album.options.append(nuova_opzione)
                self._view.pulsante_analisi_comp.disabled = False
                self._view.update()
            except ValueError:
                self._view.show_alert("inserisci un valore numerico corretto")
        else:
            self._view.show_alert("inserisci prima una durata minima")


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.album=int(self._view.dd_album.value)

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        lunghezza,lista,durata=self._model.calcola_componente_connessa(self.album)
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"dimensione componente: {lunghezza}, durata: {durata}"))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO