from requests_html import HTMLSession
import pandas as pd

def getLinks():
    ses = HTMLSession()
    strFix = 'http://fwpt.csggzy.cn/jyxxfjjggg/index'
    strVar = ['.jhtml']
    for i in range(2, 16):
        strVar.append('_' + str(i) + '.jhtml')
    lks = []
    content = []
    for sVar in strVar:
        urls = strFix + sVar
        r = ses.get(urls)
        toGet = 'body > div.bg-main > div.container-div.jyxx > div > div.right-nr > div.main-list > ul > li > p.list-leftp > a'
        results = r.html.find(toGet)
        for x in results:
            if '总承包' in x.text or '施工' in x.text or 'EPC' in x.text:
                lks.append(x.absolute_links)
                content.append(x.text)
    return lks, content

class Project(object):
    def __init__(self, sn = 1):
        self.sn = sn
        self.name = self.price = self.company = self.supervisor = self.biddingServer = self.owner = '/'

    def __str__(self):
        x = str(self.name) +'\n'+ str(self.price) +'\n'+ str(self.company) +'\n'+ str(self.supervisor) \
                +'\n'+ str(self.biddingServer) +'\n'+ str(self.owner)
        return x

def getContent():
    lks, content = getLinks()
    projects = []
    dictionary = []
    ses = HTMLSession()
    # lks = [{'http://fwpt.csggzy.cn/jyxxfjjggg/25780.jhtml'}]

    sn = 1
    for lk in lks:
        newPro = Project(sn)
        sn += 1
        url = lk.pop()
        r = ses.get(url)
        
        toFind = '项目名称'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.name = result[0].text.replace('\n','')
            ndx = newPro.name.find(toFind) + len(toFind)
            newPro.name = newPro.name[ndx:]

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
        # else:
        #     toFind = '招标投标管理'
        #     result = r.html.find('p', containing = '招标投标管理')
        #     if len(result) != 0:
        #         newPro.supervisor = result[0].text.replace('\n','')

        toFind = '招标代理'
        result = r.html.find('p', containing = toFind)
        if len(result) != 0:
            newPro.biddingServer = result[0].text.replace('\n','')
            ndx = newPro.biddingServer.find(toFind) + len(toFind)
            newPro.biddingServer = newPro.biddingServer[ndx:]

        entry = {'项目名称':newPro.name,'中标金额':newPro.price,'中标单位名称':newPro.company, \
                    '招标人':newPro.owner,'监督部门':newPro.supervisor,'招标代理':newPro.biddingServer}
        dictionary.append(entry)
        projects.append(newPro)
       
    # for p in projects:
    #     print(p)
    #     if input('type quit to quit:') == 'quit':
    #         break
    
    return dictionary, projects

def export(records):
    name, price, company, owner, supervisor, biddingServer = ([] for x in range(6))
    for rcd in records:
        name.append(rcd.name)
        price.append(rcd.price)
        company.append(rcd.company)
        owner.append(rcd.owner)
        supervisor.append(rcd.supervisor)
        biddingServer.append(rcd.biddingServer)
        # df.append(pd.DataFrame(rcd), ignore_index = True)
    data = {'项目名称':name, '中标金额':price, '中标单位名称':company, 
            '招标人':owner,'监督部门':supervisor,'招标代理':biddingServer}
    df = pd.DataFrame(data)
    df.to_excel('projects.xlsx', sheet_name='1', index=False)
    # print(df)

dictionary, projects = getContent()
export(projects)

# https://requests-html.kennethreitz.org//index.html
# https://changsha.hnsggzy.com/queryContent_356-jygk.jspx?title=&origin=&inDates=&channelId=161&ext=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&beginTime=&endTime=#