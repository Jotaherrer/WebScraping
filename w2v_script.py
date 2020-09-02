import urllib
import requests
from random import randrange
from bs4 import BeautifulSoup

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter

def html_code(n_notes):    
    codes = {}
    for note in range(2400001,2400001+n_notes):
        try:
            url = f'https://www.lanacion.com.ar/{note}'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
            req_result = urllib.request.urlopen(req)
            raw = req_result.read().decode('utf-8')
            clean_url = req_result.geturl()
            codes[str(note)] = raw
            if note % 10 == 0:
                print(f'Printing note number: {note}')
        except:
            continue
    return codes


def get_text(html_dictionary):
    content = {}
    for n, code in html_dictionary.items():
        soup = BeautifulSoup(code, 'lxml')
        try:
            print(f'Begin printing {n}')
            text = soup.find_all('section',id='cuerpo')
            text = text[0].find_all('p') 
            print(f'succesfully processed {n} with id == cuerpo')
        except IndexError:
            try:
                print(f'Begin printing {n}')
                text = soup.find_all('div', class_='cuerpo__nota')
                text = text[0].find_all('p') 
                print(f'succesfully processed {n} with class == cuerpo__nota')
            except:
                continue
        text = [texto.text.strip() for texto in text]
        text = ','.join(text).strip()
        text = text.replace('\r\n', ' ')
        text = text.replace("\'","")
        text = text.replace('(...)',".")
        text = text.replace('.,', '.')
        text = text.replace(' , ', '')        
        text = ' '.join(text.split())
        content[str(n)] = text            
    return content


if __name__ == "__main__":
    last_note_number = 2436886    # Ultimo ID de nota de LN
    number_pages = 1000
    htmls = html_code(number_pages)
    # test note number: 188160
    textos = get_text(htmls)
