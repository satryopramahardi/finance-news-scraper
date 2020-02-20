import requests
from bs4 import BeautifulSoup
import json

#Global variables
urls = {
    'tribun':['https://www.tribunnews.com/tag/finansial',{"class": "fbo f18 ln24"}],
    'tempo':['https://www.tempo.co/tag/finansial',{'class':'article__link'}],
    'liputan6':['https://www.liputan6.com/tag/finansial',{'class':'ui--a articles--iridescent-list--text-item__title-link'}],
    'detik':['https://www.detik.com/tag/finansial',{'h2'}],
    'merdeka':['https://www.merdeka.com/tag/finance',{}],
    'kompas':['https://www.kompas.com/tag/finansial',{'class':'article__link'}],
    'viva':['https://www.viva.co.id/tag/finansial',{"h3"}]
    }

global_id_counter = 1

def increase_counter():
    global global_id_counter
    global_id_counter += 1


def scrape_kompas(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page={page}'
    response = requests.get(passurl,allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all(attrs={'class':'article__link'})
    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        print(f'{global_id_counter} news processed')
        increase_counter()
        if my_dict != 0:
            headline_list.append(my_dict)
        else:
            pass
    if headlines != []:
        page += 1
        scrape_kompas(inp,page,headline_list)
    else:
        pass
    return headline_list

def scrape_merdeka(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'/index{page}'
    response = requests.get(passurl,allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        headlines = soup.find(attrs={'class':'mdk-tagdet-content'}).find_all('a')
        for headline in headlines:
            my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
            print(f'{global_id_counter} news processed')
            if my_dict.get('title') != '':
                headline_list.append(my_dict)
                increase_counter()
            else:
                pass
        if headlines != []:
            page += 1
            scrape_merdeka(inp,page,headline_list)
        else:
            pass
    except:
        return headline_list
    return headline_list

def scrape_detik(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page{page}'
    response = requests.get(passurl,allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all("h2")

    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        if any(d_headline.get('title') == my_dict.get('title') for d_headline in headline_list):
            return headline_list
        else:
            headline_list.append(my_dict)
            increase_counter()
    page += 1
    scrape_detik(inp,page,headline_list)

    return headline_list

def scrape_tribun(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page={page}'
    response = requests.get(passurl)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all(attrs=inp[1][1])

    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        print(f'{global_id_counter} news processed')
        increase_counter()
        if my_dict != 0:
            headline_list.append(my_dict)
        else:
            pass
    if headlines != []:
        page += 1
        scrape_tribun(inp,page,headline_list)
    else:
        pass
    return headline_list


def scrape_viva(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page={page}'
    response = requests.get(passurl)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all(attrs=inp[1][1])

    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        print(f'{global_id_counter} news processed')
        increase_counter()
        if my_dict != 0:
            headline_list.append(my_dict)
        else:
            pass
    if headlines != []:
        page += 1
        scrape_viva(inp,page,headline_list)
    else:
        pass
    return headline_list

def scrape_liputan6(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page={page}'
    response = requests.get(passurl)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all(attrs=inp[1][1])

    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        print(f'{global_id_counter} news processed')
        increase_counter()
        if my_dict in headline_list:
            return headline_list
        else:
            headline_list.append(my_dict)
            page += 1
            scrape_liputan6(inp,page,headline_list)
    return headline_list

def scrape_tempo(inp,page,headline_list):
    passurl = str(inp[1][0]) + f'?page={page}'
    response = requests.get(passurl)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find(attrs={"class":'list list-type-1'}).find_all("h2")

    for headline in headlines:
        my_dict = {'id': global_id_counter,'title': headline.get_text().strip()}
        print(f'{global_id_counter} news processed')
        increase_counter()
        if my_dict in headline_list:
            return headline_list
        else:
            headline_list.append(my_dict)
            page += 1
            scrape_tempo(inp,page,headline_list)
    return headline_list

def start_scrape(urls):
    results = []
    if urls[0] == 'tribun':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_tribun(urls,1,headline_list))
        # pass
    elif urls[0] == 'liputan6':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_liputan6(urls,1,headline_list))
    elif urls[0] == 'kompas':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_kompas(urls,1,headline_list))
    elif urls[0] == 'detik':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_detik(urls,1,headline_list))
    elif urls[0]=='tempo':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_tempo(urls,1,headline_list))
    elif urls[0]=='merdeka':
        headline_list=[]
        print(f'working on {urls[0]}')
        results.extend(scrape_merdeka(urls,1,headline_list))
    else:
        pass
    return(results)

def main():
    final=[]
    id_counter=1
    for url in urls.items():
        final.extend(start_scrape(url))
    # print(final)
    return(final)

if __name__=='__main__':
    main()