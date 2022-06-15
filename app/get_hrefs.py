import math
import sys
import re

from bs4 import BeautifulSoup
from urllib import request

url = "https://chot.design"

f = open('parent_links.txt')
parent_links = f.read().split()

for parent_link in parent_links:
  response = request.urlopen(url+parent_link)
  soup = BeautifulSoup(response, 'html.parser')
  response.close()
  child_links = soup.find_all('a')
  f2 = open("./links/"+parent_link.replace('/','')+".txt","w")
  for child_link in child_links:
    href = child_link.get('href')
    if parent_link in href and "javascript" not in href:
      f2.write(href+"\n")
