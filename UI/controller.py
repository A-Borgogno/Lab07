from calendar import month

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.lst_result.controls.append(ft.Text(f"Umidità media su tutto l'anno", size=20, weight=ft.FontWeight.BOLD))
            ris = self._model.getUmiditaMedia(self._mese)
        else:
            self._view.lst_result.controls.append(ft.Text(f"Umidità media al mese {self._view.dd_mese.value}", size=20, weight=ft.FontWeight.BOLD))
            ris = self._model.getUmiditaMedia(self._mese)
        for r in ris:
            self._view.lst_result.controls.append(ft.Text(f"{r}: {ris[r]}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        else:
            res = self._model.getSequenza(self._mese)
            self._view.update_page()
            for r in res:
                self._view.lst_result.controls.append(ft.Text(f"{r}"))
            self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

