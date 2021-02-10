import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import time
import os

path = "pastes\\"
# just so bot doesnt get locked out
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

while True:
    alarchives = []

    with open("alarchives.txt", "a+") as falarchives:
        text = falarchives.read()
    alarchives = text.split("\n")
    falarchives.close()


    #check the archived posts
    pastebin = requests.get("https://pastebin.com/archive", headers)

    #find all links to pastebin.com's pastes
    archive = BeautifulSoup(pastebin.content, 'html.parser')
    findarchive = archive.find_all("a", href=True)
    pastecount = 0
    archives = []
    # take the ones that dont start with /about/ or are for other matters
    for x in findarchive:
        pastecount += 1
        print(f"Paste #{pastecount}: {x['href']}")
        print("#"*25)
        a = x['href']
        if len(a) == 9:
            archives.append(a)

    #Just to print out the paste urls
    print("\n\n\n")
    for y in archives:
        print("#"*25)
        print(f"Paste link: {y}")
    print("#"*25)
    print("\n\n\n")
    print("#"*25)


    # Get the raw data for each entry in the archives
    for j in archives:
        if j not in alarchives:
            alarchives.append(j)
        elif j in alarchives:
            continue
        url = "https://pastebin.com" + str(j)
        paste = requests.get(url)
        getpaste = BeautifulSoup(paste.content, "html.parser")
        rawpaste = getpaste.find(class_="textarea", text=True)
        pastefile = j[1:]
        
        with open(path+pastefile+".txt", "wb") as pfile:
            pfile.write(rawpaste.encode("utf-8"))
        pfile.close()


    with open('alarchives.txt', 'w') as falarchives:
        for item in alarchives:
            falarchives.write("%s\n" % item)
    falarchives.close()
    time.sleep(60)
