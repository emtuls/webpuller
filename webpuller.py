#!/usr/bin/python3

# pip3 install requests
# pip3 install beautifulsoup4
import argparse
import requests
import shutil
import urllib
import sys
import os
from urllib.request import Request
from bs4 import BeautifulSoup


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", type=str, 
                        help="URL you want to pull files from.")
    parser.add_argument("-i", "--Include", type=str,
                        help="Text file that lists only files wanting to be pulled.")
    args = parser.parse_args()
    url = args.URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data)
    outDir = os.curdir + "/files/"
    os.makedirs(outDir, exist_ok=True)

    for link in soup.find_all('a'):
        fileName = link.get('href')
        fixedName = urllib.parse.unquote_plus(fileName)
        if fixedName == '../' or fixedName == url:
            continue
        if (args.Include):
            with open(args.Include, 'r') as inFile:
                files = inFile.read()
                if fixedName not in files:
                    continue
			
        req = Request(url + fileName, headers=headers)
        
        if not (outDir + fixedName).endswith('/'):          # eventually, support toggling of entering directories and pulling files from them as well...
            with urllib.request.urlopen(req) as response, open(outDir + fixedName, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
