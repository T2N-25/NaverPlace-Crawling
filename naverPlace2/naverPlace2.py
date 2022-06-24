# ====
# import selenium
from selenium import webdriver
# from selenium.webdriver import ActionChains
 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
 
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

import json

from wordcloud import WordCloud

from time import sleep

driver = webdriver.Chrome('C:/Users/kimgu/Desktop/chrome_driver/chromedriver')
driver.get('https://map.naver.com/v5/search')


driver.implicitly_wait(time_to_wait=60)
print('Web Loading Complete')

search_box = driver.find_element(By.CSS_SELECTOR, '#container > shrinkable-layout > div > app-base > search-input-box > div > div.search_box > div > input')
search_key_word = input('어느 지역의 맛집을 찾으십니까?\n::] ')
search_box.send_keys(search_key_word)

# 검색버튼 누르기
# search_box.send_keys(Keys.ENTER)
search_box.send_keys(Keys.RETURN)

driver.implicitly_wait(time_to_wait=60)
print('Search Loading Complete')

# Iframe 안에 있으므로 frame 전환
driver.switch_to.frame('searchIframe')
itemlist = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]')

#스크롤 내리기 이동 전 위치
scroll_location = 1
scroll_height = -1

while scroll_location != scroll_height:
    
    scroll_location = driver.execute_script("return document.querySelector('#_pcmap_list_scroll_container').scrollHeight")
	
    #현재 스크롤의 가장 아래로 내림
    driver.execute_script("arguments[0].scrollTo(0, document.querySelector('#_pcmap_list_scroll_container').scrollHeight)", itemlist)

    #전체 스크롤이 늘어날 때까지 대기
    sleep(0.3)
    
    #늘어난 스크롤 높이
    scroll_height = driver.execute_script("return document.querySelector('#_pcmap_list_scroll_container').scrollHeight")

print('Find Loading Complete')

html = driver.page_source # 셀레니움으로 가져오기
driver.close()

soup = BeautifulSoup(html, 'html.parser') # BS4 로 HTML 로 파싱

re_dict = {}

for i in soup.select('#_pcmap_list_scroll_container > ul > li'):
    if '광고' in i.text:
        continue
    name = i.select_one('div > a > div > div > span').text
    re_dict[name] = {}
    for j in i.select('div > a > div > span'):
        word = j.text
        if '별점' in word:
            word = word.replace('별점', '')
            re_dict[name]['별점'] = float(word)
        elif '방문자' in word or '블로그' in word:
            word = word.split()
            word[-1] = word[-1].replace(',', '')
            re_dict[name][word[0]] = int(word[-1])

# Json 으로 저장
with open('./{}_.json'.format(search_key_word), 'w') as f:
    json.dump(re_dict, f, indent=4, ensure_ascii=False)

# wc가 사용할 수 있는 형태의 딕셔너리로 수정
wc_dict = {}
for key in re_dict.keys():
    wc_dict[key] = int(sum(re_dict[key].values()))

# 단어구름, 워드클라우드
wc = WordCloud(font_path='C:/Windows/Fonts/HYDNKM.TTF', width=400, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(wc_dict)
wc.to_file('{}_wc.png'.format(search_key_word))