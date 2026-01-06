https://store.steampowered.com/api/packagedetails?packageids=1145350
https://github.com/Revadike/InternalSteamWebAPI/wiki
https://store.steampowered.com/api/appdetails?appids=1145350
https://store.steampowered.com/api/storesearch/?term=hades&cc=us&l=en=
https://gamedevtools.net/steam-app-id-finder/


steamcmd: 
https://github.com/dgibbs64/SteamCMD-Commands-List/blob/main/steamcmd_commands.txt



#image fetch
`
https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/capsule_616x353.jpg
https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/capsule_231x87.jpg
https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/header.jpg


https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/library_600x900_2x.jpg
- Game Cover

https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/library_hero.jpg
- Game Page Background

https://steamcdn-a.akamaihd.net/steam/apps/APP_ID/logo.png
- hGame Logo (transparent)

`

# steam images explaination
https://noblesteedgames.com/blog/a-handy-guide-to-graphical-assets-on-your-steam-store-page/

#BUGS:
   Minds beneath us: 1610440
   has no named launch option but it does have 
   an unamed lauch option that does not show up in package detail but does on steamdb

   The wolf among use cannot find exe (steam game)

   - smarter executae finding algo sometimes steam path is wrong because if from a different game store
   - Look for only folder in /Games and ignore .XXX files



#TODO:
 - Implementing config for non steam game  (P1)
 - Implementing a hash system for file downloading
 - Save file backup (check test.json)
 ```
        this return key ufs that has save file location

        def get_game_configuration(self, app_id: int):
 ```
 - Automatic dependency download through steam depo (check test.json)


 - Generate zip archive using thread in the background instead of when fetching

 - Can probably default to option 0 when searching for game appid

 - Fall back directory is being prioritise, should go with any working_dir provided first

 - Threading: 
    - zip process
    - game look up 
    - image downloading 
    - etc

 - Added a stub for evaluated game that fails and don't need to be retry

 - Give a way to change game folder name on scan and rerun it again with steam

 - Dynamically determine optimal download speed using network + disk read



#DOCKER
docker build -t "komorebi:latest" .
docker run -p 9543:9543 -e CACHE_CONFIG=0 -v /media/mugen/BackupL/Games:/opt/komorebi/config/games --name "m2" -it "komorebi:latest"
docker run -p 9543:9543 -e CACHE_CONFIG=1 \
       -v /media/mugen/BackupL/Games:/opt/komorebi/config/games \
       -v /media/mugen/BackupL/komorebi/:/opt/komorebi/data \
       --memory="5g"
       --name "m2" -it "komorebi:latest"

CACHE_CONFIG=1






# Give up on multi threading download hdd limited + overhead even on GIL disabled python3.14
# Make endpoint async io may increase speed  
# Improve compression algo zip_lzma is bester
# allowzip64


