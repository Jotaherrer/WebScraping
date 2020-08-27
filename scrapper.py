from urllib import *
import datetime as dt
import pandas as pd
import os, time, urllib, xlwings as xw
from bs4 import BeautifulSoup

link = 'https://finance.yahoo.com/'
link_stock = 'https://finance.yahoo.com/quote/AAPL?p=AAPL'

"""
Pasos:
1) Import urllib
2) Request al servidor de destino
3) Indicar cual es el servidor de destino y abrirlo
4) Leer el codigo HTML de la pag. destino.
5) Codificarlo en UTF-8
"""
link_handler = urllib.request.urlopen(link).read().decode('utf-8')

user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
request = urllib.request.Request(link, headers=headers)
with urllib.request.urlopen(request) as response:
    html = response.read()

##### BEAUTIFUL SOUP ==> IMG scrapper
"""
Pasos:
1) Import html code.
2) Find specific structures to scrap (header, title, imgs)
3) Loop across them to find data.
4) Download data in any format (.txt for example)
"""
yf_soup = BeautifulSoup(html, 'lxml')
#yf_soup.title
#yf_soup.find_all('a')

images = yf_soup.find_all("img")
img_titles = []
img_links = []
for img in images:
    attributes = img.attrs
    title = attributes['alt']
    img_titles.append(title)

    image = attributes['src']
    img_links.append(image)

salida = open('img_links', 'a')
with open('img_links.txt', 'a') as links:
    for text in img_links:
        links.write(text)
        links.write('\n')

with open('img_links.txt', 'a') as imgs:
    for img in img_titles:
        imgs.write(img)
        imgs.write('\n')

### GENERAL CASE

def create_url(stock):
    """
    Creates a URL to search from a stock ticker.
    """
    url_model = 'https://finance.yahoo.com/quote/'+str(stock)+'?p='+str(stock)
    return url_model

def get_html_code(url):
    """
    Pass URL string to obtain HTML Code.
    """
    user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as resp:
        code = resp.read()
    stock_info = BeautifulSoup(code, 'lxml')
    return stock_info

def get_tables_data(html):
    """
    Parses HTML code to obtain relevant financial metrics. Returns a 
    zipped list.
    """
    table_1 = html.find_all('table')[0].find_all('tr')
    table_2 = html.find_all('table')[1].find_all('tr')

    data = []
    for num in range(len(table_1)):
        try:
            info_span = table_1[num].find_all('span')
            info_td = table_1[num].find_all('td')
            for n in range(0,1):
                if len(table_1[num].find_all('span')) > 1:
                    item, value = info_span[n].text, info_span[n+1].text
                    data.append((item, value))
                else:
                    item, value = info_td[n].text, info_td[n+1].text
                    data.append((item,value))
        except:
            print('error en ejecucion')

    for num in range(len(table_2)):
        try:
            info_span = table_2[num].find_all('span')
            info_td = table_2[num].find_all('td')
            for n in range(0,1):
                if len(table_2[num].find_all('span')) > 1:
                    item, value = info_span[n].text, info_span[n+1].text
                    data.append((item, value))
                else:
                    item, value = info_td[n].text, info_td[n+1].text
                    data.append((item,value))
        except:
            print('error en ejecucion')

    data_dic = {}
    for item, value in data:
        try:
            data_dic[item] = float(value)
        except:
            data_dic[item] = value
    return data_dic

def restore_values(data):
    """
    Extracts and formats data from the input dictionary.
    """
    find_dy = data['Forward Dividend & Yield'].find('(')

    if data['Market Cap'].endswith('B'):
        if len(data['Market Cap']) == 7:
            find = data['Market Cap'].find('B')
            mkt_cap = data['Market Cap'][:find]
            mkt_cap = float(mkt_cap.replace('.', '')) * 1000000
        elif len(data['Market Cap']) == 8:
            find = data['Market Cap'].find('B')
            mkt_cap = data['Market Cap'][:find]
            mkt_cap = float(mkt_cap.replace('.', '')) * 1000000
        elif len(data['Market Cap']) < 7:
            find = data['Market Cap'].find('B')
            mkt_cap = data['Market Cap'][:find]
            mkt_cap = float(mkt_cap.replace('.', '')) * 1000000

    elif data['Market Cap'].endswith('T'):
        find = data['Market Cap'].find('T')
        mkt_cap = data['Market Cap'][:find]
        mkt_cap = float(mkt_cap.replace('.', '')) * 1000000000

    else:
        mkt_cap = data['Market Cap'][:-1]
        mkt_cap = float(mkt_cap.replace('.', '')) * 1000
    
    beta = data['Beta (5Y Monthly)']
    pe = data['PE Ratio (TTM)']
    eps = data['EPS (TTM)']
    try:
        dy = float(data['Forward Dividend & Yield'][:find_dy].strip())
    except:
        pass
    tg = data['1y Target Est']
    keys = ['Market Cap', '5Y Beta', 'PE Ratio', 'EPS', 'Div. Yield',
            'Target 1Y']
    try:
        values = [mkt_cap,beta,pe,eps,dy,tg]
    except:
        values = [mkt_cap,beta,pe,eps,tg]
    return list(zip(keys,values))

def excel_export(df):
    """
    Function that exports dataframe of actual prices to an excel file. Pass a dataframe from Pandas module to run.
    """
    if os.path.exists('Ratios.xlsx'):
        wb = xw.Book('Ratios.xlsx')
        ws = wb.sheets('Datos')
        ws.range('A1').expand().value = df
        tiempo = time.asctime()
        print('Carga exitosa de datos. Ultima ejecucion: ',tiempo)

stocks = ['BABA', 'TSLA', 'AAPL', 'MSFT', 'GGAL', 'ROKU', 'PFE', 'NIO','PAM','FB','PBR', 'MELI',
           'NFLX', 'AMD', 'NVDA','GLOB', 'YPF', 'CVX', 'XOM', 'NKE', 'SHOP', 'BBD', 'JPM']
           
data = {}
for stock in stocks:
    url = create_url(stock)
    code = get_html_code(url)
    table = get_tables_data(code)
    values = restore_values(table)
    data[stock] = values

cols = []
vals = []
for k,v in data.items():
    for i in range(len(v)):
        values = v[i][0]
        vals.append((k,v[i][1]))
        if values in cols:
            continue
        else:
            cols.append((k, values))

df_col = pd.DataFrame(cols)
df_val = pd.DataFrame(vals)
df_val.rename(columns={1:'values',0:'Ticker'},inplace=True)
df_col.rename(columns={1:'Item',0:'Ticker'},inplace=True)
df_col['values'] = df_val['values']
df_col.sort_values('Ticker', ascending=True)
pivot_table = pd.pivot(data=df_col, columns='Item', values='values', index='Ticker')

excel_export(pivot_table)
