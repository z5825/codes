from requests_html import HTMLSession
from requests_html import HTML
import pandas as pd
import time, random

class Project(object):
    def __init__(self, sn = 1):
        self.sn = sn
        self.name = self.supervisor = self.biddingServer = self.owner = self.time = self.evalMethod = '/'
        self.candidates, self.prices = ['/'] * 3, ['/'] * 3

    def __str__(self):
        x = str(self.name) +'\n'+ str(self.price) +'\n'+ str(self.candidate) +'\n'+ str(self.supervisor) \
                +'\n'+ str(self.biddingServer) +'\n'+ str(self.owner)+'\n' + str(self.time)
        return x

def getLinks():
    ses = HTMLSession()
    links = []

    # strFix = 'http://fwpt.csggzy.cn/jyxxfjjggg/index'
    # strVar = ['.jhtml']
    # for i in range(2, 16):
    #     strVar.append('_' + str(i) + '.jhtml')
    # for sVar in strVar:
    #     time.sleep(random.random()*3)
    #     urls = strFix + sVar
    #     r = ses.get(urls)
    #     toGet = 'body > div.bg-main > div.container-div.jyxx > div > div.right-nr > div.main-list > ul > li > p.list-leftp > a'
    #     results = r.html.find(toGet)
    #     for x in results:
    #         if '勘察' not in x.text and '监理' not in x.text and '咨询' not in x.text and '检测' not in x.text and '监控' not in x.text:
    #             if '设计' in x.text:
    #                if '总承包' in x.text or '施工' in x.text:
    #                 links.append(x.absolute_links)
    #             else: links.append(x.absolute_links)
    # with open('sites_A.txt', 'a') as f:
    #     for url in links:
    #         url = url.pop()+'\n'
    #         f.writelines(url)

    # with open('fromColTableInfo.xml', encoding='utf-8') as f:
    #     refs = f.read()
    # links = []
    # html = HTML(html = refs)
    # results = html.find('a')
    # for x in results:
    #     if '勘察' not in x.text and '咨询' not in x.text and '检测' not in x.text and '监控' not in x.text:
    #         if '设计' in x.text:
    #            if '总承包' in x.text or '施工' in x.text:
    #             links.append(x.absolute_links)
    #         else: links.append(x.absolute_links)

    # with open('sites_B.txt', 'w') as f:
    #     forDup = set()
    #     for url in links:
    #         url = url.pop()+'\n'
    #         url = url.replace('https://example.org/', 'http://175.6.46.113/')
    #         url = url.replace('¬', '&not')
    #         if url not in forDup:
    #             forDup.add(url)
    #             f.writelines(url)

    # strFix = 'https://changsha.hnsggzy.com/queryContent'
    # postfix = '-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&beginTime=&endTime='
    # strVar = [strFix + postfix]
    # strVar.append('https://changsha.hnsggzy.com/queryContent_3563-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&beginTime=&endTime=')

    # for i in range(2, 357):
    #     strVar.append('_' + str(i) + postfix)
    # for sVar in strVar:
    #     time.sleep(random.random()*3)
    #     urls = strFix + sVar
    #     r = ses.get(urls)
    #     toGet = 'body > div.content-warp > div.jyxxcontent > div > ul > li '
    #     results = r.html.find(toGet)
    #     for x in results:
    #         text = x.text.replace(' ', '')
    #         text = x.text.replace('\n', '')
    #         if '勘察' not in x.text and '监理' not in x.text and '咨询' not in x.text and '检测' not in x.text and '监控' not in x.text:
    #             if '设计' in text:
    #                if '总承包' in text or '施工' in text:
    #                 links.append(x.absolute_links)
    #             else: links.append(x.absolute_links)

    # with open('sites_C.txt', 'a') as f:
    #     for url in links:
    #         url = url.pop()+'\n'
    #         f.writelines(url)

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

