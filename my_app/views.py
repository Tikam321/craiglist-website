from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
# Create your views here.

BASE_CRAIGLIST_URL="https://mumbai.craigslist.org/search/sss?query={}"
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request,'my_app/base.html')


def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(quote_plus(search))
    final_url=BASE_CRAIGLIST_URL.format(quote_plus(search))    # print(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')
    post_titles=soup.find_all('a',{'class':'result-title'})
    # print(post_titles[0].get('href'))

    post_listings=soup.find_all('li',{'class':'result-row'})
    # post_title=post_listings.find(class_='result-title').text
    # post_url=post_listings.find('a').get('href')
    # post_price=post_listings.find(class_='result-price').text
    # print(post_listings)
    # print(post_title)
    # print(post_url)
    # print(post_price)
    # post_image=post_listings.find_all(class_='result-image').get('data-ids')[0]

    final_listings=[]

    for post in post_listings:
        post_title=post.find(class_='result-title').text
        post_url=post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price=post.find(class_='result-price').text
        else:
            post_price='N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(",")[0].split(":")[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ30EuaK8ifiQBrwCl1RIxmUIFv4jZ_txfW0bnT7BeViKbRoDNI&usqp=CAU'


        final_listings.append((post_title,post_url,post_price,post_image_url))
    context={
      'search':search,
      'final_listings':final_listings,
    }

    return render(request,'my_app/new_search.html',context)
