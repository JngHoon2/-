import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
import random
import pytagcloud
import webbrowser
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from IPython.display import Image

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

# 피처 마다 데이터 전처리 적용
df['title'] = df['title'].apply(lambda x : text_cleaning(x))
df['category'] = df['category'].apply(lambda x : text_cleaning(x))
df['content_text'] = df['content_text'].apply(lambda x : text_cleaning(x))

# 피처 마다 말뭉치 생성
title_corpus = ''.join(df['title'].tolist())
catetgory_corpus = ''.join(df['category'].tolist())
content_corpus = ''.join(df['content_text'].tolist())

#konlpy의 형태소 분석 모듈을 사용하여 키워드 추출
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(content_corpus)
count = Counter(nouns)

# 한글자 키워드 제거
remove_char_counter = Counter({x : count[x] for x in count if len(x) > 1})

# 불용어 리스트를 오픈합니다.
korean_stopword_path = '/Users/tuan/Documents/Python/python-data-analysis-master/data/korean_stopwords.txt'
with open(korean_stopword_path, encoding= 'utf8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]
print(stopwords[:10])

#적용이 필요한 불용어를 추가합니다.
namu_wiki_stopwords = ['상위', '문서', '내용', '누설', '아래', '해당', '표기', '설명', '추가', '모든', '사용', '매우', '가장', '줄거리', '요소', '상황', '편집', '틀', 
                        '경우', '때문', '모습', '정도', '이후', '사실', '생각', '인물', '이름', '년월']
for stopword in namu_wiki_stopwords:
    stopwords.append(stopword)

# 키워드 데이터에서 불용어를 제거 합니다
remove_char_counter = Counter({x : remove_char_counter[x] for x in count if x not in stopwords})

ranked_tags = remove_char_counter.most_common(40)

taglist = pytagcloud.make_tags(ranked_tags, maxsize = 80)

pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size = (900, 600), fontname = 'NanumGothic', rectangular = False)

Image(filename = 'wordcloud.jpg')