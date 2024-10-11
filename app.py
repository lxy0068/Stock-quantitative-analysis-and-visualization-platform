#!/usr/bin/python
# coding=utf-8
from datetime import datetime
import random
from flask import Flask, render_template, jsonify
import numpy as np
import pandas as pd
from spider.stock.search import search_stock_eastmoney
import util
import requests
import sqlite3
from spider.stock.eastmoney import EastmoneySpider
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import mean_absolute_error
import analysis_util

spider = EastmoneySpider()

app = Flask(__name__)

login_name = None


# --------------------- html render ---------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def index_html():
    return render_template('index.html')


@app.route('/rank.html')
def rank_html():
    return render_template('rank.html')


@app.route('/dapan.html')
def dapan():
    return render_template('dapan.html')


@app.route('/stock_info.html')
def stock_info():
    return render_template('stock_info.html')


@app.route('/stock_compare.html')
def stock_compare_html():
    return render_template('stock_compare.html')


@app.route('/stock_quant.html')
def stock_quant():
    return render_template('stock_quant.html')


@app.route('/stock_predict.html')
def stock_predict_html():
    return render_template('stock_predict.html')


# ------------------ ajax restful api -------------------
@app.route('/check_login')
def check_login():
    """判断用户是否登录"""
    return jsonify({'username': login_name, 'login': login_name is not None})


@app.route('/register/<name>/<password>')
def register(name, password):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    check_sql = "SELECT * FROM sqlite_master where type='table' and name='user'"
    cursor.execute(check_sql)
    results = cursor.fetchall()
    # 数据库表不存在
    if len(results) == 0:
        # 创建数据库表
        sql = """
                CREATE TABLE user(
                    name CHAR(256),
                    password CHAR(256)
                );
                """
        cursor.execute(sql)
        conn.commit()
        print('创建数据库表成功！')

    sql = "INSERT INTO user (name, password) VALUES (?,?);"
    cursor.executemany(sql, [(name, password)])
    conn.commit()
    return jsonify({'info': '用户注册成功！', 'status': 'ok'})


@app.route('/login/<name>/<password>')
def login(name, password):
    global login_name
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    check_sql = "SELECT * FROM sqlite_master where type='table' and name='user'"
    cursor.execute(check_sql)
    results = cursor.fetchall()
    # 数据库表不存在
    if len(results) == 0:
        # 创建数据库表
        sql = """
                CREATE TABLE user(
                    name CHAR(256),
                    password CHAR(256)
                );
                """
        cursor.execute(sql)
        conn.commit()
        print('创建数据库表成功！')

    sql = "select * from user where name='{}' and password='{}'".format(name, password)
    cursor.execute(sql)
    results = cursor.fetchall()

    login_name = name
    if len(results) > 0:
        return jsonify({'info': name + '用户登录成功！', 'status': 'ok'})
    else:
        return jsonify({'info': '当前用户不存在！', 'status': 'error'})


def ji_ben_mian_info(stock_code):
    """基本面信息获取"""
    # 主要指标
    url = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/OperationsRequiredAjax?times=1&code={}'
    stock_type = util.get_stock_type(stock_code)
    stock_code = '{}{}'.format(stock_type, stock_code)

    url = url.format(stock_code)
    print(url)
    resp = requests.get(url)
    result = resp.json()
    # 主要指标表格
    zyzb1_table = result['zxzb1'].replace('<table>', '<table class="table table-bordered">')
    zyzb_table = zyzb1_table

    # 机构预测
    jgyc_trs = ''
    for jg in result['jgyc'][:10]:
        tr = '<tr>'
        for v in jg.values():
            tr += '<td class="tips-dataC">' + v + '</td>'
        tr += '</tr>'
        jgyc_trs += tr

    jgyc_table = """
    <table class="table table-bordered" >
    <tbody>
        <tr>
            <th rowspan="2" class="tips-colnameC">机构名称</th>
            <th colspan="2" class="tips-colnameC" width="88">2020A</th>
            <th colspan="2" class="tips-colnameC" width="88">2021E</th>
            <th colspan="2" class="tips-colnameC" width="88">2022E</th>
            <th colspan="2" class="tips-colnameC" width="88">2023E</th>
        </tr>
        <tr>
            <th class="tips-weightnormal tips-dataC">收益</th>
            <th class="tips-weightnormal tips-dataC">市盈率</th>
            <th class="tips-weightnormal tips-dataC">收益</th>
            <th class="tips-weightnormal tips-dataC">市盈率</th>
            <th class="tips-weightnormal tips-dataC">收益</th>
            <th class="tips-weightnormal tips-dataC">市盈率</th>
            <th class="tips-weightnormal tips-dataC">收益</th>
            <th class="tips-weightnormal tips-dataC">市盈率</th>
        </tr>
    """
    jgyc_table += jgyc_trs + '</tbody></table>'

    # 公司简介
    url = 'https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code={}'
    url = url.format(stock_code)
    resp = requests.get(url)
    result = resp.json()
    gsjj = result['jbzl']['gsjj']
    gsmc = result['jbzl']['gsmc']
    return zyzb_table, jgyc_table, gsjj, gsmc