def getContent_A():
    with open('sites.txt', 'r') as f:
        links = f.readlines()
        for i in range(len(links)):
            links[i] = links[i].rstrip('\n')
    projects = []
    ses = HTMLSession()

    sn = 1
    for url in links:
        time.sleep(random.random()*3)
        newPro = Project(sn)
        sn += 1
        r = ses.get(url)
        
        toFind = '项目名称'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.name = result[0].text.replace('\n','')
            ndx = newPro.name.find(toFind) + len(toFind)

        toFind = '中标价格'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.price = result[0].text.replace('\n','')
            ndx = newPro.price.find(toFind) + len(toFind)
            newPro.price = newPro.price[ndx:]
        else:
            toFind = '中标金额'
            result = r.html.find('p', containing = toFind)
            if len(result) != 0:
                newPro.price = result[0].text.replace('\n','')
                ndx = newPro.price.find(toFind) + len(toFind)
                newPro.price = newPro.price[ndx:]
        
        toFind = '中标单位名称'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.candidate = result[0].text.replace('\n','')
            ndx = newPro.candidate.find(toFind) + len(toFind)
            newPro.candidate = newPro.candidate[ndx:]

        toFind = '招标人'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.owner = result[0].text.replace('\n','')
            ndx = newPro.owner.find(toFind) + len(toFind)
            newPro.owner = newPro.owner[ndx:]
        else:
            toFind = '招 标 人'
            result = r.html.find('p', containing = toFind)
            if len(result) != 0:
                newPro.owner = result[0].text.replace('\n','')
                ndx = newPro.owner.find(toFind) + len(toFind)
                newPro.owner = newPro.owner[ndx:]

        toFind = '监督部门'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.supervisor = result[0].text.replace('\n','')
            ndx = newPro.supervisor.find(toFind) + len(toFind)
            newPro.supervisor = newPro.supervisor[ndx:]

        toFind = '招标代理'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.biddingServer = result[0].text.replace('\n','')
            ndx = newPro.biddingServer.find(toFind) + len(toFind)
            newPro.biddingServer = newPro.biddingServer[ndx:]

        ctt = [newPro.name, newPro.price, newPro.candidate, \
                newPro.owner, newPro.supervisor, newPro.biddingServer]
        for i in range(len(ctt)):
            ndx = ctt[i].find('：')
            if ndx != -1:
                ctt[i] = ctt[i][ndx + 1:]
            else:
                ndx = ctt[i].find(':')
                if ndx != -1:
                    ctt[i] = ctt[i][ndx + 1:]
                
        for i in (1,):
            if ctt[i].endswith('万元'):
                ctt[i] = ctt[i].rsplit('万元')[0]
            elif ctt[i].endswith('（元）'):
                ctt[i] = ctt[i].rsplit('（元）')[0]
            elif ctt[i].endswith('(元)'):
                ctt[i] = ctt[i].rsplit('(元)')[0]
            elif ctt[i].endswith(' (元)'):
                ctt[i] = ctt[i].rsplit(' (元)')[0]
            elif ctt[i].endswith('元。'):
                ctt[i] = ctt[i].rsplit('元。')[0]
            elif ctt[i].endswith('元'):
                ctt[i] = ctt[i].rsplit('元')[0]
                if ctt[i].isdigit():
                    ctt[i] = int(ctt[i])/10000 
                elif ctt[i].count('.') == 1 and ctt[i][0].isdigit():
                    ctt[i] = float(ctt[i])/10000 
                # else:
                #     ctt[i] += '元'
        for i in (2, 5):
            if not ctt[i].endswith('公司'):
                ndx = ctt[i].rfind('公司') + len('公司')
                ctt[i] = ctt[i][:ndx]
        newPro.name, newPro.price, newPro.candidate, newPro.owner, newPro.supervisor, newPro.biddingServer = \
            [ctt[i] for i in range(len(ctt))]
        projects.append(newPro)

    return projects

