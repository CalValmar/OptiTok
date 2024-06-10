# OptiTok - TikTok Video Scraper

OptiTok is a Python script that scrapes and downloads videos from a specified TikTok user's profile.

![Made withPython 3.10](https://img.shields.io/badge/Made%20with-Python%203.10-1f425f.svg)


## Features

- Scrape video URLs from a TikTok user's profile
- Download videos directly to your local machine
- Skip downloading videos that have already been downloaded
- Handle errors and exceptions during the download process

## Demonstration
![demo](/src/demo.mp4)

## Installation

You can install the project by cloning the repository and by running the following command:
```
git clone https://github.com/CalValmar/OptiTok.git
```

And don't forget to install the required Python packages :
```
pip install -r requirements.txt
```

Make sure you have downloaded [ChromeDriver](https://www.google.com/chrome/).

## Configuration

This step is mandatory to run the script. The file `config.json` is created when you run the script for the first time. You need to setup the configuration file `config.json` with the following information:

```json
{
    "default_username": "tiktok",
    "default_directory": "videos",
    "cookies": {},
    "headers": {},
    "params": {},
    "data": {}
}
```

Follow this guide to get the cookies, headers, params, and data:
![Guide](/src/guide.mp4)

Exemple of a filled configuration file: (Don't copy this, it's an example)

```json
{
    "default_username": "tiktok",
    "default_directory": "videos",
    "cookies": {
        "cf_clearance": "a7VMw0HGnkfav1QJq2Xlm.Lo3rUfYwr_PTLr69c-171620911-1.0.1.1-5vKdq55Qj52tQllDfKrJo8F.hBOOltm5WATDKQEq_C8lM0EI11HWt.TFuf5Mjm2RbKNkQXKHeHqQUpLg"
    },
    "headers": {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "hx-current-url": "https://ssstik.io/",
        "hx-request": "true",
        "hx-target": "target",
        "hx-trigger": "_gcaptcha_pt",
        "origin": "https://ssstik.io",
        "priority": "u=1, i",
        "referer": "https://ssstik.io/",
        "sec-ch-ua": "\"Chromium\";v=\"125\", \"Brave\";v=\"125\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-ch-ua-platform-version": "\"6.5.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    },
    "params": {
        "url": "dl"
    },
    "data": {
        "id": "", // don't touch this
        "locale": "en",
        "tt": "WkRzUmY1"
    }
}
```

## Usage

Run the script with the TikTok username as an argument: 
(If no username is provided, the script will use the default username specified in the configuration file)

```bash
python3 Scraper/OptiTok_Scraper.py [-h] [--user USER]
```
options:
-  `-h, --help`  :  Show this help message and exit
-  `--user USER` :  Username to scrape videos from

The script will scrape the video URLs from the user's profile, download the videos, and save them in a `videos/<username>` directory.

You can change the default download directory / username by changing the values in the configuration file `config.json`.

```json
{
    "default_username": "tiktok",
    "default_directory": "videos"
}
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](/LICENSE) file for details.

GNU General Public License v3.0 © [CalValmar](https://github.com/CalValmar)

## Inspirations and Additional Information
- [Codewithvincent1](https://github.com/codewithvincent1/tiktokVideoScraper/blob/main/scrape_video.py)
- [TikTok Video Downloader](https://ssstik.io/)
- [Curl Converter](https://curlconverter.com/)