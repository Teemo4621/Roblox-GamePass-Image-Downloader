import os, requests, colorama
from bs4 import BeautifulSoup 

currentPath = os.getcwd()

gameIds = input("GameId: ")

def getGamepassImageUrl(gameId):
    imageURL = []
    req = requests.get(f"https://apis.roblox.com/universes/v1/places/{gameId}/universe")
    getUniverseId = req.json()
    req = requests.get(f"https://games.roblox.com/v1/games/{getUniverseId['universeId']}/game-passes")
    res = req.json()
    gamepassData = res["data"]
    if gamepassData:
        for i, x in enumerate(gamepassData):
            data = [{"requestId": f"{x['id']}::Asset:150x150:png:regular", "type": "GamePass", "targetId": x['id'], "format": "png", "token": "","size": "150x150"}]
            requrl = requests.post("https://thumbnails.roblox.com/v1/batch", json=data)
            resdata = requrl.json()
            imageurl = resdata['data'][0]["imageUrl"]
            imageURL.append({"name": x["name"], "url": imageurl})
    
    if len(imageURL) > 0:
        return imageURL
    else:
        return None

def getGameName(gameId):
    req = requests.get(f"https://www.roblox.com/games/{gameId}")
    if req.status_code == 200:
        res = req.text
        soup = BeautifulSoup(res, 'html.parser')
        game_title = soup.select("#game-detail-page > div.col-xs-12.section-content.game-main-content.remove-panel.follow-button-enabled > div.game-calls-to-action > div.game-title-container > h1")[0].text
        return game_title
    else:
        return None

#support multigameIds Ex: GameId: 123123 645654
loadgameIds = gameIds.split(" ")

for gameId in loadgameIds:
    os.system("cls")
    if not gameId == " " and not gameId == "" and gameId.isnumeric():
        gameTitle = getGameName(gameId)

        if gameTitle:
            print(f"{colorama.Fore.WHITE}[ {colorama.Fore.LIGHTMAGENTA_EX}MAP {colorama.Fore.WHITE}] {colorama.Fore.LIGHTWHITE_EX}{gameTitle}")
            allgamepass = getGamepassImageUrl(gameId)
            for i, v in enumerate(allgamepass):
                if not v["name"] == "[Removed Gamepass]" and not v["name"] == "Test":
                    print(f"{colorama.Fore.WHITE}[ {colorama.Fore.LIGHTGREEN_EX}DOWNLOADING {colorama.Fore.WHITE}] {colorama.Fore.LIGHTYELLOW_EX}{v['name']}.png")
                    r = requests.get(v["url"], allow_redirects=True)
                    if r.status_code == 200:
                        directory_path = f'assets\\{gameTitle.replace(" ", "")}'
                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)
                        with open(f'{directory_path}\\{v["name"]}.png', 'wb') as f:
                            f.write(r.content)