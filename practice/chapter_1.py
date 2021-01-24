#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = '../../data/drinks.csv'

drinks = pd.read_csv(file_path)
drinks['continent'] = drinks['continent'].fillna('OT')

################### question1 ###################
# 대륙별 평균 wine_servings를 탐색
wine_group = drinks.groupby('continent')['wine_servings'].mean()
print(wine_group)
# %%
################### question2 ###################
# 국가별 모든 servings의 합을 계산한 total_servings라는 피처 생성
drinks['total_servings'] = drinks['beer_servings'] + drinks['wine_servings'] + drinks['spirit_servings']
total_servings = drinks.groupby('country')['total_servings'].sum()

print(total_servings)
# %%
################### question3 ###################
# 전체 평균보다 적은 알콜을 마시는 대륙 중, spirit을 가장 많이 마시는 국가를 찾기
total_mean_alcohol = drinks['total_litres_of_pure_alcohol'].mean()

country_mean_alcohol = drinks.groupby('continent')['total_litres_of_pure_alcohol'].mean()
low_alcohol_continent = country_mean_alcohol[country_mean_alcohol < total_mean_alcohol].index.tolist()
print(low_alcohol_continent)

for x in low_alcohol_continent:
    best_spirit_country = best_spirit_country.append(drinks.loc[drinks['continent'] == x].groupby('country')['total_litres_of_pure_alcohol'].mean())

best_spirit_country = best_spirit_country.drop_duplicates()
print(best_spirit_country.sort_values(ascending = False))
# %%
################### question4 ###################
# 술소비량 대비 알콜 비율
rate = pd.DataFrame([total_servings, drinks['total_litres_of_pure_alcohol'].mean()]).T

#corr  = rate.corr(method = 'person')
print(rate)
# %%