def getContent_B():
    with open('sites_B.txt', 'r') as f:
        links = f.readlines()
        for i in range(len(links)):
            links[i] = links[i].rstrip('\n')
    
    projects = []
    ses = HTMLSession()

    sn = 0
    # links = links[203:215]
    for url in links:
        time.sleep(random.random()*3)
        newPro = Project(sn)
        r = ses.get(url)
        if r.status_code == 404 or r.status_code == 403:
            continue

        # toFind = '#content-box-id > p'
        # results = r.html.find(toFind)
        # if len(results) > 0:
        #     for i in range(len(results)):
        #         txt = results[i].text
        #         if len(txt) > 10:
        #             n1, n2 = txt.find('采用'), txt.find('评标委员会') 
        #             newPro.evalMethod = txt[n1:n2]
        #             break
        toFind = '#publicity_contents > div.title > h2'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.name = result.text
        if '中标候选人公示' in newPro.name:
            newPro.name = newPro.name.replace('中标候选人公示', '')
        toFind = '#publicity_content > table > tbody > tr:nth-child(2) > td:nth-child(4)'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.owner = result.text
        toFind = '#publicity_content > table > tbody > tr:nth-child(3) > td:nth-child(4)'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.supervisor = result.text
        toFind = '#publicity_content > table > tbody > tr:nth-child(5) > td'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.time = result.text.replace('发布日期：','')[:-6]

        s1 = '#content-box-id > table'
        s2 = ' > tbody > tr.firstRow > td'
        stCol = 0
        located = False
        for i in range(50):
            si = ':nth-child('+str(i)+')'
            results = r.html.find(s1 + si + s2)
            if len(results) > 0 :
                for stCol in range(len(results)):
                    if '中标候选人' in results[stCol].text:
                        located = True
                        break
                if located:
                    break
        stRow = 2
        toFind = '#content-box-id > table' + si + '> tbody > tr.firstRow > td:nth-child('+str(stCol+2)+')'
        result = r.html.find(toFind, first = True)
        if result is not None and '公司' in result.text:   # or '第一' not in result.text:
            stRow = 1
        
        toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child('+str(stRow)+') > td:nth-child('+str(stCol+2)+')'
        result = r.html.find(toFind, first = True)
        if result is not None: 
            newPro.candidates[0] = result.text
        for i in [1, 2]:
            toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child('+str(stRow)+') > td:nth-child('+str(stCol+2+i)+')'
            result = r.html.find(toFind, first = True)
            if result is not None:
                newPro.candidates[i] = result.text

        stCol += 2
        while True:
            toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child('+str(stRow+1)+') > td:nth-child('+str(stCol)+')'
            result = r.html.find(toFind, first = True)
            if result is not None:
                if result.text.isascii() or '元' in result.text:
                    newPro.prices[0] = result.text
                    break
                else:
                    stCol += 1
                    if stCol > 10: break
            else:
                stCol += 1
                if stCol > 10: break
        for i in [1, 2]:
            toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child('+str(stRow+1)+') > td:nth-child('+str(stCol+i)+')'
            result = r.html.find(toFind, first = True)
            if result is not None: 
                newPro.prices[i] = result.text

        toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child(3) > td:nth-child('+str(stCol-1)+')'
        results = r.html.find(toFind)
        if len(results) != 0:
            factor = 1
            for re in results:
                if '万' in re.text:
                    factor = 10000
            for n, price in enumerate(newPro.prices):
                for badwd in ['万','元','(',')','（','）',' ']:
                    price = price.replace(badwd, '')
                price = price.replace('．', '.')
                if price.isdigit() and int(price) > 100:
                    price = int(price) * factor / 10000
                elif price.count('.') == 1:
                    isFloat = True
                    for parts in price.split('.'):
                        if not parts.isdigit():
                            isFloat = False
                    if isFloat and float(price) > 100:
                            price = float(price) * factor / 10000
                newPro.prices[n] = price
        projects.append(newPro)
        sn += 1
        if len(links) < 300:
            pause = len(links)
        else: pause = 300
        if sn % (pause/10) == 0 or sn == len(links):
            print('processed to: %d ' %sn)
        if sn % pause == 0 or sn == len(links):
            print('export: %s-%s' %(sn-pause, sn-1))
            export(projects[sn-pause : sn], '%s-%s' %(sn-pause, sn-1))
            # time.sleep(random.random()*20)
            # s =  input('continue?') 
            # if s == 'n' or s == 'no':
            #     break

    return projects

