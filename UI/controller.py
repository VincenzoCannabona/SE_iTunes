import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            durata_minima=float(self._view.txt_durata.value)
            self._model.load_albums(durata_minima)
            self._model.load_collegamenti(durata_minima)
            self._model.build_graph()
            self._view.lista_visualizzazione_1.clean()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato :{len(self._model.G.nodes)} album, {len(self._model.G.edges)} archi"))
            self._view.dd_album.options = []
            for a in self._model.albums:
                nuova_opzione = ft.dropdown.Option(key=str(a.id),  # L'ID nascosto (deve essere stringa)
                                                    text=a.title)  # Quello che vede l'utente
                self._view.dd_album.options.append(nuova_opzione)

        except ValueError:
            self._view.show_alert("inserire un valore valido")

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.id_scelto =int(self._view.dd_album.value)                   #id (non posso prendere l'intero oggetto perche .value restituisce sempre una stringa)


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if not self.id_scelto:
            self._view.show_alert("scegli un titolo")
            return
        duration=0
        self.lista = self._model.calcola_c_c(self.id_scelto)        #lista di oggetti
        for a in self.lista:
            duration += a.duration
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"la componente connessa ha {len(self.lista)} album"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"durata totale {duration}"))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        durata_totale=float(self._view.txt_durata_totale.value)
        lista=self._model.set_massimo(self.id_scelto, durata_totale)
        self._view.lista_visualizzazione_3.clean()
        for a in lista:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{a.title}: {a.duration}"))
        self._view.update()
