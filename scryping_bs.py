import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import io

url = 'https://scraping-for-beginner.herokuapp.com/udemy'

res = requests.get(url)
#print(res)

soup = BeautifulSoup(res.text, 'html.parser')
#print(soup.find_all('p'))  全て<p>
#print(soup.find('p')[0] 最初の<p>

subscribers = soup.find_all('p', attrs={'class':'subscribers'})[0]

#print(subscribers)

n_subscribers = int(subscribers.text.split('：')[1])
# ":"が全角の場合もある
#soup.select('.subscribers')
#soup.select_one('.subscribers')
#soup.select('.subscribers').text

print(n_subscribers)

reviews = soup.find_all('p', attrs={'class':'reviews'})[0]
n_reviews = int(reviews.text.split('：')[1])

print(n_reviews)


#観光地名

url = 'https://scraping-for-beginner.herokuapp.com/ranking/'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

data = []
spots = soup.find_all('div', attrs={'class':'u_areaListRankingBox'})

for spot in spots:
    spot_name = spot.find('div', attrs={'class':'u_title'})
    #spot_name = spot.find_all('div', attrs={"class:u_title"})で一つしかないことを確認する

    spot_name.find('span', attrs={'class': 'badge'}).extract()
    #"badgeを除去"
    spot_name = spot_name.text.replace('\n', '')
    #"\n"を除去
    #print(spot_name)

    #総合評価
    eval_num = soup.find('div', attrs={'class': 'u_rankBox'}).text
    #一階層上のu_rankBoxに着目する。

    eval_num = float(eval_num.replace('\n',''))
    #"\n"を除去
    #print(eval_num)

    categoryItems = spot.find('div', attrs={'class': 'u_categoryTipsItem'})
    categoryItems = categoryItems.find_all('dl')

    details = {}
    for categoryItem in categoryItems:
        category = categoryItem.dt.text
        rank = float(categoryItem.span.text)
        details[category] = rank

    datum = details
    datum['観光地名'] = spot_name
    datum['評点'] = eval_num
    data.append(datum)

#print(data)

df = pd.DataFrame(data)
df = df[['観光地名', '評点', 'アクセス', '人混みの多さ', '景色', '楽しさ']]
df.to_csv('観光地情報.csv', index=False)


#画像の取得と保存

url = 'https://scraping-for-beginner.herokuapp.com/image'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

#img_tag=soup.find('img')

#root_url='https://scraping-for-beginner.herokuapp.com'
#img_url = root_url + img_tag['src']

#img = Image.open(io.BytesIO(requests.get(img_url).content))
#img.save('img/sample.jpg')

img_tags = soup.find_all('img')
for i, img_tag in enumerate(img_tags):
    root_url = 'https://scraping-for-beginner.herokuapp.com'
    img_url = root_url + img_tag['src']
    img = Image.open(io.BytesIO(requests.get(img_url).content))
    img.save(f'{i}.jpg')