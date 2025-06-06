import os
import sys
import requests
from bs4 import BeautifulSoup
import colorama

colorama.init()

def get_gamepass_image_urls(game_id):
    image_urls = []
    
    try:
        req = requests.get(f"https://apis.roblox.com/universes/v1/places/{game_id}/universe")
        req.raise_for_status()
        universe_id = req.json()['universeId']
        
        req = requests.get(f"https://games.roblox.com/v1/games/{universe_id}/game-passes?limit=100&sortOrder=Asc")
        req.raise_for_status()
        gamepass_data = req.json().get("data", [])
        
        for item in gamepass_data:
            if item["name"] not in ["[Removed Gamepass]", "Test"]:
                data = [{
                    "requestId": f"{item['id']}::Asset:150x150:png:regular",
                    "type": "GamePass",
                    "targetId": item['id'],
                    "format": "png",
                    "size": "150x150"
                }]
                req_url = requests.post("https://thumbnails.roblox.com/v1/batch", json=data)
                req_url.raise_for_status()
                image_url = req_url.json()['data'][0]["imageUrl"]
                image_urls.append({"name": item["name"], "url": image_url})

    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}[ERROR] {e}")
    
    return image_urls if image_urls else None

def get_game_name(game_id):
    try:
        req = requests.get(f"https://www.roblox.com/games/{game_id}")
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')
        game_title = soup.select_one("h1.game-name")
        return game_title.text.strip() if game_title else f"Game_{game_id}"
    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}[ERROR] {e}")
        return None

def download_gamepass_images(game_id, game_title):
    all_gamepasses = get_gamepass_image_urls(game_id)
    
    if not all_gamepasses:
        print(f"{colorama.Fore.YELLOW}[INFO] No GamePasses found for {game_title}.")
        return
    
    directory_path = f"output/{game_title.replace(' ', '')}"
    os.makedirs(directory_path, exist_ok=True)
    
    for gamepass in all_gamepasses:
        filename = f"{gamepass['name']}.png".replace("/", "_")
        print(f"{colorama.Fore.WHITE}[ {colorama.Fore.LIGHTGREEN_EX}DOWNLOADING {colorama.Fore.WHITE}] {colorama.Fore.LIGHTYELLOW_EX}{filename}")
        try:
            r = requests.get(gamepass["url"], allow_redirects=True)
            r.raise_for_status()
            with open(f"{directory_path}/{filename}", 'wb') as f:
                f.write(r.content)
        except requests.RequestException as e:
            print(f"{colorama.Fore.RED}[ERROR] Failed to download {gamepass['name']}: {e}")

def main():
    if len(sys.argv) < 2:
        print(f"{colorama.Fore.RED}[ERROR] Usage: python main.py <game_id>")
        sys.exit(1)
    #support multigameIds Ex: GameId: 123123,645654
    game_ids = sys.argv[1].split(",")

    for game_id in game_ids:
        game_id = game_id.strip()
        if game_id.isnumeric():
            game_title = get_game_name(game_id)
            if game_title:
                print(f"{colorama.Fore.WHITE}[ {colorama.Fore.LIGHTMAGENTA_EX}MAP {colorama.Fore.WHITE}] {colorama.Fore.LIGHTWHITE_EX}{game_title}")
                download_gamepass_images(game_id, game_title)
            else:
                print(f"{colorama.Fore.RED}[ERROR] Could not retrieve title for Game ID {game_id}")
        else:
            print(f"{colorama.Fore.RED}[ERROR] Invalid Game ID: {game_id}")

if __name__ == "__main__":
    main()
