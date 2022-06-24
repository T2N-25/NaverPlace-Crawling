import requests
from bs4 import BeautifulSoup
import urllib

# location_url = urllib.parse.quote(input('어느 지역의 맛집을 찾으십니까?\n::] ') + '맛집')
location_url = urllib.parse.quote('부산대' + '맛집')

url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}'.format(location_url)
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select_one('#place-main-section-root > section.sc_new._1hPYK > div > ul')
    
    li = ul.select('li')
    
    # 식당리스트
    re_list = []

    for i in li:

        re_list.append([])

        a = i.select_one('div._3hn9q > a')
        div = a.select('div')
        # 식당명
        # re_name = div[1].select_one('span').text
        # print(re_name)
        # print(len(div))
        # print(div[3])

        span = a.select('div > span')
        for j in span:
            re_list[-1].append(j.text)
else:
    print(response.status_code)

print(re_list)
