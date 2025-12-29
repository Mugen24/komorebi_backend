docker remove m2
docker build -t "komorebi:latest" .
docker run -p 9543:9543 -e CACHE_CONFIG=1 \
       -v /media/mugen/BackupL/Games:/opt/komorebi/config/games \
       -v /media/mugen/BackupL/komorebi/:/opt/komorebi/data \
       --name "m2" -it "komorebi:latest"

