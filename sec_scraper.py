import pandas as pd
import edgar, os, requests


def download_files(path):
    """
    Returns filings made by SEC-controlled companies.
    """
    return edgar.download_index(path,2019,skip_all_present_except_last=False)


def get_filings(tsv_files, company, report):
    """
    Gets filings data from .tsv files with CSV function establishing tabs as separators.
    """
    files_list = []
    for archivo in tsv_files:
        with open("./edgar_statements/"+archivo, 'r') as arch:
            data = pd.read_csv(arch, sep='\t', lineterminator='\n', names=None)
            data.columns.values[0] = 'Items'
            companyReport = data[(data['Items'].str.contains(company)) & (data['Items'].str.contains(report))]
            filing = companyReport['Items'].str.split('|')
            filing = filing.to_list()
            for f in filing:
                files_list.append(f)
    return files_list


def html_link(filings_list):
    """
    Returns clean url links to scrap statements from selected company.
    """
    html_links = {}
    for lista in filings_list:
        
        for e in lista:    
            if 'html' in e:
                url = 'https://www.sec.gov/Archives/' + e            
                table = pd.read_html(url)[0]
                table = table['Document'][0].split(' ')

                url_formatted = url.replace('-', '').replace('index.html', '')
                html_links[lista[3]] = url_formatted+'/'+table[0] 

    return html_links


def scrap_data(links):
    '''
    Scraps SEC filings from any company to extract required financial statements.
    '''
    requested_info = {}
    for date, url in links.items():    
        data = pd.read_html(url)
        for table in data:
            table = table.dropna(how='all')
            bs = (table[0].str.contains('Retained') | table[0].str.contains('Total assets'))
            if bs.any():
                balance_sheet = table
                balance_sheet = balance_sheet.iloc[:,[0,2,6]]   # Filter items, period 1 and period 2.
                balance_sheet = balance_sheet.drop(index=3)     # Delete row with "unaudited" clarification.
                balance_sheet.columns = balance_sheet.iloc[0]   # Create columns from df lines. 
                try:
                    balance_sheet.columns.values[0] = 'Item'        # Change first column name
                except:
                    continue
                balance_sheet = balance_sheet.loc[3:,:]
                balance_sheet[balance_sheet.columns[1:]] = balance_sheet[balance_sheet.columns[1:]].astype(str)     # Convert to data to str
                balance_sheet[balance_sheet.columns[1]] = balance_sheet[balance_sheet.columns[1]].map(lambda x: x.replace('(','-'))     # Format negative numbers in col 1
                balance_sheet[balance_sheet.columns[2]] = balance_sheet[balance_sheet.columns[2]].map(lambda x: x.replace('(','-'))     # Format negative numbers in col 2
                balance_sheet[balance_sheet.columns[1]] = balance_sheet[balance_sheet.columns[1]].map(lambda x: x.replace(',',''))     # Format commas in col 1
                balance_sheet[balance_sheet.columns[2]] = balance_sheet[balance_sheet.columns[2]].map(lambda x: x.replace(',',''))     # Format commas in col 2
                balance_sheet[balance_sheet.columns[1:]] = balance_sheet[balance_sheet.columns[1:]].astype(float)     # Convert to data to float
                requested_info[date] = balance_sheet.reset_index(drop=True)
    
    return requested_info


if __name__ == '__main__':
    path = './edgar_statements/'
    download_files(path)
    reports = os.listdir(path)

    name_company = 'Alphabet Inc.'
    name_report = '10-Q'

    filings_sec = get_filings(reports, name_company, name_report)
    url_links = html_link(filings_sec)
    statements = scrap_data(url_links)
    statements['2019-04-30']
    statements['2019-07-26']
    statements['2019-10-29']   