def getContent_C():
    with open('sites_C.txt', 'r') as f:
        links = f.readlines()
        for i in range(len(links)):
            links[i] = links[i].rstrip('\n')
    
    projects = []
    ses = HTMLSession()
    # links.insert(0, 'https://changsha.hnsggzy.com/jygksz/1048644.jhtml')
    sn = 1
    for url in links:
        time.sleep(random.random()*3)
        newPro = Project(sn)
        sn += 1
        if sn % 100 == 0:
            print('the record: %d ' %sn)
        r = ses.get(url)
        if r.status_code == 404:
            continue

        toFind = 'body > div.content-warp > div.content > div.content-title2 > span:nth-child(1)'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.time = result[0].text

        toFind = 'body > div.content-warp > div.content > div.content-title'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.name = result[0].text.replace('中标候选人公示','')

        toFind = '招标人：'
        result = r.html.find('p', containing = toFind)
        if len(result) == 0:
            toFind = '标 人：' 
            result = r.html.find('p', containing = toFind)
       
            if len(result) == 0:
                toFind = '标\xa0人：' 
                result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.owner = result[0].text.replace('\n','')
            ndx = newPro.owner.find(toFind) + len(toFind)
            newPro.owner = newPro.owner[ndx:]

        toFind = '监督部门：' 
        result = r.html.find('p', containing = toFind)
        if len(result) == 0:
            toFind = '监管部门：' 
            result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.supervisor = result[0].text.replace('\n','')
            ndx = newPro.supervisor.find(toFind) + len(toFind)
            newPro.supervisor = newPro.supervisor[ndx:]

        toFind = 'body > div.content-warp > div.content > div.content-article > div.div-article2 > table '
        result = r.html.find(toFind)
        if len(result) != 0:
            txt = result[0].text
            n1 = txt.find('\n', txt.find('中标候选人名称')) + len('\n')
            n2 = txt.find('\n', n1)
            newPro.candidate = txt[n1:n2]

            se1 = '报价（'
            p1 = txt.find(se1)
            if p1 == -1:
                se1 = '报价'
                p1 = txt.find(se1)
            if p1 != -1:
                n1 = txt.find('\n', p1) + len('\n')
                n2 = txt.find('\n', n1)
                if '万' in txt[p1: p1 + len('s1') + 5]:
                    w = 10000
                else: w = 1
                newPro.price = txt[n1:n2].strip()
                if newPro.price.endswith('元'):
                    newPro.price = newPro.price.rsplit('元')[0]
                ndot = newPro.price.find('.')
                if newPro.price[:ndot].isdigit() and newPro.price[ndot + 1:].isdigit():
                    newPro.price = str(float(newPro.price) * w)
        
        # ctt = [newPro.name, newPro.price, newPro.candidate, \
        #         newPro.owner, newPro.supervisor, newPro.biddingServer, newPro.time]
        # for i in range(len(ctt)):
        #     ndx = ctt[i].find('：')
        #     if ndx != -1:
        #         ctt[i] = ctt[i][ndx + 1:]
        #     else:
        #         ndx = ctt[i].find(':')
        #         if ndx != -1:
        #             ctt[i] = ctt[i][ndx + 1:]
                
        # for i in (1,):
        #     if ctt[i].endswith('万元'):
        #         ctt[i] = ctt[i].rsplit('万元')[0]
        #     elif ctt[i].endswith('（元）'):
        #         ctt[i] = ctt[i].rsplit('（元）')[0]
        #     elif ctt[i].endswith('(元)'):
        #         ctt[i] = ctt[i].rsplit('(元)')[0]
        #     elif ctt[i].endswith(' (元)'):
        #         ctt[i] = ctt[i].rsplit(' (元)')[0]
        #     elif ctt[i].endswith('元。'):
        #         ctt[i] = ctt[i].rsplit('元。')[0]
        #     elif ctt[i].endswith('元'):
        #         ctt[i] = ctt[i].rsplit('元')[0]
        #         if ctt[i].isdigit():
        #             ctt[i] = int(ctt[i])/10000 
        #         elif ctt[i].count('.') == 1 and ctt[i][0].isdigit():
        #             ctt[i] = float(ctt[i])/10000 
        #         # else:
        #         #     ctt[i] += '元'
        # for i in (2, 5):
        #     if not ctt[i].endswith('公司'):
        #         ndx = ctt[i].rfind('公司') + len('公司')
        #         ctt[i] = ctt[i][:ndx]
        # newPro.name, newPro.price, newPro.candidate, newPro.owner, newPro.supervisor, newPro.biddingServer, newPro.time = \
        #     [ctt[i] for i in range(len(ctt))]
        projects.append(newPro)
        # if sn % 100 == 0 or sn == len(links):
        if sn % 100 == 0 or sn == 140:
            export(projects[sn-100 : sn], '%s-%s' %(sn-100, sn-1))
            if sn == 140:
                break

    return projects


