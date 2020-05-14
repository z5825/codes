from requests_html import HTMLSession
import time, random

def getLinks():
    ses = HTMLSession()
    links = []

    strFix = 'http://searchs.hunan.gov.cn/hunan/hnxjxq/news?q=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&searchfields=&sm=&columnCN=&p='
    for i in range(0, 70):
        time.sleep(random.random()*3)
        urls = strFix + str(i) + '&timetype='
        r = ses.get(urls)
        if r.status_code == 404 or r.status_code == 403:
            continue
        toGet = '#hits > li > div.com-title'
        results = r.html.find(toGet)
        for x in results:
            if '勘察' not in x.text and '监理' not in x.text and '咨询' not in x.text and '检测' not in x.text and '监控' not in x.text:
                if '设计' in x.text:
                   if '总承包' in x.text or '施工' in x.text:
                    links.append(x.absolute_links)
                else: links.append(x.absolute_links)
    with open('sites_D.txt', 'w') as f:
        for url in links:
            url = url.pop()+'\n'
            f.writelines(url)

getLinks()
