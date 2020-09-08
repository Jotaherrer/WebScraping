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


def html_code(filings_list):
    """
    Returns clean url links to scrap statements from selected company.
    """
    html_codes = {}
    for lista in filings_list:
        
        for e in lista:    
            if 'html' in e:
                url = 'https://www.sec.gov/Archives/' + e            
                table = pd.read_html(url)[0]
                table = table['Document'][0].split(' ')

                url_formatted = url.replace('-', '').replace('index.html', '')
                html_codes[lista[3]] = url_formatted+table[0] 

    return html_codes



if __name__ == '__main__':
    path = './edgar_statements/'
    download_files(path)
    reports = os.listdir(path)

    name_company = 'Alphabet Inc.'
    name_report = '10-Q'

    filings_sec = get_filings(reports, name_company, name_report)
    url_links = html_code(filings_sec)