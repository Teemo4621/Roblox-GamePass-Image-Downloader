# Roblox GamePass Image Downloader 🎮📸

This Python script allows you to download the images of GamePasses for specified Roblox games using their Game ID. You can provide one or multiple Game IDs to fetch GamePass images for each game and save them locally. 🚀

---

## Features 🌟

- Fetches the title of the game using the game ID. 🏷️  
- Downloads the GamePass images associated with the game. 📥  
- Saves the images in a structured folder format based on the game title. 📂  
- Supports multiple Game IDs input at once. 🧑‍💻  
- Error handling for network and data retrieval issues. ⚠️  
- **Supports GitHub Actions workflow to run the script directly from the GitHub UI!** ⚙️🚀  

---

## Preview 📸

![preview](./docs/images/preview.png)

---

## Requirements 📦

Before running the script locally, make sure you have the following Python packages installed:

- `requests` (for making HTTP requests) 🌐  
- `beautifulsoup4` (for parsing HTML content) 🔍  
- `colorama` (for colored output in the terminal) 🌈  

Install them with:

```sh
pip install -r requirements.txt
````

---

## Run Locally 🚀

```sh
python main.py 123456,789012,345678
```

You'll be prompted to enter one or more Game IDs separated by commas.
Or double-click the `run.bat` file (for Windows users).

---

## Run with GitHub Actions ⚙️

You can run this script directly from GitHub using **Actions > Run workflow**.

### How:

1. Go to the `Actions` tab in the repository.
2. Click on the `Run workflow` button (top right).
3. Enter the Game ID(s), separated by commas:

   ```
   123456,789012,345678
   ```
4. Click **Run workflow**.

The images will be automatically downloaded and stored in the workflow's artifacts.
You can download them from the completed workflow page. 🧾📥

---

### 💙 Made with love by ZEMONNUB
