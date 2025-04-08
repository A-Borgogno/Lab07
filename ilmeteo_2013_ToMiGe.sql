select Localita, sum(Umidita)/count(*) 
from situazione s
where month(`Data`) = 02
group by Localita