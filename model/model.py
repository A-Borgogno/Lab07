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
            for s in situazioni:
                costo = 0
                cambioPossibile = self.verificaTreGiorni(precedenti)
                if cambioPossibile:
                    pass
                else:
                    prec = precedenti[-1]
                    for i in range(0, 3):
                        if s[i].localita == prec.localita:
                            precedenti.append(s[i])
                            costo += s[i].umidita
                    self.trovaSequenza(situazioni, precedenti)
                return precedenti




    def verificaTreGiorni(self, precedenti):
        if len(precedenti) == 0:
            return True
        if len(precedenti)>=3:
            if precedenti[-1]==precedenti[-2]==precedenti[-3]:
                return True
        return False