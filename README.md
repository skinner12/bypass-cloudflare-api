# ANTI BOT APIs

This server API load a webpage blocked for bot and return HTML code.

Based on: [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

## Installation

```bash
sudo apt install -y xvfb
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo tee -a /usr/share/keyrings/linux_signing_key.pub
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
```
