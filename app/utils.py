import datetime as dt
from typing import Tuple

def get_sonar_timestamp(date_str:str,delta: Tuple[int]):
        datetime_obj = dt.datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S')
        h,m,s = delta
        datetime_obj += dt.timedelta(hours=h,minutes=m,seconds=s,milliseconds=0)
        str_date = datetime_obj.isoformat()+'.00'
        datetime_obj = dt.datetime.strptime(str_date,'%Y-%m-%dT%H:%M:%S.%f')
        return datetime_obj.timestamp()
    
def get_gps_timestamp(date_str:str, time_str:str):
    time_str,ff = time_str.split('.')
    hh,mm,ss = map(lambda i: int(i),time_str.split(':'))
    h,m,s = time_str.split(':')
    if ss == 60:
        s= '00'
        mm = mm + 1
        m = str(mm)
        if mm == 60:
            m = '00'
            hh+=1
            h = str(h)
    time_part = ':'.join([h,m,s])
    time_str = time_part+'.'+ff
    datetime_str = dt.datetime.strptime(date_str+ ' '+time_str,'%Y.%m.%d %H:%M:%S.%f')
    return datetime_str.timestamp()