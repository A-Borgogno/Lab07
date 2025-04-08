from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def getSituazioniMese(month):
        cnx = DBConnect.get_connection()
        result = []
        diz = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = f"select Localita, `Data`, Umidita from situazione s where day(`Data`)<16 and month(`Data`) = {month} order by Data"
            cursor.execute(query,)
            for row in cursor:
                s = Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"])
                result.append(s)
                if row["Data"] not in diz.keys():
                    diz[row["Data"]] = [s]
                else:
                    diz[row["Data"]].append(s)
                print(diz)
            cursor.close()
            cnx.close()
        return diz


    @staticmethod
    def getUmiditaMedia(month):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "select Localita, sum(Umidita)/count(*) as Media from situazione s"
        if month == 0:
            query += f" group by Localita"
        else:
            query += f" where month(`Data`) = {month} group by Localita"
        cursor.execute(query)
        risultati = {}
        for row in cursor.fetchall():
            risultati[row["Localita"]] = row["Media"]
        cursor.close()
        cnx.close()
        return risultati
