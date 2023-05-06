import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn import move_legend

fandango = pd.read_csv('fandango_scrape.csv')
print(fandango.head())

sns.scatterplot(data=fandango, y='VOTES', x='RATING')                                            #Связь между популярностью фильма и его рейтингом
#plt.show()

fandango.corr()

title = 'Название фильма (год)'
title.split('(')[-1].replace(')','')

fandango['YEAR']=fandango['FILM'].apply(lambda title: title.split('(')[-1].replace(')',''))      #Добавляем колонку: год выпуска фильма
fandango['YEAR'].value_counts()

sns.countplot(data=fandango, x='YEAR')                                                           #Визуализация количества фильмов в год


fandango.nlargest(10,'VOTES')                                                                    #10 фильмов с наибольшим количеством голосов
len(fandango[fandango['VOTES'] == 0])                                                            #Количество фильмов с нулем отзывов
fan_reviewd = fandango[fandango['VOTES'] > 0]                                                    #DaraFrame только с теми фильмами, у которых есть отзывы


plt.figure(figsize=(10,4), dpi=150)
sns.kdeplot(data=fan_reviewd, x='RATING', clip=[0,5], fill=True, label='True Rating')
sns.kdeplot(data=fan_reviewd, x='STARS', clip=[0,5], fill=True, label='Stars Displayed')
plt.legend(loc=(1.05, 0.5))
#plt.show()


fan_reviewd['STARS_DIFF'] = fan_reviewd['STARS'] - fan_reviewd['RATING']                         #Разница между колонками STARS и RATING
fan_reviewd['STARS_DIFF'] = fan_reviewd['STARS_DIFF'].round(1)
sns.countplot(data=fan_reviewd, x='STARS_DIFF', palette="rocket" )                               #Визуализация колонок STARS И RATING по разнице,
#plt.show()                                                                                      #которая говорит о том,
                                                                                                 #на сколько RATING совпдает со STARS по количеству фиьмов
var = fan_reviewd[fan_reviewd['STARS_DIFF'] == 1]

#Вывод: исхлдя из графика визуализации колонок STARS И RATING по разнице STARS_DIFF, можно сделать вывод, что
#сайт Fandango действительно завышает рейтинг фильмов. Следующии факты о завышении рейтинга со сравнением рейтингов других сайтов и Fandango:


all_sites = pd.read_csv('all_sites_scores.csv')                                                 #Чтение файла с рейтингами фильмов других сайтов


sns.scatterplot(data=all_sites, y='RottenTomatoes_User', x='RottenTomatoes')                    #Связь между рейтингами от критиков и пользовательскими
plt.ylim(0,100)                                                                                 #рейтингами от компании Rotten Tomatoes
plt.xlim(0,100)

all_sites['Rotten_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']       #Разница между рейтингом от критиков и пользовательским рейтингом
all_sites['Rotten_Diff'].apply(abs).mean()                                                      #Усреднение значений

plt.figure(figsize=(10,4), dpi=200)                                                             #Визуализация разницы
sns.histplot(data=all_sites, x='Rotten_Diff', kde=True, bins=25)


all_sites.nsmallest(5,'Rotten_Diff')[['FILM', 'Rotten_Diff']]                                   #Фильмы, которые были выше всего оценены пользователями
all_sites.nlargest(5,'Rotten_Diff')[['FILM', 'Rotten_Diff']]                                    #Фильмы, которые были выше всего оценены критикми


sns.scatterplot(data=all_sites, y='Metacritic_User', x='Metacritic')                            #Отображение пользовательских рейтингов и своих официальных
plt.xlim(0,10)                                                                                  #От MetaCritic
plt.ylim(0,100)


sns.scatterplot(data=all_sites, y='IMDB_user_vote_count', x='Metacritic_user_vote_count')       #Отображение пользовательских рейтингов и своих официальных
plt.xlim(0,10)                                                                                  #От IMDB
plt.ylim(0,100)


all_sites.nlargest(1,'IMDB_user_vote_count')                                                    #Фильм с самым юольшим количеством голосов на IMDB
all_sites.nlargest(1,'Metacritic_user_vote_count')                                              #Фильм с самым юольшим количеством голосов на MetaCritic




df = pd.merge(fandango, all_sites, on='FILM', how='inner')                                      #Объединение двух df по колонке FILM

df['RT_Norm'] = np.round(df['RottenTomatoes']/20,1)                                             #Нормализация данных
df['RTU_Norm'] = np.round(df['RottenTomatoes_User']/20,1)                                       #в диапозоне от 0 до 5
df['Meta_Norm'] = np.round(df['Metacritic']/20,1)                                               #в соответствии
df['Meta_U_Norm'] = np.round(df['Metacritic_User']/2,1)                                         #с колонками STARS и RATING
df['IMDB_Norm'] = np.round(df['IMDB']/2,1)                                                      #от Fandango

norm_scores = df[['STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]             #Создаём DataFrame с нормализованными значениями


fig, ax = plt.subplots(figsize=(15,6), dpi=200)                                                                   #Сравнение распределения рейтингов от разных компаний
sns.kdeplot(data=norm_scores,clip=[0,5],fill=True,palette='Set1')
move_legend(ax, "upper left")


fig, ax = plt.subplots(figsize=(15,6), dpi=200)                                                                   #Сравение распределения рейтингов
sns.kdeplot(data=norm_scores[['RT_Norm','STARS']],clip=[0,5],fill=True,palette='Set1')                            #Rotten Tomatoes и распределения рейтингов STARS от Fandango
move_legend(ax, "upper left")

sns.histplot(norm_scores, bins=50)                                                                                #Гистограмма, сравнивающая все нормализованные рейтинги


sns.clustermap(norm_scores, cmap = 'magma', col_claster=False)                                                    #График, показывающий как различные компании
                                                                                                                  #оценивают фильмы с наименьшими рейтингами

norm_films = df[['FILM','STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm' ]]      #Выявление 10-ти фильмом с наихудшими рейтингами
worst_films = norm_films.nsmallest(10, 'RT_Norm')                                                                 #И какие рейтинги дали этим фильмам другие компании
sns.kdeplot(data=worst_films, clip=[0,5], shade=True, palette='Set1')


