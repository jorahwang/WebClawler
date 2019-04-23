#from urllib.request import urlopen
#from urllib.request import urlretrieve
from urllib import request

from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os


def save_img(img_url):
    file_path = os.getcwd() + '/images/'
    #print(file_path)
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        file_name = file_path + img_url.split('/')[-1]
        print(img_url)
        request.urlretrieve(img_url, file_name)

    except IOError as e:
        print ('文件操作失败', e)
    except Exception as e:
        print('错误', e)

html = request.urlopen("http://jandan.net/pic")
bsObj = BeautifulSoup(html)
print(bsObj.img)
#imgaes = bsObj.findAll("img", {"src": re.compile("//[a-zA-Z0-9]+\.sinaimg\.cn/.+\.(jpg|png|gif)")})
imgaes = bsObj.findAll("img", {"src": re.compile("//[a-zA-Z0-9]+\.sinaimg\.cn/.+\.(jpg|png|gif)")})
for image in imgaes:
    #print(image)
    #print(image["src"])
    save_img("https:"+image["src"])

