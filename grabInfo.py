from requests_html import HTMLSession
import pandas as pd

def getLinks():
    ses = HTMLSession()
    strFix = 'http://fwpt.csggzy.cn/jyxxfjjggg/index'
    strVar = ['.jhtml']
    for i in range(2, 2):
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
        
        result = r.html.find('p', containing = '项目名称')
        if len(result) != 0:
            newPro.name = result[0].text.replace('\n','')

        result = r.html.find('p', containing = '中标价格')
        if len(result) != 0:
            newPro.price = result[0].text.replace('\n','')
        else:
            result = r.html.find('p', containing = '中标金额')
            if len(result) != 0:
                newPro.price = result[0].text.replace('\n','')

        result = r.html.find('p', containing = '中标单位名称')
        if len(result) != 0:
            newPro.company = result[0].text.replace('\n','')

        result = r.html.find('p', containing = '招标人')
        if len(result) != 0:
            newPro.owner = result[0].text.replace('\n','')
        else:
            result = r.html.find('p', containing = '招 标 人')
            if len(result) != 0:
                newPro.owner = result[0].text.replace('\n','')

        result = r.html.find('p', containing = '监督部门')
        if len(result) != 0:
            newPro.supervisor = result[0].text.replace('\n','')
        else:
            result = r.html.find('p', containing = '招标投标管理')
            if len(result) != 0:
                newPro.supervisor = result[0].text.replace('\n','')

        result = r.html.find('p', containing = '招标代理')
        if len(result) != 0:
            newPro.biddingServer = result[0].text.replace('\n','')

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
    rcd = records[0]
    # df = pd.DataFrame.from_dict(rcd)
    df = pd.DataFrame(data = rcd)
    # df = pd.DataFrame(data = rcd, columns = \
    #                 ['项目名称','中标金额','中标单位名称','招标人','监督部门','招标代理'], index = [1])
    # for rcd in records:
    #     df.append(pd.DataFrame(rcd), ignore_index = True)

    print(df)

dictionary, projects = getContent()
export(dictionary)

# https://requests-html.kennethreitz.org//index.html