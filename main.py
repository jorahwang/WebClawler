import os
import re
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
PHANTOMJS_PATH="C:/Tools/phantomjs-2.1.1-windows/bin/phantomjs.exe"

def save_img(img_url):
    file_path = os.getcwd() + '/images/'
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        print(img_url)
        file_name = file_path + img_url.split('/')[-1]
        request.urlretrieve(img_url, file_name)

    except IOError as e:
        print ('文件操作失败', e)
    except Exception as e:
        print('错误', e)

def FindHImage(bsObj):
    items = bsObj.findAll("li", {"id": re.compile("comment-[0-9]+")}, 1)
    print("start")
    count=0

    try:
        for item in items:
            # print(item)
            text = item.find("div", {"class": "text"})
            # vote = item.find("div", {"class": "jandan - vote"})

            oo = int(item.find("span", {"class": "tucao-like-container"}).span.get_text())
            if oo > 1000:
                image = item.find("img", {"src": re.compile("//[a-zA-Z0-9]+\.sinaimg\.cn/.+\.(jpg|png|gif)")})
                if image != None:
                    img_url="http:"+image["src"]
                    save_img(img_url)

                    xx = item.find("span", {"class": "tucao-unlike-container"}).span.get_text()
                    print(img_url + " oo=" + str(oo) + " xx=" + xx)
                    count = count+1

        return count
    except:
        print ("an error occured")
        return 0

def GetNextPage(bsObj):
    try:
        next= bsObj.find("a", {"class", "previous-comment-page"})
        if next == None:
            print("GetNextPage next=null")
            return ""
        else:
            return "http:"+next["href"]
    except:
        print("GetNextPage error")
        return ""

# TODO 记录每一张图的OOXX数到csv
def Run():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(options=chrome_options, executable_path=PHANTOMJS_PATH)
    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
    driver.set_page_load_timeout(30)
    #http://jandan.net/pic/page-1#comments

    url = "http://jandan.net/pic"

    maxPageNum=200
    pageCount = 0
    while pageCount < maxPageNum:
        print("loading page url="+url)
        try:
            driver.get(url)
        except TimeoutException:
            print('time out after 30 seconds when loading page' )
        finally:
            pass
            #driver.execute_script('window.stop()')

        bsObj = BeautifulSoup(driver.page_source, features="html.parser")
        print("finding HImages...")
        count = FindHImage(bsObj)
        print(str(count) + " HImages found")

        url = GetNextPage(bsObj)
        print("next="+url)
        if url == "":
            break

        pageCount = pageCount+1


    print("finish")
    driver.close()

def Run2():
    html = request.urlopen("http://jandan.net/pic")
    bsObj = BeautifulSoup(html)
    ooxx = bsObj.findAll("span", {"class": "tucao-like-container"})
    #print(ooxx)
    for elem in ooxx:
        print(elem.span.get_text())
        oo = elem.span.get_text()

    #imgaes = bsObj.findAll("img", {"src": re.compile("//[a-zA-Z0-9]+\.sinaimg\.cn/.+\.(jpg|png|gif)")})
    #for image in imgaes:
        # print(image)
        # print(image["src"])
        #save_img("https:" + image["src"])

if __name__ == "__main__":
    Run()