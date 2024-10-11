#!/usr/bin/python
# _*_ coding: utf-8 _*_
import json
import time

import requests
import pandas as pd
from datetime import datetime, timedelta


def get_security_type(security_code: str):
    """
    根据股票代码判断所属证券市场
    XSHG 代表 Shan(g)hai，XSHE 代表 Sh(e)nzhen

    ['50', '51', '60', '90', '110'] 为 XSHG
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 XSHE
    ['5', '6', '9'] 开头的为 XSHG， 其余为 XSHE
    """
    just_code = security_code.replace('.', '').replace("SH", '').replace("SZ", '')
    if len(just_code) != 6:
        raise ValueError('security code must be 6 figures')

    if security_code.endswith(("SH", "SZ")):
        return security_code[-4:]
    if security_code.startswith(
            ("50", "51", "60", "90", "110", "113", "132", "204")
    ):
        return "SH"
    if security_code.startswith(
            ("00", "13", "18", "15", "16", "18", "20", "30", "39", "115", "1318")
    ):
        return "SZ"
    if security_code.startswith(("5", "6", "9", "7")):
        return "SH"
    return "SZ"


class EastmoneySpider(object):

    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            "Cookie": "intellpositionL=1152px; IsHaveToNewFavor=0; qgqp_b_id=dbe20efaab3321e948962637a37ac894; em-quote-version=topspeed; em_hq_fls=js; emhq_picfq=2; _qddaz=QD.fqkydg.323wae.klgkordo; st_si=68830202953408; emshistory=%5B%22%E5%8C%97%E5%90%91%E8%B5%84%E9%87%91%22%2C%22%E9%BB%84%E5%8D%8E%E6%9F%92%22%2C%22603501%22%2C%22603501.SH%22%2C%22%E7%AB%8B%E8%AE%AF%E7%B2%BE%E5%AF%86%22%2C%22%E9%87%91%E9%BE%99%E9%B1%BC%22%2C%22000001%22%2C%22%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85%22%5D; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; testtc=0.5378301696721359; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=06-23 23:41:40@#$%u5357%u534E%u4E30%u6DF3%u6DF7%u5408A@%23%24005296; sid=112627825; vtpst=|; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300999-%u91D1%u9F99%u9C7C%2Ca-sh-600199-%u91D1%u79CD%u5B50%u9152%2Ca-sh-601279-%u82F1%u5229%u6C7D%u8F66%2Ca-sz-002261-%u62D3%u7EF4%u4FE1%u606F%2Ca-sz-002570-%u8D1D%u56E0%u7F8E%2Ca-sz-000150-%u5B9C%u534E%u5065%u5EB7%2Ca-sz-300785-%u503C%u5F97%u4E70%2Ca-sz-003039-%u987A%u63A7%u53D1%u5C55%2Ca-sz-000158-%u5E38%u5C71%u5317%u660E%2Ca-sz-002044-%u7F8E%u5E74%u5065%u5EB7%2Ca-sz-002475-%u7ACB%u8BAF%u7CBE%u5BC6; cowCookie=true; cowminicookie=true; st_asi=delete; st_pvi=89273277965854; st_sp=2020-07-21%2011%3A22%3A06; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2FBK0473.html; st_sn=186; st_psi=20210707231408251-111000300841-0970974274; intellpositionT=2215px",
            "Host": None,
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        }

    def get_stock_kline_factor_datas(self, security_code, period, market_type):
        """
        获取个股的 K 线和基本指标数据

        Args:
            security_code: 股票代码
            period: 周期: day、week、month
        """
        if not market_type:
            security_type = get_security_type(security_code)
            market_type = int(security_type == 'SH')
        print('market_type:', market_type)

        # 根据当前时间，计算 beg 值
        cur_date = datetime.now()
        if period == 'day':
            begin_date = cur_date + timedelta(days=-1200)
            begin_date = begin_date.strftime('%Y%m%d')
            url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg={begin_date}&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid={market_type}.{security_code}&klt=101&fqt=1'
        elif period == 'week':
            begin_date = cur_date + timedelta(days=-120)
            begin_date = begin_date.strftime('%Y%m%d')
            url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg={begin_date}&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid={market_type}.{security_code}&klt=102&fqt=1'
        elif period == 'month':
            begin_date = cur_date + timedelta(days=-250)
            begin_date = begin_date.strftime('%Y%m%d')
            url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg={begin_date}&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid={market_type}.{security_code}&klt=103&fqt=1'
        else:
            raise ValueError(f'暂不支持 {period} 类型周期')

        resp = requests.get(url)
        resp.encoding = 'utf8'
        resp_data = resp.json()['data']
        security_name = resp_data['name']
        klines = resp.json()['data']['klines']

        all_stock_info = []
        for kline in klines:
            # 日期, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅, 涨跌幅, 涨跌额, 换手率
            datas = kline.split(',')
            stock_info = {
                'date': datas[0],
                'code': security_code,
                'name': security_name,
                'open': float(datas[1]),
                'close': float(datas[2]),
                'high': float(datas[3]),
                'low': float(datas[4]),
                'volume': float(datas[6])
            }
            all_stock_info.append(stock_info)

        stock_df = pd.DataFrame(all_stock_info)
        return stock_df

    def fetch_stock_capital_flow_rank(self, days=0):
        """
        获取东方财富个股资金流的最新排名

        fid 次数代表统计的时间范围，f62：今日排名，f267：3日排名，f164：5日排名，f174：10日排名
        http://data.eastmoney.com/zjlx/detail.html

        Args:
            days: 间隔的时间，0：f62，今日排名；3，f267,3日排名；5，f164，5日排名；10，f174，10日排名
        """
        page = 1
        page_size = 10000

        if days == 0:
            fid = 'f62'
        elif days == 3:
            fid = 'f267'
        elif days == 5:
            fid = 'f164'
        elif days == 10:
            fid = 'f174'
        else:
            raise ValueError('not supported days, Only 0, 3, 5, 10 can be selected')

        url = f'https://push2.eastmoney.com/api/qt/clist/get?fid={fid}&po=1&pz={page_size}&pn={page}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'

        self.headers['Host'] = "push2.eastmoney.com"
        self.headers['Referer'] = "http://data.eastmoney.com/"

        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf8'
        stock_datas = json.loads(resp.text)['data']['diff']

        # 当前统计的日期
        cur_date = stock_datas[0]['f124']
        cur_date = datetime.fromtimestamp(cur_date)
        # 转成 dataframe
        stock_df = pd.DataFrame(stock_datas)

        rename_columns = {
            "f12": "股票代码",
            "f14": "股票名称",
            "f62": f"{days}日主力净流入_净额",
            "f184": f"{days}日主力净流入_净占比",
        }
        stock_df.rename(columns=rename_columns, inplace=True)

        for col in rename_columns.values():
            stock_df = stock_df[stock_df[col] != '-']
            if col not in {'股票代码', '股票名称'}:
                stock_df[col] = stock_df[col].astype(float)

        drop_coumns = [f for f in stock_df.columns.tolist() if f not in set(rename_columns.values())]
        stock_df.drop(drop_coumns, axis=1, inplace=True)
        stock_df[f'{days}日排名'] = range(1, stock_df.shape[0] + 1)
        return cur_date, stock_df

    def fetch_stock_main_fund_proportion_rank(self):
        """
        个股主力资金占比排名
        http://data.eastmoney.com/zjlx/list.html
        """
        page = 1
        page_size = 10000
        url = f'http://push2.eastmoney.com/api/qt/clist/get?fid=f184&po=1&pz={page_size}&pn={page}&np=1&fltt=2&invt=2&fields=f2%2Cf3%2Cf12%2Cf13%2Cf14%2Cf62%2Cf184%2Cf225%2Cf165%2Cf263%2Cf109%2Cf175%2Cf264%2Cf160%2Cf100%2Cf124%2Cf265%2Cf1&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2'

        self.headers['Host'] = "push2.eastmoney.com"
        self.headers['Referer'] = "http://data.eastmoney.com/"

        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf8'
        stock_datas = json.loads(resp.text)['data']['diff']
        # 当前统计的日期
        cur_date = stock_datas[0]['f124']
        cur_date = datetime.fromtimestamp(cur_date)

        stock_df = pd.DataFrame(stock_datas)
        rename_columns = {
            "f12": "股票代码",
            "f14": "股票名称",
            "f184": "今日主力净占比",
            "f3": "今日涨跌",
            "f165": "5日主力净占比",
            "f109": "5日涨跌",
            "f175": "10日主力净占比",
            "f160": "10日涨跌",
            "f100": "所属版块",

        }
        stock_df.rename(columns=rename_columns, inplace=True)

        for col in rename_columns.values():
            stock_df = stock_df[stock_df[col] != '-']
            if col not in {'股票代码', '股票名称', '所属版块'}:
                stock_df[col] = stock_df[col].astype(float)

        drop_coumns = [f for f in stock_df.columns.tolist() if f not in set(rename_columns.values())]
        stock_df.drop(drop_coumns, axis=1, inplace=True)
        return cur_date, stock_df

    def fetch_stock_north_bound_foreign_capital_rank(self):
        """
        个股北向资金持仓排名，注意是上一个交易日的数据
        http://data.eastmoney.com/hsgtcg/list.html
        """
        page = 1
        page_size = 10000
        HdDate = datetime.now().date()

        while True:
            url = f'https://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?st=ShareSZ_Chg_One&sr=-1&ps={page_size}&p={page}&type=HSGT20_GGTJ_SUM&token=894050c76af8597a853f5b408b759f5d&js=%7B%22data%22%3A(x)%2C%22pages%22%3A(tp)%2C%22font%22%3A(font)%7D&filter=(DateType%3D%271%27)(HdDate%3D%27{str(HdDate)}%27)'

            self.headers['Host'] = "dcfm.eastmoney.com"
            self.headers['Referer'] = "http://data.eastmoney.com/"

            resp = requests.get(url, headers=self.headers)
            resp.encoding = 'utf8'
            stock_datas = json.loads(resp.text)['data']

            if len(stock_datas) > 0:
                break
            HdDate = HdDate + timedelta(days=-1)

        stock_df = pd.DataFrame(stock_datas)
        rename_columns = {
            "SCode": "股票代码",
            "SName": "股票名称",
            "HYName": "所属行业",
            "HYCode": "行业代码",
            "DQName": "所属地区",
            "DQCode": "地区代码",
            "ShareHold": "今日持股股数",
            "ShareSZ": "今日持股市值",
            "LTZB": "今日持股占流通股比",
            "ZZB": "今日持股占总股本比",
            "ShareHold_Chg_One": "今日增持股数",
            "ShareSZ_Chg_One": "今日增持市值",
            "LTZB_One": "今日增持占流通股比‰",
            "ZZB_One": "今日增持占总股本比‰",
        }
        stock_df.rename(columns=rename_columns, inplace=True)
        for col in rename_columns.values():
            stock_df = stock_df[stock_df[col] != '-']
            if col not in {'股票代码', '股票名称', '所属版块', '所属行业', '行业代码', '所属地区', '地区代码'}:
                stock_df[col] = stock_df[col].astype(float)

        drop_coumns = [f for f in stock_df.columns.tolist() if f not in set(rename_columns.values())]
        stock_df.drop(drop_coumns, axis=1, inplace=True)
        return HdDate, stock_df

    def fetch_stock_commodity_rank(self):
        """
        个股大宗交易排名
        http://data.eastmoney.com/dzjy/dzjy_mrtj.html
        """
        page = 1
        page_size = 10000
        trade_date = datetime.now().date()

        while True:
            url = f'http://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TURNOVERRATE&sortTypes=-1&pageSize={page_size}&pageNumber={page}&reportName=RPT_BLOCKTRADE_STA&columns=TRADE_DATE%2CSECURITY_CODE%2CSECUCODE%2CSECURITY_NAME_ABBR%2CCHANGE_RATE%2CCLOSE_PRICE%2CAVERAGE_PRICE%2CPREMIUM_RATIO%2CDEAL_NUM%2CVOLUME%2CDEAL_AMT%2CTURNOVERRATE%2CD1_CLOSE_ADJCHRATE%2CD5_CLOSE_ADJCHRATE%2CD10_CLOSE_ADJCHRATE%2CD20_CLOSE_ADJCHRATE&source=WEB&client=WEB&filter=(TRADE_DATE%3D%27{str(trade_date)}%27)'

            self.headers['Host'] = "datacenter-web.eastmoney.com"
            self.headers['Referer'] = "http://data.eastmoney.com/"
            self.headers[
                'Cookie'] = 'intellpositionL=1152px; IsHaveToNewFavor=0; qgqp_b_id=dbe20efaab3321e948962637a37ac894; em-quote-version=topspeed; em_hq_fls=js; emhq_picfq=2; _qddaz=QD.fqkydg.323wae.klgkordo; st_si=68830202953408; emshistory=%5B%22%E5%8C%97%E5%90%91%E8%B5%84%E9%87%91%22%2C%22%E9%BB%84%E5%8D%8E%E6%9F%92%22%2C%22603501%22%2C%22603501.SH%22%2C%22%E7%AB%8B%E8%AE%AF%E7%B2%BE%E5%AF%86%22%2C%22%E9%87%91%E9%BE%99%E9%B1%BC%22%2C%22000001%22%2C%22%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85%22%5D; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; testtc=0.5378301696721359; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=06-23 23:41:40@#$%u5357%u534E%u4E30%u6DF3%u6DF7%u5408A@%23%24005296; sid=112627825; vtpst=|; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300999-%u91D1%u9F99%u9C7C%2Ca-sh-600199-%u91D1%u79CD%u5B50%u9152%2Ca-sh-601279-%u82F1%u5229%u6C7D%u8F66%2Ca-sz-002261-%u62D3%u7EF4%u4FE1%u606F%2Ca-sz-002570-%u8D1D%u56E0%u7F8E%2Ca-sz-000150-%u5B9C%u534E%u5065%u5EB7%2Ca-sz-300785-%u503C%u5F97%u4E70%2Ca-sz-003039-%u987A%u63A7%u53D1%u5C55%2Ca-sz-000158-%u5E38%u5C71%u5317%u660E%2Ca-sz-002044-%u7F8E%u5E74%u5065%u5EB7%2Ca-sz-002475-%u7ACB%u8BAF%u7CBE%u5BC6; cowCookie=true; cowminicookie=true; ct=G0hDUs9gKQi4aW3xEvD_nUrvLeySSKACcjb7pt3PMuXGFTG6vFrXgU2TgPWTwf0rdVDMadZVeZigKBdt7gEhjYNn-RAz71rx4ymc2WaoxFJ_DrbmougHAvgzabrvCDKIsufTnqqSWBv6Q7YBPwmh9axru9ZquwZx92r6AdmT8Wg; ut=FobyicMgeV6oOlrtxUaVohmqCX7oh_O3yYZj6h8pdH-y_j-3oLUInf8bY9Ltl5f6Ki3pD_dO18HVqwCVuj1QyYJHLPkGETogY_ap7tz0wKJXzFJDtSmVcrzoevDqsYUBPGCv5dW5brKbArK3fBLyWzpQgl5n5MAk_OzmiEqnm51rW36tdorfCNXhVKg5yk-63EQHMLUW9L6Udk014KnVVkrMRaKd8abrVT_Gjm9muJBGNT39TG5KMpoZ62yiZy6FoSafAw4HWQIOqXw-mDGlHNghBD8PfPjD; st_asi=delete; intellpositionT=708px; JSESSIONID=22EE02E35CAF6CCCDE9D3E0D02F7AFFF; st_pvi=89273277965854; st_sp=2020-07-21%2011%3A22%3A06; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2FBK0473.html; st_sn=222; st_psi=20210708150358412-113300300970-2924897269'

            resp = requests.get(url, headers=self.headers)
            resp.encoding = 'utf8'
            stock_datas = json.loads(resp.text)['result']

            if stock_datas is not None and len(stock_datas) > 0:
                stock_datas = stock_datas['data']
                break
            trade_date = trade_date + timedelta(days=-1)

        stock_df = pd.DataFrame(stock_datas)
        rename_columns = {
            "SECURITY_CODE": "股票代码",
            "SECURITY_NAME_ABBR": "股票名称",
            "CHANGE_RATE": "当日涨跌幅",
            "CLOSE_PRICE": "当日收盘价",
            "AVERAGE_PRICE": "大宗交易均价",
            "PREMIUM_RATIO": "大宗交易折溢率",
            "DEAL_NUM": "大宗交易笔数",
            "VOLUME": "成交总量(万股)",
            "DEAL_AMT": "成交总额(万元)",
            "TURNOVERRATE": "成交总额/流通市值"
        }
        stock_df.rename(columns=rename_columns, inplace=True)
        for col in rename_columns.values():
            stock_df = stock_df[stock_df[col] != '-']
            if col not in {'股票代码', '股票名称'}:
                stock_df[col] = stock_df[col].astype(float)

        drop_coumns = [f for f in stock_df.columns.tolist() if f not in set(rename_columns.values())]
        stock_df.drop(drop_coumns, axis=1, inplace=True)
        return trade_date, stock_df

    def fetch_stock_institutional_research_rank(self):
        """
        个股机构调研情况排名
        http://data.eastmoney.com/jgdy/
        """
        page = 1
        page_size = 1000
        cur_date = datetime.now().date()
        time_token = int(time.time() * 1000)
        url = f'https://datainterface3.eastmoney.com/EM_DataCenter_V3/api/JGDYHZ/GetJGDYMX?tkn=eastmoney&secuCode=&sortfield=0&sortdirec=1&pageNum={page}&pageSize={page_size}&cfg=jgdyhz&p=1&pageNo=1&_={time_token}'

        self.headers['Host'] = "datainterface3.eastmoney.com"
        self.headers['Referer'] = "http://data.eastmoney.com/"
        self.headers[
            'Cookie'] = 'intellpositionL=1152px; IsHaveToNewFavor=0; qgqp_b_id=dbe20efaab3321e948962637a37ac894; em-quote-version=topspeed; em_hq_fls=js; emhq_picfq=2; _qddaz=QD.fqkydg.323wae.klgkordo; st_si=68830202953408; emshistory=%5B%22%E5%8C%97%E5%90%91%E8%B5%84%E9%87%91%22%2C%22%E9%BB%84%E5%8D%8E%E6%9F%92%22%2C%22603501%22%2C%22603501.SH%22%2C%22%E7%AB%8B%E8%AE%AF%E7%B2%BE%E5%AF%86%22%2C%22%E9%87%91%E9%BE%99%E9%B1%BC%22%2C%22000001%22%2C%22%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85%22%5D; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; testtc=0.5378301696721359; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=06-23 23:41:40@#$%u5357%u534E%u4E30%u6DF3%u6DF7%u5408A@%23%24005296; sid=112627825; vtpst=|; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300999-%u91D1%u9F99%u9C7C%2Ca-sh-600199-%u91D1%u79CD%u5B50%u9152%2Ca-sh-601279-%u82F1%u5229%u6C7D%u8F66%2Ca-sz-002261-%u62D3%u7EF4%u4FE1%u606F%2Ca-sz-002570-%u8D1D%u56E0%u7F8E%2Ca-sz-000150-%u5B9C%u534E%u5065%u5EB7%2Ca-sz-300785-%u503C%u5F97%u4E70%2Ca-sz-003039-%u987A%u63A7%u53D1%u5C55%2Ca-sz-000158-%u5E38%u5C71%u5317%u660E%2Ca-sz-002044-%u7F8E%u5E74%u5065%u5EB7%2Ca-sz-002475-%u7ACB%u8BAF%u7CBE%u5BC6; cowCookie=true; cowminicookie=true; ct=G0hDUs9gKQi4aW3xEvD_nUrvLeySSKACcjb7pt3PMuXGFTG6vFrXgU2TgPWTwf0rdVDMadZVeZigKBdt7gEhjYNn-RAz71rx4ymc2WaoxFJ_DrbmougHAvgzabrvCDKIsufTnqqSWBv6Q7YBPwmh9axru9ZquwZx92r6AdmT8Wg; ut=FobyicMgeV6oOlrtxUaVohmqCX7oh_O3yYZj6h8pdH-y_j-3oLUInf8bY9Ltl5f6Ki3pD_dO18HVqwCVuj1QyYJHLPkGETogY_ap7tz0wKJXzFJDtSmVcrzoevDqsYUBPGCv5dW5brKbArK3fBLyWzpQgl5n5MAk_OzmiEqnm51rW36tdorfCNXhVKg5yk-63EQHMLUW9L6Udk014KnVVkrMRaKd8abrVT_Gjm9muJBGNT39TG5KMpoZ62yiZy6FoSafAw4HWQIOqXw-mDGlHNghBD8PfPjD; st_asi=delete; st_pvi=89273277965854; st_sp=2020-07-21%2011%3A22%3A06; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2FBK0473.html; st_sn=224; st_psi=20210708160232686-113300301541-4842351849; intellpositionT=2071px'

        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf8'
        stock_datas = json.loads(resp.text)['Data'][0]

        column_names = stock_datas['FieldName'].split(',')
        stock_datas = stock_datas['Data']

        stock_data_list = []
        for stock in stock_datas:
            stock_data_list.append(stock.split('|'))

        stock_df = pd.DataFrame(stock_data_list, columns=column_names)

        rename_columns = {
            "SCode": "股票代码",
            "SName": "股票名称",
            "OrgSum": "接待机构数量",
            "StartDate": "接待日期",
            "NoticeDate": "公告日期",
        }
        stock_df.rename(columns=rename_columns, inplace=True)
        for col in rename_columns.values():
            stock_df = stock_df[stock_df[col] != '-']

        drop_coumns = [f for f in stock_df.columns.tolist() if f not in set(rename_columns.values())]
        stock_df.drop(drop_coumns, axis=1, inplace=True)
        return cur_date, stock_df

    def fetch_realtime_kline_bar_data(self, code):
        """
        获取个股的实时行情数据
        """
        raise NotImplementedError
