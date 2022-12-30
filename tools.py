import datetime
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import exists

import dateutil.tz
import pytz
import yaml
from dateutil.tz import gettz

from privacy import USERNAME, PASSWORD

SMTP_SERVER="ssl0.ovh.net"
SMTP_SERVER_PORT=587
IMAP_SERVER="imap.ionos.fr"
STATIC_FOLDER="./"
APPNAME="RescueWallet"

def open_html_file(name:str,replace=dict(),domain_appli="",directory=STATIC_FOLDER):
    """
    ouvre un fichier html et remplace le code avec le dictionnaire de remplacement
    :param name:
    :param replace:
    :param domain_appli:
    :return:
    """
    if len(name)>10 and len(name.split(" "))>5:
        body=name
    else:
        if not name.endswith("html"):name=name+".html"
        if exists(directory+name):
            with open(directory+name, 'r', encoding='utf-8') as f: body = f.read()
        else:
            log("Le mail type "+name+" n'existe pas")
            return None

    style="""
        <style>
        .button {
         border: none;
         background: #d9d9d9;
         color: #fff;
         padding: 10px;
         display: inline-block;
         margin: 10px 0px;
         font-family: Helvetica, Arial, sans-serif;
         font-weight: lighter;
         font-size: large;
         -webkit-border-radius: 3px;
         -moz-border-radius: 3px;
         border-radius: 3px;
         text-decoration: none;
        }

     .button:hover {
        color: #fff;
        background: #666;
     }
    </style>
    """

    replace["appname"]=APPNAME
    replace["appdomain"]=domain_appli

    for k in list(replace.keys()):
        body=body.replace("{{"+k+"}}",str(replace.get(k)))

    body=body.replace("</head>",style+"</head>")

    return body

def is_email(addr):
    if addr is None:return False
    if len(addr)==0 or not "@" in addr:return False
    return True


def send_mail(body:str,_to="paul.dudule@gmail.com",_from:str="contact@nfluent.io",subject="",attach=None,filename=""):
    if body is None or not is_email(_to):return False
    with smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT,timeout=10) as server:
        server.ehlo()
        server.starttls()
        try:
            log("Tentative de connexion au serveur de messagerie")
            server.login(USERNAME, PASSWORD)
            log("Connexion réussie. Tentative d'envoi")

            msg = MIMEMultipart()
            msg.set_charset("utf-8")
            msg['From'] = _from
            msg['To'] = _to
            msg['Subject'] = subject
            msg.attach(MIMEText(body,"html"))

            if not attach is None:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(attach)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',"attachment",filename=filename)
                msg.attach(part)

            log("Send to "+_to+" <br><div style='font-size:x-small;max-height:300px>"+body+"</div>'")
            server.sendmail(msg=msg.as_string(), from_addr=_from, to_addrs=[_to])
            return True
        except Exception as inst:
            log("Echec de fonctionement du mail"+str(type(inst))+str(inst.args))
            return False


def now(format="dec", tz=dateutil.tz.gettz("Europe/Paris")):
    rc=datetime.datetime.now(tz=tz).timestamp()
    if format=="dt" or format=="datetime" or format=="date": rc=datetime.datetime.now(tz=tz)
    if format=="hex": rc=hex(int(rc*100000)).replace("0x","")
    if format=="str":
        rc=datetime.datetime.strftime(datetime.datetime.now(tz=tz),"%d/%m %H:%M")
    return rc


def get_config(validator_name="allthatnode"):
    rc=yaml.load(open("./config.yaml","r"),yaml.FullLoader)
    return rc["validators"][validator_name]


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