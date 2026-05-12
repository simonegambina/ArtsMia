import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e "
                    f"{self._model.getNumEdges()} archi."))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()


    def handleCompConnessa(self,e):
        txtIdOggetto = self._view._txtIdOggetto.value

        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un valore nel campo ID.", color="red"))
            self._view.update_page()
            return

        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un valore numerico nel campo ID.", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, l'ID inserito non è presente nel grafo.", color="orange"))
            self._view.update_page()
            return

        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} è composta da {sizeCompConn} nodi",
                    color="green"))

        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        lunValues = list(range(2, sizeCompConn))

        # metodo possibile
        #for v in lunValues:
        #    self._view._ddLun.options.append(ft.dropdown.Option(v))

        lunValuesDD = list(map(lambda x: ft.dropdown.Option(x), lunValues))
        # serve per poter assegnarlo direttamente come sotto

        self._view._ddLun.options = lunValuesDD

        self._view.update_page()



    def handleCerca(self, e):
       source = self._model.getNodeFromId(int(self._view._txtIdOggetto.value))

       lun = self._view._ddLun.value

       if lun is None:
           self._view.txt_result.controls.clear()
           self._view.txt_result.controls.append(
               ft.Text("Attenzione, selezionare un valore di lunghezza fra le scelte proposte.",
                       color = "red"))
           self._view.update_page()
           return

       lunInt = int(lun)

       path, cost = self._model.getOptPath(source, lunInt)

       self._view.txt_result.controls.clear()
       self._view.txt_result.controls.append(
           ft.Text(f"Ho trovato un cammino che parte da {source} "
                   f"e che ha un peso totale pari a {cost}.", color="green"))
       self._view.txt_result.controls.append(
           ft.Text("Di seguito i nodi che compongono questo cammino:", color="green"))

       for p in path:
           self._view.txt_result.controls.append(ft.Text(p))

       self._view.update_page()

