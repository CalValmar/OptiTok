from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from urllib.request import urlopen
from colorama import Fore, Style
from bs4 import BeautifulSoup
import argparse
import requests
import json
import time
import os

def banner():
    banner = """
     ____        __  _ ______      __               _____                                
    / __ \____  / /_(_)_  __/___  / /__            / ___/______________ _____  ___  _____
   / / / / __ \/ __/ / / / / __ \/ //_/  ______    \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
  / /_/ / /_/ / /_/ / / / / /_/ / ,<    /_____/   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
  \____/ .___/\__/_/ /_/  \____/_/|_|            /____/\___/_/   \__,_/ .___/\___/_/     
      /_/                                                            /_/                  
    """
        
    info = """
 Github  : https://github.com/CalValmar
 Author  : Valmar
 Version : 1.1 
 """
    
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + banner + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + info + Style.RESET_ALL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_config():
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + " [~] Loading config file..." + Style.RESET_ALL)
    if not os.path.exists('config.json'):
        print(Fore.LIGHTRED_EX + Style.BRIGHT + " [!] Config file not found, creating a new one..." + Style.RESET_ALL)
        config = {
            'default_username': 'tiktok',
            'default_directory': 'videos',
            'cookies': {},
            'headers': {},
            'params': {},
            'data': {}
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + " [+] Config file created successfully!\n" + Style.RESET_ALL)
    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + " [+] Config file loaded successfully!\n" + Style.RESET_ALL)
    return config

def setup_driver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scroll_page(driver, scroll_pause_time):
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

def extract_video_urls(driver, className):
    script  = "let l = [];"
    script += "Array.from(document.getElementsByClassName(\""
    script += className
    script += "\")).forEach(item => { l.push(item.querySelector('a').href)});"
    script += "return l;"
    urlsToDownload = driver.execute_script(script)
    return urlsToDownload

def download_video(link, id, user):
    data = {
        'id': link,
        'locale': config['data']['locale'],
        'tt': config['data']['tt'],
    }
    try:
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()) + Fore.LIGHTGREEN_EX + f" [{id}] Downloading video" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + " : " + Style.RESET_ALL + link)
        
        cookies = config['cookies']
        headers = config['headers']
        params = config['params']
        data = {
            'id': link,
            'locale': config['data']['locale'],
            'tt': config['data']['tt'],
        }
        
        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
        downloadSoup = BeautifulSoup(response.text, "html.parser")

        downloadLink = downloadSoup.a["href"]
        videoTitle = downloadSoup.p.getText().strip()
        
        mp4File = urlopen(downloadLink)
        with open(f"videos/{user}/{id}-{videoTitle}.mp4", "wb") as output:
            while True:
                data = mp4File.read(4096)
                if data:
                    output.write(data)
                else:
                    break
        return True
    except Exception as e:
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()) + Fore.RED + f" [{id}] Error downloading" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + " : " + Style.RESET_ALL + link)
        print(Fore.RED + Style.BRIGHT + "Error: " + Style.RESET_ALL + str(e))
        return False
    
def main(user):
    try:
        default_directory = config['default_directory']

        if not os.path.exists(f'{default_directory}/{user}'):
            os.makedirs(f'{default_directory}/{user}')

        time.sleep(2)
        driver = setup_driver()
        driver.get(f"https://www.tiktok.com/@{user}")
        time.sleep(5)

        scroll_page(driver, scroll_pause_time=2)
        time.sleep(3)
        
        urlsToDownload = extract_video_urls(driver, className=" css-at0k0c-DivWrapper") # Make sure to change this class name if TikTok changes it
        
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "     +" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=================================================" + Fore.LIGHTBLUE_EX + Style.BRIGHT + "+")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"       Found " + Fore.LIGHTYELLOW_EX + Style.BRIGHT + str(len(urlsToDownload)) + Fore.LIGHTBLUE_EX + Style.BRIGHT + f" videos to download from " + Fore.LIGHTYELLOW_EX + Style.BRIGHT + user)
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "     +" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=================================================" + Fore.LIGHTBLUE_EX + Style.BRIGHT + "+\n")
        
        for index, url in enumerate(urlsToDownload):
            files = os.listdir(f'{default_directory}/{user}')
            if any(file.startswith(f"{index+1}") for file in files):
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()) + Fore.LIGHTCYAN_EX + f" [{index+1}] Video already downloaded" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + " : " + Style.RESET_ALL + url)
                continue
            time.sleep(10) # 10 seconds sleep to avoid getting blocked by TikTok
            download_video(url, index+1, user)
            
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "     +" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=================================" + Fore.LIGHTBLUE_EX + Style.BRIGHT + "+")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "       " + Fore.LIGHTBLUE_EX + Style.BRIGHT + "All videos have been downloaded" + Fore.LIGHTBLUE_EX + Style.BRIGHT)
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "     +" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=================================" + Fore.LIGHTBLUE_EX + Style.BRIGHT + "+")
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n" + " [!] Exiting script..." + Style.RESET_ALL)

if __name__ == "__main__":
    clear_screen()
    banner()
    
    config = load_config()
    default_username = config['default_username']
    
    parser = argparse.ArgumentParser(description='TikTok Video Scraper')
    parser.add_argument('--user', default=default_username, help='Username to scrape videos from')
    args = parser.parse_args()

    main(args.user)