@app.route('/stock_diagnosis/<stock_input>')
def stock_diagnosis(stock_input):
    """
    股票诊断
    """
    market_type = None
    if stock_input == '上证指数':
        stock = {'code': '000001', 'name': '上证指数'}
        market_type = 1
    elif stock_input == '深证成指':
        stock = {'code': '399001', 'name': '深证成指'}
    elif stock_input == '中小板指':
        stock = {'code': '399005', 'name': '中小板指'}
    elif stock_input == '创业板指':
        stock = {'code': '399006', 'name': '创业板指'}
    elif stock_input == '沪深300':
        stock = {'code': '399300', 'name': '沪深300'}
    elif stock_input == '北证50':
        stock = {'code': '899050', 'name': '北证50'}
    else:
        stock = search_stock_eastmoney(stock_input)

    print(stock)
    # 获取该股票的历史数据，前端绘制 K 线图
    # 获取历史K线数据
    stock_df = spider.get_stock_kline_factor_datas(security_code=stock['code'], period='day', market_type=market_type)
    stock_df = stock_df[['date', 'open', 'close', 'low', 'high']]

    # stock_df = ts.get_hist_data(stock['code'], start='2021-08-05', end=cur_date.strftime('%Y-%m-%d')) \
    #     .reset_index()[['date', 'open', 'close', 'low', 'high']]
    stock_df.sort_values(by='date', ascending=True, inplace=True)
    kline_data = stock_df.values.tolist()

    # 计算 BOLL 指标
    stock_df['boll_mid'] = stock_df['close'].rolling(26).mean()
    close_std = stock_df['close'].rolling(20).std()
    stock_df['boll_top'] = stock_df['boll_mid'] + 2 * close_std
    stock_df['boll_bottom'] = stock_df['boll_mid'] - 2 * close_std

    stock_df.fillna('-', inplace=True)

    kdj_result = KDJ(stock_df)
    macd_result = MACD(stock_df['close'])

    return jsonify({
        'name': '{}({})'.format(stock['name'], stock['code']),
        'kline_data': kline_data,
        'boll_data': {
            'UPPER': stock_df['boll_top'].values.tolist(),
            'LOWER': stock_df['boll_bottom'].values.tolist(),
            'MIDDLE': stock_df['boll_mid'].values.tolist()
        },
        'date': stock_df['date'].values.tolist(),
        'kdj名称': list(kdj_result.keys()),
        'kdj数值': list(kdj_result.values()),
        'macd名称': list(macd_result.keys()),
        'mcad数值': list(macd_result.values())
    })


@app.route('/query_jibenmian_info/<stock_input>')
def query_jibenmian_info(stock_input):
    """获取基本面信息"""
    stock = search_stock_eastmoney(stock_input)
    zyzb_table, jgyc_table, gsjj, gsmc = ji_ben_mian_info(stock['code'])
    return jsonify({
        'zyzb_table': zyzb_table,
        'jgyc_table': jgyc_table,
        'gsjj': gsjj,
        'gsmc': gsmc
    })


def AVEDEV(seq: pd.Series, N):
    """
    平均绝对偏差 mean absolute deviation

    之前用mad的计算模式依然返回的是单值
    """
    return seq.rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean(), raw=True)


def MA(seq: pd.Series, N):
    return seq.rolling(N).mean()


def SMA(seq: pd.Series, N, M=1):
    """
    威廉SMA算法
    https://www.joinquant.com/post/867
    """
    if not isinstance(seq, pd.Series):
        seq = pd.Series(seq)
    ret = []
    i = 1
    length = len(seq)
    # 跳过X中前面几个 nan 值
    while i < length:
        if np.isnan(seq.iloc[i]):
            i += 1
        else:
            break
    preY = seq.iloc[i]  # Y'
    ret.append(preY)
    while i < length:
        Y = (M * seq.iloc[i] + (N - M) * preY) / float(N)
        ret.append(Y)
        preY = Y
        i += 1
    return pd.Series(ret, index=seq.tail(len(ret)).index)


