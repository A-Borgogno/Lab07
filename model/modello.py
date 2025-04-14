import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.n_soluzioni = 0
        self.costoOttimo = -1
        self.soluzione_ottima = []


    def getUmiditaMedia(self, month):
        return MeteoDao.getUmiditaMedia(month)


    def trova_possibili_step(self, precedenti, situazioni):
        giorno = len(precedenti)+1
        candidati = []
        for situazione in situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati


    def getSequenza(self, month):
        self.n_soluzioni = 0
        self.costoOttimo = -1
        self.soluzione_ottima = []
        situazioniMese = MeteoDao.getSituazioniMese(month)
        self._trovaSequenza(situazioniMese, [])
        return self.soluzione_ottima, self.costoOttimo


    def _trovaSequenza(self, situazioni, precedenti):
        if len(precedenti) == 15:
            self.n_soluzioni += 1
            costo = self._calcola_costo(precedenti)
            # print(f"Costo = {costo} |||| {precedenti}")
            if self.costoOttimo == -1 or self.costoOttimo > costo:
                self.costoOttimo = costo
                self.soluzione_ottima = copy.deepcopy(precedenti)
            return precedenti
        else:
            candidates = self.trova_possibili_step(precedenti, situazioni)
            for candidate in candidates:
                # verifica vincoli
                if self.is_admissible(candidate, precedenti):
                    precedenti.append(candidate)
                    self._trovaSequenza(situazioni, precedenti)
                    precedenti.pop()




            # for s in situazioni:
            #     costo = 0
            #     ss = {s: situazioni.get(s)}
            #     if self.verificaTreGiorni(precedenti):
            #         for i in range(len(ss.get(s))):
            #             precedenti.append(ss.get(s)[i])
            #             costo += ss.get(s)[i].umidita
            #             self.trovaSequenza(situazioni.pop(s), precedenti)
            #     else:
            #         prec = precedenti[-1]
            #         for i in range(len(ss.get(s))):
            #             if situazioni.get(ss)[i].localita == prec.localita:
            #                 precedenti.append(ss.get(s)[i])
            #                 costo += ss.get(s)[i].umidita
            #         # if costo < self.costoMinimo:
            #         #     self.costoMinimo = costo
            #         #     self.percorsoCorretto
            #         self.trovaSequenza(situazioni.pop(s), precedenti)
            #     return precedenti




    def is_admissible(self, candidate, precedenti):
        # vincolo sui sei giorni
        counter = 0
        for situazione in precedenti:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False

        # vincolo sulla permanenza
        # 1) lunghezza di parziale minore di 3
        if len(precedenti) == 0:
            return True
        if len(precedenti) < 3:
            return candidate.localita == precedenti[0].localita
        # 2) le tre situazioni precedenti non sono uguali
        else:
            if not precedenti[-1].localita == precedenti[-2].localita == precedenti[-3].localita:
                return candidate.localita == precedenti[-1].localita

        # altrimenti okay
        return True

        # if len(precedenti) == 0:
        #     return True
        # if len(precedenti)>=3:
        #     if precedenti[-1]==precedenti[-2]==precedenti[-3]:
        #         return True
        # return False

    def _calcola_costo(self, precedenti):
        costo = 0
        # 1) costo umidità
        for situazione in precedenti:
            costo += situazione.umidita

        # 2) costo su spostamenti
        for i in range(3, len(precedenti)):
            if not precedenti[i-1].localita == precedenti[i-2].localita == precedenti[i].localita:
                costo += 100
        return costo



if __name__ == '__main__':
    my_model = Model()
    print(my_model.getSequenza(2))