import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
from konlpy.tag import Okt
from collections import Counter

#크롤링할 사이트 주소 정의
source_url = 'https://namu.wiki/RecentChanges'

#html 구조에 기반한 크롤링 수행
req = requests.get(source_url)
html = req.content
soup = BeautifulSoup(html, 'lxml')
contents_table = soup.find(name = 'table')
table_body = contents_table.find(name = 'tbody')
table_rows = table_body.find_all(name = 'tr')

#a태그의 herf속성 추출후 리스트업
page_url_base = 'https://namu.wiki'
page_urls = []
for index in range(0, len(table_rows)):
    frist_td = table_rows[index].find_all(name = 'td')[0]
    td_url = frist_td.find_all(name = 'a')
    if len(td_url) > 0:
        page_url = page_url_base + td_url[0].get('href')
        if 'png' not in page_url:
            page_urls.append(page_url)

# 중복값 제거
page_urls = list(set(page_urls))

#크롤링한 데이터, 데이터프레임으로 만들기 위한 정의
columns = ['title', 'category', 'content_text']
df = pd.DataFrame(columns = columns)

#각 페이지 별 인포메이션을 데이터 프레임으로
for page_url in page_urls:
    req = requests.get(page_url)
    html = req.content
    soup = BeautifulSoup(html, 'lxml')
    contents_table = soup.find(name = 'article')
    title = contents_table.find('h1')
    category = contents_table.find('ul')
    content_paragraphs = contents_table.find_all(name = 'div', attrs = {'class' : 'wiki-paragraph'})
    content_corpus_list = []

    # 페이지 내 제목에서 개행 문자 제거 후 추출
    # 없는 경우 빈 문자열로 대체
    if title is not None:
        row_title = title.text.replace("\n", ' ')
    else:
        row_title = ''

    # 페이지 내 카테고리에서 개행 문자 제거 후 추출
    # 없는 경우 빈 문자열로 대체

    if category is not None:
        row_category = category.text.replace("\n", ' ')
    else:
        row_category = ''

    # 페이지 내 본문에서 개행 문자 제거 후 추출
    # 없는 경우 빈 문자열로 대체
    if content_paragraphs is not None:
        for paragraphs in content_paragraphs:
            if paragraphs is not None:
                content_corpus_list.append(paragraphs.text.replace('\n', ' '))
            else:
                content_corpus_list.append('')

    # 데이터 프레임에 저장
    row = [row_title, row_category, ''.join(content_corpus_list)]
    series = pd.Series(row, index = df.columns)
    df = df.append(series, ignore_index = True)

# 텍스트 정제 (한글을 제외한 모든 문자 제거)
def text_cleaning(text):
    hangul = re.compile('^ ㄱ-|가-힣]+') # 한글 정규표현식
    result = hangul.sub('', text)
    return result

df['title'] = df['title'].apply(lambda x : text_cleaning(x))
df['category'] = df['category'].apply(lambda x : text_cleaning(x))
df['content_text'] = df['content_text'].apply(lambda x : text_cleaning(x))

title_corpus = ''.join(df['title'].tolist())
catetgory_corpus = ''.join(df['category'].tolist())
content_corpus = ''.join(df['content_text'].tolist())

nouns_tagger = Okt()
nouns = nouns_tagger.nouns(content_corpus)
count = Counter(nouns)

print(count)

