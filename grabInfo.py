from requests_html import HTMLSession
import pandas as pd

class Project(object):
    def __init__(self, sn = 1):
        self.sn = sn
        self.name = self.price = self.company = self.supervisor = self.biddingServer = self.owner = '/'

    def __str__(self):
        x = str(self.name) +'\n'+ str(self.price) +'\n'+ str(self.company) +'\n'+ str(self.supervisor) \
                +'\n'+ str(self.biddingServer) +'\n'+ str(self.owner)
        return x

def getLinks():
    ses = HTMLSession()
    links = []

    strFix = 'http://fwpt.csggzy.cn/jyxxfjjggg/index'
    strVar = ['.jhtml']
    for i in range(2, 16):
        strVar.append('_' + str(i) + '.jhtml')
    for sVar in strVar:
        urls = strFix + sVar
        r = ses.get(urls)
        toGet = 'body > div.bg-main > div.container-div.jyxx > div > div.right-nr > div.main-list > ul > li > p.list-leftp > a'
        results = r.html.find(toGet)
        for x in results:
           if '勘察' not in x.text and '监理' not in x.text and '咨询' not in x.text:
               if '设计' in x.text:
                   if '总承包' in x.text or '施工' in x.text:
                    links.append(x.absolute_links)
               else: links.append(x.absolute_links)

    strFix = 'https://changsha.hnsggzy.com/queryContent'
    postfix = '-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A&beginTime=&endTime='
    strVar = [strFix + postfix]
    strVar.append('https://changsha.hnsggzy.com/queryContent_2788-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A&beginTime=&endTime=')

    for i in range(2, 279):
        strVar.append('_' + str(i) + postfix)
    for sVar in strVar:
        urls = strFix + sVar
        r = ses.get(urls)
        toGet = 'body > div.content-warp > div.jyxxcontent > div > ul > li '
        results = r.html.find(toGet)
        for x in results:
            text = x.text.replace(' ', '')
            text = x.text.replace('\n', '')
            if '勘察' not in text and '监理' not in text and '咨询' not in text:
               if '设计' in text:
                   if '总承包' in text or '施工' in text:
                    links.append(x.absolute_links)
               else: links.append(x.absolute_links)

    # print(len(links))
    with open('sites.txt', 'a') as f:
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
            newPro.company = result[0].text.replace('\n','')
            ndx = newPro.company.find(toFind) + len(toFind)
            newPro.company = newPro.company[ndx:]

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

        ctt = [newPro.name, newPro.price, newPro.company, \
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
        newPro.name, newPro.price, newPro.company, newPro.owner, newPro.supervisor, newPro.biddingServer = \
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

    sn = 1
    for url in links:
        newPro = Project(sn)
        sn += 1
        r = ses.get(url)
        
        s1 = '#content-box-id > table'
        si = ''
        s2 = ' > tbody > tr.firstRow > td:nth-child(1) > p > span'
        for i in range(15):
            result = r.html.find(s1 + si + s2)
            if result[0].text == '中标候选人':
                break
            else:
                si = ':nth-child(' + str(i) + ')'

        toFind = '#publicity_content > table' + si + '> tbody > tr:nth-child(1) > td.xmmc'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.name = result[0].text.replace('\n','')

        toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child(3) > td:nth-child(2) > p > span'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.price = result[0].text.replace('\n','')
        
        toFind = '#content-box-id > table' + si + '> tbody > tr:nth-child(2) > td:nth-child(2) > p > span'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.company = result[0].text.replace('\n','')

        toFind = '#publicity_content > table' + si + '> tbody > tr:nth-child(2) > td:nth-child(4)'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.owner = result[0].text.replace('\n','')

        toFind = '#publicity_content > table' + si + '> tbody > tr:nth-child(3) > td:nth-child(4)'
        result = r.html.find(toFind)
        if len(result) != 0:
            newPro.supervisor = result[0].text.replace('\n','')

        # toFind = '招标代理'
        # result = r.html.find('p', containing = toFind)
        # if len(result) != 0:
        #     newPro.biddingServer = result[0].text.replace('\n','')
        #     ndx = newPro.biddingServer.find(toFind) + len(toFind)
        #     newPro.biddingServer = newPro.biddingServer[ndx:]

        ctt = [newPro.name, newPro.price, newPro.company, \
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
        newPro.name, newPro.price, newPro.company, newPro.owner, newPro.supervisor, newPro.biddingServer = \
            [ctt[i] for i in range(len(ctt))]
        projects.append(newPro)

    return projects

def export(projects):
    name, price, company, owner, supervisor, biddingServer = ([] for x in range(6))
    for proj in projects:
        name.append(proj.name)
        price.append(proj.price)
        company.append(proj.company)
        owner.append(proj.owner)
        supervisor.append(proj.supervisor)
        biddingServer.append(proj.biddingServer)
    data = {'项目名称':name, '中标金额（元）':price, '中标单位名称':company, 
            '招标人':owner,'监督部门':supervisor,'招标代理':biddingServer}
    df = pd.DataFrame(data)
    df.to_csv('projects.csv')

# getLinks()
# projects = getContent_A()
projects = getContent_B()
export(projects)

#content-box-id > table > tbody > tr:nth-child(2) > td:nth-child(2) > p > span
#content-box-id > table:nth-child(9) > tbody > tr:nth-child(2) > td:nth-child(2) > p
#content-box-id > table:nth-child(9) > tbody > tr:nth-child(3) > td:nth-child(2) > p > span



# https://requests-html.kennethreitz.org//index.html
# https://changsha.hnsggzy.com/queryContent_356-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&beginTime=&endTime=#
# 施工 总承包 项目 标段 工程  ） 

    # for p in projects:
    #     print(p)
    #     if input('type quit to quit:') == 'quit':
    #         break
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(22) > tbody > tr:nth-child(2) > td:nth-child(1) > p > span
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(22) > tbody > tr:nth-child(2) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > p > span
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(22) > tbody > tr.firstRow > td:nth-child(2) > p > span
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(8) > tbody > tr:nth-child(2) > td:nth-child(2) > p > span
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td:nth-child(2)
# body > div.content-warp > div.content > div.content-article > div.div-article2 > table > tbody > tr > td > table:nth-child(8)
#content-box-id > table:nth-child(10) > tbody > tr:nth-child(2) > td:nth-child(2) > p > span