def getContent_D():
    with open('sites_D.txt', 'r') as f:
        links = f.readlines()
        for i in range(len(links)):
            links[i] = links[i].rstrip('\n')
    
    projects = []
    ses = HTMLSession()

    sn = 0
    # links = links[203:215]
    for url in links:
        time.sleep(random.random()*3)
        newPro = Project(sn)
        r = ses.get(url)
        if r.status_code == 404 or r.status_code == 403:
            continue

        toFind = 'body > div.main > div.sub-detail > div > h2'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.name = result.text
        if '中标候选人公示' in newPro.name:
            newPro.name = newPro.name.replace('中标候选人公示', '')
        toFind = 'body > div.main > div.sub-detail > div > h6 > label:nth-child(3)'
        result = r.html.find(toFind, first = True)
        if result is not None:
            newPro.time = result.text.replace('时间：','')
        toFind = '#div_content > p > font'
        result = r.html.find(toFind, containing = '工程名称', first = True)
        if result is not None:
            newPro.name = result.text.replace('工程名称', '')
        result = r.html.find(toFind, containing = '建设单位', first = True)
        if result is not None:
            newPro.owner = result.text.replace('建设单位', '')
        else:
            result = r.html.find(toFind, containing = '招   标   人', first = True)
            if result is not None:
                newPro.owner = result.text.replace('招   标   人', '')
            else:
                result = r.html.find(toFind, containing = '招 标 人', first = True)
                if result is not None:
                    newPro.owner = result.text.replace('招 标 人', '')

        result = r.html.find(toFind, containing = '第一', first = True)
        if result is not None:
            newPro.candidates[0] = result.text
        result = r.html.find(toFind, containing = '第二', first = True)
        if result is not None:
            newPro.candidates[1] = result.text
        result = r.html.find(toFind, containing = '第三', first = True)
        if result is not None:
            newPro.candidates[2] = result.text
        
        elements = [newPro.name, newPro.time, newPro.owner, \
                    newPro.candidates[0],newPro.candidates[1],newPro.candidates[2]]
        for i, ele in enumerate(elements):
            n1 = ele.find('：')
            if n1 == -1: n1 = ele.find(':')
            if n1 != -1:
                ele = ele[n1 + 1:]
            elements[i] = ele       

        newPro.name, newPro.time, newPro.owner, newPro.candidates[0],newPro.candidates[1],newPro.candidates[2] = \
            elements
        projects.append(newPro)

        sn += 1
        if len(links) < 10:
            pause = len(links)
        else: pause = 10
        if sn % (pause/10) == 0 or sn == len(links):
            print('processed to: %d ' %sn)
        if sn % pause == 0 or sn == len(links):
            print('export: %s-%s' %(sn-pause, sn-1))
            export(projects[sn-pause : sn], '%s-%s' %(sn-pause, sn-1))
            s =  input('continue?') 
            if s == 'n' or s == 'no':
                break

def export(projects, fname):
    evalMethod, name, price1, price2, price3, candidate1, candidate2, candidate3, owner, supervisor, biddingServer, time \
        = ([] for x in range(12))
    for proj in projects:
        time.append(proj.time)
        name.append(proj.name)
        owner.append(proj.owner)
        supervisor.append(proj.supervisor)
        candidate1.append(proj.candidates[0])
        candidate2.append(proj.candidates[1])
        candidate3.append(proj.candidates[2])
        price1.append(proj.prices[0])
        price2.append(proj.prices[1])
        price3.append(proj.prices[2])
        biddingServer.append(proj.biddingServer)
        evalMethod.append(proj.evalMethod)
    data = {'时间':time, '项目名称':name, '招标人':owner, '第一':candidate1, '第二':candidate2, '第三':candidate3, \
            '投标报价1\n（万元）':price1, '报价2':price2, '报价3':price3, '监督部门':supervisor,'评标办法':evalMethod}
    df = pd.DataFrame(data)
    df.to_csv(fname + '.csv')
    # df.to_excel(fname + '.xls')

# getLinks()
# projects = getContent_A()
# projects = getContent_B()
# projects = getContent_C()
# projects = getContent_D()
# export(projects)


# https://changsha.hnsggzy.com/queryContent_356-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&beginTime=&endTime=#
# http://www.ruanyifeng.com/blog/2020/05/weekly-issue-106.html