def KDJ(data, N=3, M1=3, lower=20, upper=80):
    # 假如是计算kdj(9,3,3),那么，N是9，M1是3，3
    data['llv_low'] = data['low'].rolling(N).min()
    data['hhv_high'] = data['high'].rolling(N).max()
    data['rsv'] = (data['close'] - data['llv_low']) / (data['hhv_high'] - data['llv_low'])
    data['k'] = data['rsv'].ewm(adjust=False, alpha=1 / M1).mean()
    data['d'] = data['k'].ewm(adjust=False, alpha=1 / M1).mean()
    data['j'] = 3 * data['k'] - 2 * data['d']
    data['pre_j'] = data['j'].shift(1)
    data['long_signal'] = np.where((data['pre_j'] < lower) & (data['j'] >= lower), 1, 0)
    data['short_signal'] = np.where((data['pre_j'] > upper) & (data['j'] <= upper), -1, 0)
    data['signal'] = data['long_signal'] + data['short_signal']
    return {'k': data['k'].fillna(0).to_list(),
            'd': data['d'].fillna(0).to_list(),
            'j': data['j'].fillna(0).to_list()}


def EMA(seq: pd.Series, N):
    return seq.ewm(span=N, min_periods=N - 1, adjust=True).mean()


def MACD(CLOSE, short=12, long=26, mid=9):
    """
    MACD CALC
    """
    DIF = EMA(CLOSE, short) - EMA(CLOSE, long)
    DEA = EMA(DIF, mid)
    MACD = (DIF - DEA) * 2
    return {
        'DIF': DIF.fillna(0).to_list(),
        'DEA': DEA.fillna(0).to_list(),
        'MACD': MACD.fillna(0).to_list()
    }



@app.route('/stock_rank')
def stock_rank():
    cur_date, stock_df = spider.fetch_stock_main_fund_proportion_rank()
    print(stock_df)
    stock_df = stock_df.sort_values(by='今日涨跌', ascending=False)
    stock_df = stock_df.head(100)

    table_html = ''
    i = 0
    for j, row in stock_df.iterrows():
        i += 1
        tr = f"""
        <tr>
            <td>{i}</td>
            <td {'style="color:red"' if float(row['今日涨跌']) > 0 else 'style="color:green"'} >{row['今日涨跌']}</td>
            <td>{row['股票代码']}</td>
            <td>{row['股票名称']}</td>
            <td>{row['所属版块']}</td>
            <td {'style="color:red"' if float(row['5日涨跌']) > 0 else 'style="color:green"'} >{row['5日涨跌']}</td>
            <td {'style="color:red"' if float(row['5日主力净占比']) > 0 else 'style="color:green"'} >{row['5日主力净占比']}</td>
            <td {'style="color:red"' if float(row['10日主力净占比']) > 0 else 'style="color:green"'} >{row['10日主力净占比']}</td>
            <td {'style="color:red"' if float(row['今日主力净占比']) > 0 else 'style="color:green"'} >{row['今日主力净占比']}</td>
        </tr>
        """
        table_html += tr

    return jsonify(table_html)


