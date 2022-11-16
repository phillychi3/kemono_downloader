import requests
from bs4 import BeautifulSoup
import zipfile
import fake_useragent
from progress.bar import IncrementalBar
import os
from argparse import ArgumentParser
def download_all(url,folder,iszip):
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    headers = {
        'user-agent': useragent
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    lsitdata = soup.find_all('article', class_='post-card post-card--preview')
    name=soup.find("a", class_="user-header__profile").find('span',{'itemprop':'name'}).get_text()
    name = name.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "").replace(' ', "")
    if folder == False:
        if not os.path.exists(f'downloads/{name}'):
            os.mkdir(f'downloads/{name}')
        path = f'downloads/{name}'
    else:
        path = folder
    for i in lsitdata:
        case=i.find("a").get("href")
        title=i.find("header").get_text()
        title = title.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "")
        if os.path.exists(f'{path}/{title}.zip') or os.path.exists(f'{path}/{title}'):
            print(f'{title} exists')
            continue
        casedata = requests.get("https://kemono.party"+case, headers=headers)
        soup2 = BeautifulSoup(casedata.text, 'html.parser')
        downloads = soup2.find_all('a', class_='post__attachment-link')
        images = soup2.find_all('div', class_='post__thumbnail')
        if downloads == [] and images == []: # 之後要加上內容 (markdown)
            print("No downloads found")
            continue
        with IncrementalBar('Downloading', max=len(downloads)+len(images)) as bar:
            with zipfile.ZipFile(f'{path}/{title}.zip', mode='w') as zf:
                for i in downloads:
                    data = requests.get("https://kemono.party/"+i.get('href'), headers=headers)
                    zf.writestr(i.get('href').split('/')[-1], data.content)
                    bar.next()
                ct=1
                for i in images:
                    data = requests.get("https://kemono.party/"+i.find('img').get('src'), headers=headers)
                    zf.writestr(str(ct)+i.find('img').get('src').split('/')[-1][-4:], data.content)
                    ct+=1
                    bar.next()
    print("Done")

def download_one(url,folder,iszip):
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    headers = {
        'user-agent': useragent
    }
    casedata = requests.get(url, headers=headers)
    soup2 = BeautifulSoup(casedata.text, 'html.parser')
    downloads = soup2.find_all('a', class_='post__attachment-link')
    images = soup2.find_all('div', class_='post__thumbnail')
    title=soup2.find('h1',class_="post__title").find('span').get_text()
    title = title.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "")
    name=soup2.find('a',class_="post__user-name").get_text()
    name = name.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "").replace(' ', "")
    if folder == False:
        if not os.path.exists(f'downloads/{name}'):
            os.mkdir(f'downloads/{name}')
        path = f'downloads/{name}'
    else:
        path = folder
    if os.path.exists(f'{path}/{title}.zip') or os.path.exists(f'{path}/{title}'):
        print(f'{title} exists')
        return
    if downloads == [] and images == []: # 之後要加上內容 (markdown)
        print("No downloads found")
        return
    with IncrementalBar('Downloading', max=len(downloads)+len(images)) as bar:
        with zipfile.ZipFile(f'{path}/{title}.zip', mode='w') as zf:
            for i in downloads:
                data = requests.get("https://kemono.party/"+i.get('href'), headers=headers)
                zf.writestr(i.get('href').split('/')[-1], data.content)
                bar.next()
            ct=1
            for i in images:
                data = requests.get("https://kemono.party/"+i.find('img').get('src'), headers=headers)
                zf.writestr(str(ct)+i.find('img').get('src').split('/')[-1][-4:], data.content)
                ct+=1
                bar.next()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('url', help='url')
    parser.add_argument('-z', '--zip', help='use zip', action='store_true')
    parser.add_argument('-f', '--folder', help='save folder', default='downloads')
    args = parser.parse_args()
    if 'post' in args.url:
        download_one(args.url, args.folder, args.zip)
    else:
        download_all(args.url, args.folder, args.zip)



    # input_url = input("Enter the URL: ")
    # if "kemono.party" not in input_url:
    #     print("Invalid URL")
    #     exit()
    # if os.path.isdir("downloads") == False:
    #     os.mkdir("downloads")
    # download_all(input_url)
    #download_one(input_url)

    