# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:16:41 2023

@author: User
"""
import requests
import os
import random
import time
import re

#设置请求头和代理ip
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
#proxies = {'https':'https://14.29.124.168:24007'}

def getIPList():
    IPList = []
    url = 'http://www.66ip.cn/index.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    tablePattern = '<table[^>]*>[\s\S]*?<\/table>'
    rowPattern = '<tr>(.*?)<\/tr>'
    resultList = re.findall(rowPattern,re.findall(tablePattern,html)[-1])[1:]
    for i in resultList:
        IPList.append('https://'+i.split('</td><td>')[0].split('>')[-1]+':'+i.split('</td><td>')[1])
    return IPList


#定义请求目标url的方法
def get_html(url,proxy):
    try:
        response = requests.get(url, headers=headers,proxies=proxy)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
    except Exception:
        print('错误2')

#获取分页地址的url
def get_url(url):
    head = 'http://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/gxbyszpzl'
    return head+re.findall('/.*',url)[0][:-1]

#获取下载地址的url
def get_download_url(html,head):
    downloadPattren = '<a\s+href="\.\/[^"]+\.\w+"'
    downloadLink = re.findall(downloadPattren, html)
    return [head+re.findall('/.*',i)[0][:-1] for i in downloadLink]

#获取文件名
def get_filename(html):
    fileNamePattern = '<a\s+href="\.\/[^"]+\.\w+">[^<]+<\/a>'
    fileNameList = re.findall(fileNamePattern, html)
    return [i.split('>')[-2].split('<')[0] for i in fileNameList]

#下载文件
def download_file(url,company,fileName,proxy):
    pathHead = 'C:/Users/User/Desktop/SYDW'
    response = requests.get(url,headers=headers,proxies=proxy)
    path = pathHead+'/'+company
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path+'/'+fileName, 'wb') as code:
        code.write(response.content)



startTime = time.time()
count = 0
for p in range(20):
    if p == 0:
        indexPage = 'index'
    else:
        indexPage = 'index_'+str(p)
    IPList = getIPList()
    randomIP = IPList[random.randint(0, len(IPList)-1)]
    proxy = {'https':randomIP}
    url = 'http://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/gxbyszpzl/'+indexPage+'.html'
    html = get_html(url,proxy)
    targetUrlPattern = '<a\s+href="\.\/\d+\/t\d+_\d+\.html"'
    targetTitlePattrern = 'title="[^"]+"'
    htmlList = re.findall(targetUrlPattern,html)
    titleList = re.findall(targetTitlePattrern,html)
    for i in range(len(htmlList)):
        describeUrl = get_url(htmlList[i])
        downloadHead = '/'.join(describeUrl.split('/')[:-1])
        describeHtml = get_html(describeUrl,proxy)
        downloadList = get_download_url(describeHtml,downloadHead)
        fileNameList = get_filename(describeHtml)
        company = titleList[i].split('"')[-2]
        for j in range(len(downloadList)):
            download_file(downloadList[j],company,fileNameList[j],proxy)
            time.sleep(random.uniform(0,3))
        deltaTime = time.time()-startTime
        count += 1
        print('累计用时'+str(round(deltaTime,3))+'秒,进度完成'+str(round((count/200)*100,1))+'%')
    
    
