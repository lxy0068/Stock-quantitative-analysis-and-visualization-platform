#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
天天基金搜索接口
"""
import time
import json
import requests

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
eastmoney_fund_cookie = 'intellpositionL=1152px; IsHaveToNewFavor=0; qgqp_b_id=dbe20efaab3321e948962637a37ac894; cowminicookie=true; emshistory=%5B%22000001%22%2C%22%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85%22%5D; em-quote-version=topspeed; st_si=10129111187284; intellpositionT=455px; st_asi=delete; em_hq_fls=js; emhq_picfq=2; EMFUND0=02-14%2012%3A54%3A48@%23%24%u6613%u65B9%u8FBE%u4E2D%u8BC1%u56FD%u4F01%u5E26%u8DEF%u53D1%u8D77%u5F0F%u8054%u63A5C@%23%24007789; EMFUND1=02-14%2012%3A55%3A09@%23%24%u9E4F%u534E%u4E2D%u8BC1500ETF%u8054%u63A5C@%23%24008001; EMFUND2=02-14%2012%3A55%3A36@%23%24%u5E73%u5B89500ETF%u8054%u63A5C@%23%24006215; EMFUND3=02-14%2013%3A48%3A04@%23%24%u534E%u5546%u53CC%u64CE%u9886%u822A%u6DF7%u5408@%23%24010550; EMFUND4=02-14%2013%3A51%3A20@%23%24%u534E%u6CF0%u67CF%u745E%u6210%u957F%u667A%u9009%u6DF7%u5408A@%23%24010345; EMFUND5=02-14%2013%3A53%3A04@%23%24%u6613%u65B9%u8FBE%u4E2D%u8BC1800ETF%u8054%u63A5C@%23%24007857; EMFUND6=02-14%2016%3A09%3A53@%23%24%u535A%u65F6%u5065%u5EB7%u6210%u957F%u53CC%u5468%u5B9A%u671F%u53EF%u8D4E%u56DE%u6DF7%u5408A@%23%24009468; EMFUND7=02-14%2016%3A09%3A53@%23%24%u535A%u65F6%u4EA7%u4E1A%u7CBE%u9009%u6DF7%u5408C@%23%24010456; HAList=a-sz-002352-%u987A%u4E30%u63A7%u80A1%2Ca-sh-601012-%u9686%u57FA%u80A1%u4EFD%2Cd-hk-00700%2Ca-sz-300122-%u667A%u98DE%u751F%u7269%2Cd-hk-06886%2Ca-sz-300815-%u7389%u79BE%u7530%2Ca-sz-002475-%u7ACB%u8BAF%u7CBE%u5BC6%2Ca-sh-603655-%u6717%u535A%u79D1%u6280%2Ca-sz-000001-%u5E73%u5B89%u94F6%u884C%2Ca-sh-600093-%u6613%u89C1%u80A1%u4EFD%2Ca-sz-002668-%u5965%u9A6C%u7535%u5668%2Ca-sz-002982-%u6E58%u4F73%u80A1%u4EFD; EMFUND9=02-14%2016%3A37%3A43@%23%24%u4E1C%u5434%u884C%u4E1A%u8F6E%u52A8%u6DF7%u5408C@%23%24011240; EMFUND8=02-14 17:32:32@#$%u6731%u96C0%u4EA7%u4E1A%u81FB%u9009%u6DF7%u5408C@%23%24007494; st_pvi=89273277965854; st_sp=2020-07-21%2011%3A22%3A06; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2FBK0473.html; st_sn=179; st_psi=20210214173232100-0-7604659170'


def search_fund_eastmoney(fund_input):
    """
    天天基金搜索接口
    """
    search_api = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?callback=jQuery18308460939170427073_1613295152155&m=1&key={}&_={}'
    url = search_api.format(fund_input, int(time.time() * 1000))

    headers = {
        'Accept': accept,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': eastmoney_fund_cookie,
        'Host': 'fundsuggest.eastmoney.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf8'

    similar_results = json.loads(resp.text.split('"Datas":')[1][:-2])
    if similar_results:
        return {'code': similar_results[0]['CODE'], 'name': similar_results[0]['NAME']}
    else:
        return None
