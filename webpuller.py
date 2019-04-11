#!/usr/bin/python3

# pip3 install requests
# pip3 install beautifulsoup4
import requests
import shutil
import urllib
import sys
import os
from urllib.request import Request
from bs4 import BeautifulSoup


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: " + sys.argv[0] + " <URL>")
        sys.exit(1)
    url = sys.argv[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data)
    outDir = os.curdir + "/files/"
    os.makedirs(outDir, exist_ok=True)

    for link in soup.find_all('a'):
        fileName = link.get('href')
        fixedName = urllib.parse.unquote_plus(fileName)
        if (fileName == '../'):
            continue
        req = Request(url + fileName, headers=headers)

        with urllib.request.urlopen(req) as response, open(outDir + fixedName, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
