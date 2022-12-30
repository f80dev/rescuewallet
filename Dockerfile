#Fichier docker d'installation du serveur

#effacer toutes les images : docker rmi $(docker images -a -q)
#effacer tous les containers : docker rm  $(docker ps -a -f status=exited -q)

#install docker :
#sudo curl -sSL get.docker.com | sh
#systemctl start docker
#systemctl enable --now docker
#configurer le firewall via cockpit aver ouverture des port pour mongoDB & 6800
#dnf install -y grubby && grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0" && reboot

#renouvellement des certificats
#désactiver le parefeu puis
#Pour le server F80: certbot certonly --standalone --email hhoareau@gmail.com -d server.f80lab.com
#Pour le serveur NFluent: certbot certonly --standalone --email hhoareau@gmail.com -d api.nfluent.io
#cp /etc/letsencrypt/live/server.f80lab.com/* /root/certs

#fabrication: docker build -t f80hub/walletrescue . && docker push f80hub/walletrescue:latest
#installation: docker rm -f walletrescue && docker pull f80hub/walletrescue:latest
#Ouverture des ports : firewall-cmd --zone=public --add-port=4242/tcp
#démarrage prod : docker rm -f walletrescue && docker pull f80hub/walletrescue && docker run --restart=always -v /root/pool:/pool --name walletrescue -d f80hub/walletrescue:latest walletrescue


#Installation d'un serveur
#il faut créer les répertoire
#mkdir /root/pool

#Version pour PC
FROM python:3.9.0-buster

# set environment variables
ENV APP_HOME .

RUN export PATH="$HOME/.local/bin:$PATH"

RUN pip3 -v install cosmospy
RUN pip3 -v install osmopy
RUN pip3 -v install pyyaml
RUN pip3 -v install python-dateutil
RUN pip3 -v install pytz
RUN pip3 -v install protobuf==3.20.0

WORKDIR /

VOLUME /pool

EXPOSE 4343

COPY *.py $APP_HOME
WORKDIR $APP_HOME

CMD ["python3"]