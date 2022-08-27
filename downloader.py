import requests
from bs4 import BeautifulSoup
import zipfile
import fake_useragent
from progress.bar import IncrementalBar


def download_all(url):
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    headers = {
        'user-agent': useragent
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    lsitdata = soup.find_all('h2', class_='post-card__heading')
    for i in lsitdata:
        case=i.find("a").get("href")
        title=i.find("a").get_text()
        title = title.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "")
        casedata = requests.get("https://kemono.party"+case, headers=headers)
        soup2 = BeautifulSoup(casedata.text, 'html.parser')
        downloads = soup2.find_all('a', class_='post__attachment-link')
        images = soup2.find_all('div', class_='post__thumbnail')
        if downloads == [] and images == []: # 之後要加上內容 (markdown)
            print("No downloads found")
            continue
        with IncrementalBar('Downloading', max=len(downloads)+len(images)) as bar:
            with zipfile.ZipFile(f'{title}.zip', mode='w') as zf:
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

def download_one(url):
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    headers = {
        'user-agent': useragent
    }
    casedata = requests.get(url, headers=headers)
    soup2 = BeautifulSoup(casedata.text, 'html.parser')
    downloads = soup2.find_all('a', class_='post__attachment-link')
    images = soup2.find_all('div', class_='post__thumbnail')
    title=soup2.find("a").get_text()
    if downloads == [] and images == []: # 之後要加上內容 (markdown)
        print("No downloads found")
        return
    with IncrementalBar('Downloading', max=len(downloads)+len(images)) as bar:
        with zipfile.ZipFile(f'{title}.zip', mode='w') as zf:
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
    input_url = input("Enter the URL: ")
    if "kemono.party" not in input_url:
        print("Invalid URL")
        exit()
    download_all(input_url)

    