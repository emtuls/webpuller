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


def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "no":
        prompt = " [y/N] "
    elif default == "yes":
        prompt = " [Y/n]"
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", type=str, 
                        help="URL you want to pull files from.")
    parser.add_argument("-f", "--files", type=str,
                        help="Text file that lists only files wanting to be pulled.")
    parser.add_argument("-o", "--output", type=str,
                        help="Output folder you want the files to go into. Default is new folder in current directory called 'files'" )
    parser.add_argument("-t", "--tag", type=str, default="a href",
                        help="Specify the HTML tag you are looking to pull from, enclosed in \"s. Default is 'a href.'; Max 2 tags supported.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Use this flag to debug your expected output. This will not download anything.")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Use this flag to display a more verbose output.")
    args = parser.parse_args()
    url = args.URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data)

    if args.output:
        outDir = args.output
    else:
        outDir = os.curdir + "/files/"
    os.makedirs(outDir, exist_ok=True)

    if args.tag:
        if args.verbose:
            print("You supplied the tags:", args.tag)
        if len(args.tag.split(" ")) != 2:
            print("Improper number of tags specified. Please specify 2 tags (ex: \"a href\"). You supplied:", args.tag)
            sys.exit(1)
        tags = args.tag.split()
        tag1 = tags[0]
        tag2 = tags[1]
    
    if args.debug:
        debugValue = None
        debugValue = query_yes_no("Would you like to display the entire HTML Page?")
        if debugValue:
            print(soup.prettify)

    if args.debug:
        debugValue = None
        debugValue = query_yes_no("Would you like to display the expected outcome? NOTE: This will not download anything.")

    for link in soup.find_all(tag1):
        fileName = link.get(tag2)
        fixedName = urllib.parse.unquote_plus(fileName)
        if fixedName == '../' or fixedName == url:
            continue
        if (args.files):
            with open(args.files, 'r') as inFile:
                files = inFile.read()
                if fixedName not in files:
                    continue

        req = Request(url + fileName, headers=headers)
        
        if not (outDir + fixedName).endswith('/'):          # eventually, support toggling of entering directories and pulling files from them as well...
            if args.debug:
                if debugValue:
                    print(fixedName)
                continue
            if args.verbose:
                print("Downloading {} ...".format(fixedName))
            with urllib.request.urlopen(req) as response, open(outDir + fixedName, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            if args.verbose:
                print("Download Complete.")
