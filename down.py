# coding=utf-8
""" 
Created on 2015-12-05  Ontology Spider
@author Eastmount CSDN
URL:
  http://www.meddir.cn/cate/736.htm
  http://www.medlive.cn/pubmed/
  http://paper.medlive.cn/literature/1502224
"""

import time          
import re          
import os
import shutil
import sys
import codecs 
from selenium import webdriver      
from selenium.webdriver.common.keys import Keys      
import selenium.webdriver.support.ui as ui      
from selenium.webdriver.common.action_chains import ActionChains  

#Open PhantomJS
driver = webdriver.Firefox()
driver2 = webdriver.PhantomJS(executable_path="C:/Users/zhangp/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe") 
wait = ui.WebDriverWait(driver,10)

'''
出处：https://www.cnblogs.com/eastmount/p/5055911.html
 Load Ontoloty
 去到每个生物本体页面下载摘要信息
 http://paper.medlive.cn/literature/literature_view.php?pmid=26637181
 http://paper.medlive.cn/literature/1526876
'''
def getAbstract(num,title,url):
    try:
        fileName = ".\\PubMedSpider\\" + str(num) + ".txt"
        #result = open(fileName,"w")
        #Error: 'ascii' codec can't encode character u'\u223c'
        result = codecs.open(fileName,'w','utf-8') 
        result.write("[Title]\r\n")
        result.write(title+"\r\n\r\n")
        result.write("[Astract]\r\n")
        driver2.get(url)
        elem = driver2.find_element_by_xpath("//div[@class='txt']/p")
        #print elem.text
        result.write(elem.text+"\r\n")
    except Exception:    
        print('Error:')
    finally:
        result.close()
        print('END\n')

'''
 循环获取搜索页面的URL
 规律 http://www.medlive.cn/pubmed/pubmed_search.do?q=protein&page=1
'''
def getURL():
    page = 1      #跳转的页面总数
    count = 1     #统计所有搜索的生物本体个数    
    while page<=20:
        url_page = "http://www.medlive.cn/pubmed/pubmed_search.do?q=protein&page="+str(page)
        print(url_page)
        driver.get(url_page)
        elem_url = driver.find_elements_by_xpath("//div[@id='div_data']/div/div/h3/a")
        for url in elem_url:
            num = "%05d" % count
            title = url.text
            url_content = url.get_attribute("href")
            print(num)
            print(title)
            print(url_content)
            #自定义函数获取内容
            getAbstract(num,title,url_content)
            count = count + 1
        else:
            print("Over Page " + str(page) + "\n\n")
        page = page + 1
    else:
        "Over getUrl()\n"
        time.sleep(5)

'''
 主函数预先运行
'''
if __name__ == '__main__':
    path = ".\\PubMedSpider\\"
    if os.path.isfile(path):         #Delete file
        os.remove(path)
    elif os.path.isdir(path):        #Delete dir    
        shutil.rmtree(path, True)    
    os.makedirs(path)                #Create the file directory
    getURL()
    print("Download has finished.")