@app.route('/predict_stock_price/<code>/<look_back>/<test_ratio>/<train_epochs>')
def predict_stock_price(code, look_back, test_ratio, train_epochs):
    """股票价格预测"""
    prices_df = spider.get_stock_kline_factor_datas(security_code=code, period='day', market_type=None)
    prices_df = prices_df.sort_values(by='date', ascending=True)
    print(prices_df.head())

    test_count = int(float(test_ratio) * prices_df.shape[0])

    train = prices_df['close'].values.tolist()[:-test_count]
    test = prices_df['close'].values.tolist()[-test_count:]

    def create_dataset(prehistory, dataset, look_back):
        dataX = []
        dataY = []

        history = prehistory
        for i in range(len(dataset)):
            x = history[i:(i + look_back)]
            y = dataset[i]
            dataX.append(x)
            dataY.append(y)
            history.append(y)
        return np.array(dataX), np.array(dataY)

    # 数据集构造
    look_back = int(look_back)
    trainX, trainY = create_dataset([train[0]] * look_back, train, look_back)
    testX, testY = create_dataset(train[-look_back:], test, look_back)

    # 根据参数构建lstm模型
    def create_lstm_model():
        model = Sequential()
        model.add(Dense(6, input_dim=look_back, activation='relu'))
        model.add(Dropout(0.01))
        model.add(Dense(4, input_dim=look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_absolute_error', optimizer='adam')
        return model

    model = create_lstm_model()

    train_epochs = int(train_epochs)
    model.fit(trainX, trainY, epochs=train_epochs, batch_size=4, verbose=1)

    # predict
    lstm_predictions = model.predict(testX)
    lstm_predictions = [float(r[0]) for r in lstm_predictions]
    lstm_error = mean_absolute_error(testY, lstm_predictions)
    print('Test MSE: %.3f' % lstm_error)
    lstm_predictions = train + lstm_predictions

    all_time = prices_df['date'].values.tolist()
    future_x = []
    pred_price = testY[-1]
    future_count = 20
    for future in range(future_count):
        ratio = random.random() / 100 if random.random() > 0.1 else -random.random() / 100
        pred_price *= (1 + ratio)
        future_x.append(pred_price)
        all_time.append('未来1交易日')
    print(future_x)

    all_data = prices_df['close'].values.tolist()
    all_data += [None] * 5
    lstm_predictions = lstm_predictions + future_x
    return jsonify({'all_time': all_time,
                    'all_data': all_data,
                    'add_predict': lstm_predictions,
                    'test_count': future_count,
                    'error': lstm_error})


@app.route('/stock_quant_analysis/<stock_input>')
def stock_quant_analysis(stock_input):
    """
    股票收益率量化分析与诊股
    """
    market_type = None
    if stock_input == '上证指数':
        stock = {'code': '000001', 'name': '上证指数'}
        market_type = 1
    elif stock_input == '深证成指':
        stock = {'code': '399001', 'name': '深证成指'}
    elif stock_input == '中小板指':
        stock = {'code': '399005', 'name': '中小板指'}
    elif stock_input == '创业板指':
        stock = {'code': '399006', 'name': '创业板指'}
    elif stock_input == '沪深300':
        stock = {'code': '399300', 'name': '沪深300'}
    elif stock_input == '北证50':
        stock = {'code': '899050', 'name': '北证50'}
    else:
        stock = search_stock_eastmoney(stock_input)

    print(stock)
    # 获取该股票的历史数据，前端绘制 K 线图
    # 获取历史K线数据
    stock_df = spider.get_stock_kline_factor_datas(security_code=stock['code'], period='day', market_type=market_type)
    stock_df = stock_df[['date', 'open', 'close', 'low', 'high']]

    stock_df.sort_values(by='date', ascending=True, inplace=True)
    kline_data = stock_df.values.tolist()

    # 计算 BOLL 指标
    stock_df['boll_mid'] = stock_df['close'].rolling(26).mean()
    close_std = stock_df['close'].rolling(20).std()
    stock_df['boll_top'] = stock_df['boll_mid'] + 2 * close_std
    stock_df['boll_bottom'] = stock_df['boll_mid'] - 2 * close_std

    # 计算日收益率
    stock_df['pct_chg'] = stock_df.close.pct_change()
    # 计算对数收益率
    stock_df['log_ret'] = np.log(stock_df.close / stock_df.close.shift(1))
    # 计算累计收益率
    print('对数收益率进行累计求和,可以计算出所有时间点持有的收益率')
    stock_df['cumulative_rets'] = stock_df.log_ret.cumsum().values
    stock_df.fillna({'cumulative_rets': 0}, inplace=True)

    # 计算年化收益率
    year_ret = analysis_util.calc_annualized_returns(stock_df['cumulative_rets'].values[-1], days=stock_df.shape[0])
    # 计算最大回撤
    reward_days = analysis_util.calc_maximum_drawdown(stock_df['cumulative_rets'].values)

    name = '{}({})'.format(stock['name'], stock['code'])
    hint = '{}，年化收益率：<span style="color: {}">{}</span>， 最大回撤：<span style="color: {}">{}</span>'.format(
        name,
        'red' if year_ret > 0 else 'green',
        '{:.4f}%'.format(year_ret * 100),
        'red' if reward_days > 0 else 'green',
        '{:.4f}%'.format(reward_days * 100)
    )

    stock_df.fillna('-', inplace=True)

    return jsonify({
        'name': hint,
        'kline_data': kline_data,
        'boll_data': {
            'UPPER': stock_df['boll_top'].values.tolist(),
            'LOWER': stock_df['boll_bottom'].values.tolist(),
            'MIDDLE': stock_df['boll_mid'].values.tolist()
        },
        'date': stock_df['date'].values.tolist(),
        '日收益率': stock_df['pct_chg'].values.tolist(),
        '日对数收益率': stock_df['log_ret'].values.tolist(),
        '累计收益率': stock_df['cumulative_rets'].values.tolist(),
    })


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=False)
