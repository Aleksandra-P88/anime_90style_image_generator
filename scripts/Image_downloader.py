# -*- coding: utf-8 -*-
"""
Created on Fri May 10 22:44:40 2024

@author: aleks
"""

import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import os
from PIL import Image
from io import BytesIO


class DownloadImage:
    def __init__(self, tag, panel_of_image, individual_image):
        self.tag = tag
        self.list_of_urls = []
        self.panel_of_image = panel_of_image
        self.individual_image = individual_image


    def fill_list_of_urls(self, number_of_page): 
        #Gelbooru
        #return [f'https://gelbooru.com/index.php?page=post&s=list&tags={self.tag}%pid={index}' for index in range(0,number_of_page,42)]
        #Safebooru
        return [f'https://safebooru.org/index.php?page=post&s=list&tags={self.tag}&pid={index}' for index in range(0,number_of_page,42)]
        #Danbooru
        #return [f'https://danbooru.donmai.us/posts?page={index}&tags={self.tag}' for index in range(number_of_page)][1:] 
         
    
    def download_and_save_images(self, amount_of_pages, save_path):
        i = 0
        list_of_urls = self.fill_list_of_urls(amount_of_pages)
        
        for item in list_of_urls:
            #req = urllib.request.Request(item, headers={'User-Agent': 'Mozilla/5.0'})
            #page = urllib.request.urlopen(req).read()
            #page = urllib.request.urlopen(req)
            page = urllib.request.urlopen(item)
            page_soup = BeautifulSoup(page, 'html.parser')
            
            img_items = page_soup.find('div', {"class": f"{self.panel_of_image}"})
            img_div = img_items.find_all(class_=f"{self.individual_image}")
            
            
            for img in img_div:
                post_link_tag = img.find('a')
                if not post_link_tag:
                    continue
                post_href = post_link_tag.get('href')
                full_post_url = f"https://safebooru.org/{post_href}"
                #full_post_url = f"https://gelbooru.org/{post_href}"
                #full_post_url = f"https://danbooru.org/{post_href}"
    
                # Wejdź w stronę pojedynczego posta
               # req_post = urllib.request.Request(full_post_url, headers={'User-Agent': 'Edge/12'})
                post_page = urllib.request.urlopen(full_post_url)
                #post_page = urllib.request.urlopen(req_post)
                post_soup = BeautifulSoup(post_page, 'html.parser')
                full_img_tag = post_soup.find('img', id='image')  # <- tutaj jest pełny obraz
                if not full_img_tag:
                    continue
    
                full_img_url = full_img_tag.get('src')
                file_name = str(i)
                complete_path = os.path.join(save_path, file_name + ".jpeg")
    
                
                #req_post = urllib.request.Request(full_post_url, headers={'User-Agent': 'Edge/12'})  
                #image_data = urllib.request.urlopen(req_post).read()
                image_data = urllib.request.urlopen(full_img_url).read()
                image = Image.open(BytesIO(image_data))
                if image.mode != "RGB":
                    image = image.convert("RGB")  # <-- to tutaj

                image.save(complete_path, "JPEG")
                i += 1
        
        '''
        new_size=(800,800)
        i=0
        list_of_urls = self.fill_list_of_urls(amount_of_pages)
        for item in list_of_urls:
            #req = urllib.request.Request(item, headers={'User-Agent': 'Edge/12.0'})
            page = urllib.request.urlopen(item)
            #page = urllib.request.urlopen(req).read()
            page_soup = BeautifulSoup(page, 'html.parser')
            img_items = page_soup.find('div', {"class":f"{self.panel_of_image}"})
            img_div = img_items.find_all(class_=f"{self.individual_image}")
            for img in img_div:
                img_tag=img.find('img')
                img_src = img_tag.get("src")
                image = img_src
                file_name = str(i)
                complete_path = os.path.join(save_path, file_name + ".jpeg")
                
                image_data = urllib.request.urlopen(img_src).read()
       
                   # Otwórz obraz za pomocą PIL
                image = Image.open(BytesIO(image_data))
                   
                   # Zmień rozmiar obrazu
                resized_image = image.resize(new_size)
                   
                   # Zapisz obraz o zmienionym rozmiarze
                #resized_image.save(complete_path, "JPEG")
                image.save(complete_path, "JPEG")  
                i += 1

           '''
      
      
#Danboruu
#downloadimage = DownloadImage('retro_artstyle+solo', 'posts-container gap-2', 'post-preview-container')
#downloadimage.download_and_save_images(389, 'E:\Programy\Image_Classification/Datasets/danbooru_90s')

#Safebooru
downloadimage = DownloadImage('takeuchi_naoko+sailor_moon', 'content', 'thumb')
downloadimage.download_and_save_images(42, "E:\Programy\Image_Classification\Datasets\T_Usagi")

##Gelbooru 

#downloadimage = DownloadImage('1990s_%28style%29+solo', 'thumbnail-container', 'thumbnail-preview')
#downloadimage.download_and_save_images(23058, "E:\Programy\Datasets\Image_Classification\gelbooru_90s")




'''

url = "https://danbooru.donmai.us/posts?tags=kaname_madoka&z=1"
page = urllib.request.urlopen(url)
page_soup = BeautifulSoup(page, 'html.parser')

#print(page_soup)

img_items = page_soup.find('div', {"class":"posts-container gap-2"})

img_div = img_items.find_all(class_="post-preview-container")

i=1
for img in img_div:
    img_tag=img.find('img')
    img_src = img_tag.get("src")
    print(img_src)
    image = img_src
    print(image)
    file_name = str(i)
    i+=1
    img_file=open(file_name +'.jpeg','wb')
    img_file.write(urllib.request.urlopen(image).read())
    img_file.close()
'''
'''
headers = {'Users-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"}

r = requests.get(url=url, headers=headers)


soup = BeautifulSoup(r.content, 'html.parser')
'''