

import requests
from bs4 import BeautifulSoup
s = requests.Session()
salary_list =[]
ITEMS = 100
URL = f'https://hh.ru/search/vacancy?st=searchVacancy&text=python&items_on_page={ITEMS}'
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
headers = {
    'Host': 'hh.ru',
    'Connection': 'keep-alive',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    #'max_redirects': '50'
}


def session():
    r = s.get(URL)# headers=headers)#,headers=headers),#allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    pages = []
    soup_soup = soup.find_all("div",{"class":"magritte-text___pbpft_3-0-22 magritte-text_style-primary___AQ7MW_3-0-22 magritte-text_typography-label-2-regular___ia7GB_3-0-22"})
    for page in soup_soup:
        if page.text.isnumeric():
            pages.append(int(page.text))
    return pages[-1]


def extract_job(html):

    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('span', {
        "class": "magritte-text___pbpft_3-0-22 magritte-text_style-primary___AQ7MW_3-0-22 magritte-text_typography-label-3-regular___Nhtlp_3-0-22"}).find(
        "span").text
    if 'ООО\xa0' in company:
        company = company.replace('\xa0', '')
    company = company.strip()
    town = html.find("span", {'data-qa':"vacancy-serp__vacancy-address"}).text
    town = town.strip()
    salary = html.find_all("span", {'class':"magritte-text___pbpft_3-0-22 magritte-text_style-primary___AQ7MW_3-0-22 magritte-text_typography-label-1-regular___pi3R-_3-0-22"})
    for page in salary:
        salary = page.text
        if '\u202f' in salary:
            salary = salary.replace('\u202f', '')
        if '\xa0' in salary:
            salary = salary.replace('\xa0', ' ')
    return {'title': title, 'company': company, 'town': town,'link': link,"salary": salary }


def extract_hh(last_page):
    last_page = 20
    jobs = []
    for page in range(last_page):
        result = s.get(f'{URL}&page={page}')
        soup = BeautifulSoup(result.text, 'html.parser')
        soup_soup = soup.find_all("div", {'class':"magritte-redesign"})
        for Job in soup_soup:
            job = extract_job(Job)
            jobs.append(job)
    return jobs

def get_jobs():
    max_page = session()
    jobs = extract_hh(max_page)
    return jobs