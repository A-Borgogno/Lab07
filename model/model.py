from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass


    def getUmiditaMedia(self, month):
        return MeteoDao.getUmiditaMedia(month)

    def getSequenza(self, month):
        situazioniMese = MeteoDao.getSituazioniMese(month)
        return self.trovaSequenza(situazioniMese, [])

    def trovaSequenza(self, situazioni, precedenti):
        if len(precedenti) == 15:
            return precedenti
        else:
            if len(precedenti) == 0:
                for s in situazioni:
                    costo = 0
                    for i in range(0, 3):
                        precedenti.append(s[i])
                        costo += s[i].umidita
                        self.trovaSequenza(situazioni, precedenti)
            for s in situazioni:
                costo = 0
                (treGiorni, prec) = self.verificaTreGiorni(precedenti)
                if not treGiorni:
                    for i in range(0, 3):
                        if s[i].localita == prec.localita:
                            precedenti.append(s[i])
                            costo += s[i].umidita
                self.trovaSequenza(situazioni, precedenti)
            return precedenti





    def verificaTreGiorni(self, precedenti):
        if precedenti[-1]==precedenti[-2] and precedenti[-2]==precedenti[-3]:
            return True, precedenti[-1]
        return False, precedenti[-1]