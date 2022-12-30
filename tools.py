import datetime

import dateutil.tz
import pytz
from dateutil.tz import gettz


def now(format="dec", tz=dateutil.tz.gettz("Europe/Paris")):
    rc=datetime.datetime.now(tz=tz).timestamp()
    if format=="dt" or format=="datetime" or format=="date": rc=datetime.datetime.now(tz=tz)
    if format=="hex": rc=hex(int(rc*100000)).replace("0x","")
    if format=="str":
        rc=datetime.datetime.strftime(datetime.datetime.now(tz=tz),"%d/%m %H:%M")
    return rc


def convert_date(dt:str):
    if type(dt)==str:
        if ":" in dt and not ("-" in dt or "/" in dt):
            if len(dt.split(":"))<3: dt=dt+":00"
            dt=datetime.datetime.strftime(now("dt"),"%Y-%m-%d")+" "+dt

        if "/" in dt:
            dt=datetime.datetime.strptime(dt,"%d/%m/%Y %H:%M:%S")
        else:
            if "-" in dt:
                dt=datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")

    if type(dt)==float: return dt
    return dt.timestamp()


def transaction_to_str(transaction:dict):
    rc=""
    if "result" in transaction["transaction"]:
        result=transaction["transaction"]["result"]
        if result["code"]==0:
            rc="Transaction: "+result["hash"]
        else:
            rc=str(result["code"])+" - "+result["log"]

    return rc



start=now()
store_log=""
def log(text:str,sep='\n',raise_exception=False):
    global store_log
    if text.startswith("\n"):
        print("\n\n")
        text=text[1:]

    delay=int(now()-start)
    line:str=str(int(delay/60))+":"+str(delay % 60)+" : "+text
    try:
        print(line)
    except:
        print("Problème d'affichage d'une ligne")
    store_log = line+sep+store_log[0:10000]
    if raise_exception:raise RuntimeError(text)
    return text


def toDate(n:float):
    return datetime.datetime.fromtimestamp(n).strftime("%d/%m %H:%M")