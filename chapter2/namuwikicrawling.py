import requests
from bs4 import BeautifulSoup
import re

#크롤링할 사이트 주소를 정의합니다.
source_url = 'https://namu.wiki/RecentChanges'

#사이트의 HTML 구조에 기반하여 크롤링을 수행합니다.
req = requests.get(source_url)
html = req.content
soup = BeautifulSoup(html, 'lxml')
contents_table = soup.find(name = 'table')
table_body = contents_table.find(name = 'tbody')
table_rows = table_body.find_all(name = 'tr')
# a 태그의 href 속성을 리스트로 추출하여 크롤링할 페이지 리스트를 생성합니다.
page_url_base = 'https://namu.wiki'
page_urls = []
for index in range(0, len(table_rows)):
    first_td = table_rows[index].find_all(name ='td')[0]
    td_url = first_td.find_all('a')
    if len(td_url) > 0:
        page_url = page_url_base + td_url[0].get('href')
        page_urls.append(page_url)

# 중복 url을 제거합니다.
page_urls = list(set(page_urls))
for page in page_urls[:5]:
    print(page)

req = requests.get(page_urls[0])
html = req.content
soup = BeautifulSoup(html, 'lxml')
contents_table = soup.find(name = 'article')
title = contents_table.find_all('h1')[0]
category = contents_table.find_all('ul')[0]
contents_paragraphs = contents_table.find_all(name = 'div')
contents_corpus_list = []

for paragraphs in contents_paragraphs:
    contents_corpus_list.append(paragraphs.text)

contents_corpus = ''.join(contents_corpus_list)

print(title.text)
print('-----------------------')
print(category.text)
print('-----------------------')
print(contents_corpus)
