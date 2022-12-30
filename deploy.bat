echo "Mise en place du serveur"
docker build -t f80hub/walletrescue .
docker push f80hub/walletrescue:latest

putty -pw %1 -ssh root@173.249.41.158 -m "install_server.txt"

echo "Traitement terminé"
