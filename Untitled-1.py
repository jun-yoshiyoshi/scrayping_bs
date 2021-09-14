url = 'https://scraping-for-beginner.herokuapp.com/image'
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

img_tag=soup.find('img')

#root_url='https://scraping-for-beginner.herokuapp.com'
#img_url = root_url + img_tag['src']

#img = Image.open(io.BytesIO(requests.get(img_url).content))
#img.save('img/sample.jpg')

img_tags = soup.find_all('img')

for i,img_tag in enumerate(img_tags):
    print(i,img_tags)
    root_url='https://scraping-for-beginner.herokuapp.com'
    img_url = root_url + img_tag['src']

    img = Image.open(io.BytesIO(requests.get(img_url).content))
    img.save(f'img/{i}.jpg')
