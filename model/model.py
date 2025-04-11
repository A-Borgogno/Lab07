from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.costoMinimo = 100000000000


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
                ss = {s: situazioni.get(s)}
                if self.verificaTreGiorni(precedenti):
                    for i in range(len(ss.get(s))):
                        precedenti.append(ss.get(s)[i])
                        costo += ss.get(s)[i].umidita
                        self.trovaSequenza(situazioni.pop(s), precedenti)
                else:
                    prec = precedenti[-1]
                    for i in range(len(ss.get(s))):
                        if situazioni.get(ss)[i].localita == prec.localita:
                            precedenti.append(ss.get(s)[i])
                            costo += ss.get(s)[i].umidita
                    # if costo < self.costoMinimo:
                    #     self.costoMinimo = costo
                    #     self.percorsoCorretto
                    self.trovaSequenza(situazioni.pop(s), precedenti)
                return precedenti




    def verificaTreGiorni(self, precedenti):
        if len(precedenti) == 0:
            return True
        if len(precedenti)>=3:
            if precedenti[-1]==precedenti[-2]==precedenti[-3]:
                return True
        return False