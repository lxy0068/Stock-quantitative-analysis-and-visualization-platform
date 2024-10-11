#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
基金的实时净值（估值）
"""
import time
import json
import requests


def fetch_fund_realtime_price(fund_code):
    url = "http://fundgz.1234567.com.cn/js/{}.js?rt={}"
    time_token = int(time.time() * 1000)
    url = url.format(fund_code, time_token)
    headers = {
        "Cookie": "st_si=88136748688505; em_hq_fls=js; _qddaz=QD.3axogy.w74yar.k7aj193n; pgv_pvi=9638725632; pgv_si=s6451931136; qgqp_b_id=d9105c4067adcc9a6acd3b15c74f1afe; EMFUND0=05-24%2022%3A29%3A56@%23%24%u56FD%u6CF0%u541B%u5B89%u541B%u5F97%u946B%u6DF7%u5408C@%23%24952099; EMFUND1=05-25%2000%3A01%3A57@%23%24%u5609%u5B9E%u65B0%u5174%u4EA7%u4E1A%u80A1%u7968@%23%24000751; EMFUND2=05-25%2000%3A14%3A34@%23%24%u5929%u5F18%u4E2D%u8BC1500%u6307%u6570C@%23%24005919; EMFUND3=05-25%2000%3A20%3A15@%23%24%u5929%u5F18%u6CAA%u6DF1300ETF%u8054%u63A5C@%23%24005918; EMFUND4=05-25%2022%3A50%3A53@%23%24%u94F6%u6CB3%u521B%u65B0%u6210%u957F%u6DF7%u5408@%23%24519674; EMFUND5=05-25%2022%3A51%3A06@%23%24%u6C47%u6DFB%u5BCC%u4E2D%u8BC1%u5168%u6307%u8BC1%u5238%u516C%u53F8%u6307%u6570C@%23%24501048; EMFUND6=05-28%2014%3A55%3A19@%23%24%u56FD%u6CF0CES%u534A%u5BFC%u4F53%u884C%u4E1AETF%u8054%u63A5C@%23%24008282; EMFUND7=05-28%2014%3A54%3A56@%23%24%u5E7F%u53D1%u53CC%u64CE%u5347%u7EA7%u6DF7%u5408@%23%24005911; EMFUND8=06-01%2013%3A51%3A33@%23%24%u534E%u5B9D%u4E2D%u8BC1%u533B%u7597ETF@%23%24512170; EMFUND9=06-02 15:00:58@#$%u5BCC%u56FD%u7814%u7A76%u91CF%u5316%u7CBE%u9009%u6DF7%u5408@%23%24005075; intellpositionL=1152px; cowminicookie=true; emshistory=%5B%22515860%22%2C%22sh515860%22%2C%22515860.SH%22%2C%22%E4%B8%AD%E4%BF%A1%E4%B8%80%E7%BA%A7%22%2C%22%E5%9C%BA%E5%86%85%E6%B5%81%E9%80%9A%E4%BB%BD%E9%A2%9D%22%2C%22%E5%85%89%E5%88%BB%E8%83%B6%22%2C%22%E5%AE%9E%E7%9B%98%E7%A7%80%22%5D; HAList=f-0-399976-CS%u65B0%u80FD%u8F66%2Ca-sh-600104-%u4E0A%u6C7D%u96C6%u56E2%2Ca-sz-002456-%u6B27%u83F2%u5149%2Ca-sz-002400-%u7701%u5E7F%u96C6%u56E2%2Ca-sh-603997-%u7EE7%u5CF0%u80A1%u4EFD%2Ca-sz-300090-%u76DB%u8FD0%u73AF%u4FDD%2Ca-sh-601628-%u4E2D%u56FD%u4EBA%u5BFF; st_asi=delete; intellpositionT=1741px; st_pvi=24720107306190; st_sp=2020-02-27%2015%3A11%3A30; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=1875; st_psi=20200607211234416-0-0748570310",
        "Host": "fundgz.1234567.com.cn",
        "Referer": "http://fund.eastmoney.com/{}.html?spm=001.1.swh".format(fund_code),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf8'
    data = json.loads(resp.text[8:-2])
    return {'基金代码': fund_code, 
            '基金': data['name'],
            '净值估算': data['gsz'], 
            '时间': data['gztime']}
