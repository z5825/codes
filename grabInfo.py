from requests_html import HTMLSession

def getLinks():
    ses = HTMLSession()
    strFix = 'http://fwpt.csggzy.cn/jyxxfjjggg/index'
    strVar = ['.jhtml']
    for i in range(2, 3):
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
    def __init__(self):
        self.name, self.money, self.company, self.supervisor, self.biddingServer, self.owner = [None] * 6

    def __str__(self):
        x = str(self.name) +','+ str(self.money) +','+ str(self.company) +','+ str(self.supervisor) \
                +','+ str(self.biddingServer) +','+ str(self.owner)
        return x

def getContent():
    lks, content = getLinks()
    projects = []
    ses = HTMLSession()

    for lk in lks:
        newPro = Project()
        url = lk.pop()
        r = ses.get(url)
        toGet = '#printArea > div > p > span > font'
        # for x in r.html.find(toGet):
        #     if '项目名称' in x.text:
        #         newPro.name = x.text
        #     if '中标价格' in x.text or '中标金额' in x.text:
        #         newPro.money = x.text
        #     if '中标单位名称' in x.text:
        #         newPro.company = x.text
        #     if '招 标 人' in x.text or '招标人' in x.text:
        #         newPro.owner = x.text
        #     if '监督部门' in x.text or '招标投标管理' in x.text:
        #         newPro.supervisor = x.text
        #     if '招标代理' in x.text:
        #         newPro.biddingServer = x.text
        #     projects.append(newPro)
        for x in r.html.find(toGet, containing = '项目名称'):
            newPro.name = x.text
            # if '中标价格' in x.text or '中标金额' in x.text:
            #     newPro.money = x.text
            # if '中标单位名称' in x.text:
            #     newPro.company = x.text
            # if '招 标 人' in x.text or '招标人' in x.text:
            #     newPro.owner = x.text
            # if '监督部门' in x.text or '招标投标管理' in x.text:
            #     newPro.supervisor = x.text
            # if '招标代理' in x.text:
            #     newPro.biddingServer = x.text
            projects.append(newPro)

    for p in projects:
        print(p)
        if input('type quit to quit:') == 'quit':
            break
    



    # print(lks[0])
    # print(content)

getContent()

#printArea > div > p:nth-child(8) > span:nth-child(1) > font
#printArea > div > p:nth-child(10) > span:nth-child(1) > font
# toGet = '#printArea > div > p'
#printArea > div > p:nth-child(11) > span:nth-child(1) > font
#printArea > div > p:nth-child(3) > span
# <font face="宋体">长沙市开福区招标投标管理办公室</font>

# https://requests-html.kennethreitz.org//index.html