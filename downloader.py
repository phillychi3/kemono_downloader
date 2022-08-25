import requests
from bs4 import BeautifulSoup
import zipfile
import fake_useragent
def downloader(url):
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    headers = {
        'user-agent': useragent
    }
    r = requests.get(url, headers=headers)
    print("rok")
    soup = BeautifulSoup(r.text, 'html.parser')
    lsitdata = soup.find_all('h2', class_='post-card__heading')
    print("rok")
    for i in lsitdata:
        print("rok")
        case=i.find("a").get("href")
        title=i.find("a").get_text()
        title = title.replace("\n", "").replace(r"\u300004a","").replace("\u3000", "").replace('"', "")
        casedata = requests.get("https://kemono.party"+case, headers=headers)
        soup2 = BeautifulSoup(casedata.text, 'html.parser')
        downloads = soup2.find_all('a', class_='post__attachment-link')
        images = soup2.find_all('div', class_='post__thumbnail')
        if downloader == [] and images == []: # 之後要加上內容 (markdown)
            print("No downloads found")
            continue
        with zipfile.ZipFile(f'{title}.zip', mode='w') as zf:
            for i in downloads:
                data = requests.get("https://kemono.party/"+i.get('href'), headers=headers)
                zf.writestr(i.get('href').split('/')[-1], data.content)
            ct=1
            for i in images:
                data = requests.get("https://kemono.party/"+i.find('img').get('src'), headers=headers)
                zf.writestr(str(ct)+i.find('img').get('src').split('/')[-1][-4:], data.content)
                ct+=1

if __name__ == '__main__':
    input_url = input("Enter the URL: ")
    downloader(input_url)