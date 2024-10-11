#!/usr/bin/python
# _*_ coding: utf-8 _*_
import numpy as np


def calc_alpha(annualized_returns, benchmark_annualized_returns, beta, rf):
    """
    投资中面临着系统性风险（即Beta）和非系统性风险（即Alpha），Alpha是投资者获得与市场波动无关的回报。
    比如投资者获得了15%的回报，其基准获得了10%的回报，那么Alpha或者价值增值的部分就是5%。
    α>0	策略相对于风险，获得了超额收益
    α=0	策略相对于风险，获得了适当收益
    α<0	策略相对于风险，获得了较少收益

    Alpha=α=Rp−[Rf+βp(Rm−Rf)]
    Rp=策略年化收益率
    Rm=基准年化收益率
    Rf=无风险利率（默认0.04）
    βp=策略beta值
    """
    alpha = (annualized_returns - rf) - beta * (benchmark_annualized_returns - rf)
    return alpha


def calc_beta(assest_profit, benchmark_profit):
    """
    贝塔

    表示投资的系统性风险，反映了策略对大盘变化的敏感性。例如一个策略的Beta为1.5，则大盘涨1%的时候，策略可能涨1.5%，反之亦然；
    如果一个策略的Beta为-1.5，说明大盘涨1%的时候，策略可能跌1.5%，反之亦然。

    β<0	投资组合和基准的走向通常反方向，如空头头寸类
    β=0	投资组合和基准的走向没有相关性，如固定收益类
    0<β<1	投资组合和基准的走向相同，但是比基准的移动幅度更小
    β=1	投资组合和基准的走向相同，并且和基准的移动幅度贴近
    β>1	投资组合和基准的走向相同，但是比基准的移动幅度更大

    Beta=βp=Cov(Dp,Dm) / Var(Dm)
    Dp=策略每日收益
    Dm=基准每日收益
    Cov(Dp,Dm)=策略每日收益与基准每日收益的协方差
    Var(Dm)=基准每日收益的方差
    """
    if len(assest_profit) < len(benchmark_profit):
        for i in range(0, len(benchmark_profit) - len(assest_profit), 1):
            assest_profit.append(0)
    elif len(assest_profit) > len(benchmark_profit):
        for i in range(0, len(assest_profit) - len(benchmark_profit), 1):
            benchmark_profit.append(0)
    calc_cov = np.cov(assest_profit, benchmark_profit)
    beta = calc_cov[0, 1] / calc_cov[1, 1]
    return beta


def calc_annualized_returns(total_returns, days):
    """
    策略年化收益
    Total Annualized Returns = Rp = ((1+P)^250/n − 1) ∗ 100%
    P=策略收益
    n=策略执行天数
    """
    return np.power(1 + total_returns, 250 / days) - 1


def calc_volatility(daily_yields, days):
    """
    用来测量策略的风险性，波动越大代表策略风险越高。

    Algorithm Volatility = σp = square(250 / (n-1) * ∑<i=1..n>(rp−rp¯)^2 )
    rp=策略每日收益率
    rp¯=策略每日收益率的平均值=1n∑i=1nrpi
    n=策略执行天数
    """
    mean_daily_yields = np.mean(daily_yields)
    volatility = np.sqrt(250 / (days - 1) * np.sum(np.power(daily_yields - mean_daily_yields, 2)))
    return volatility


def calc_sharpe(annualized_returns, rf, volatility):
    """
    夏普比率，表示每承受一单位总风险，会产生多少的超额报酬，可以同时对策略的收益与风险进行综合考虑。

    Sharpe Ratio=(Rp−Rf) / σp
    Rp=策略年化收益率
    Rf=无风险利率（默认0.04）
    σp=策略收益波动率
    """
    return (annualized_returns - rf) / volatility


def calc_win_prob(daily_yields):
    """
    胜率，盈利次数在总交易次数中的占比。

    胜率=盈利交易次数 / 总交易次数
    """
    abovez = 0
    belowz = 0
    for i in range(0, len(daily_yields) - 1, 1):
        if daily_yields[i] > 0:
            abovez = abovez + 1
        elif daily_yields[i] < 0:
            belowz = belowz + 1
    if belowz == 0:
        belowz = 1
    if abovez == 0:
        abovez = 1
    win_rate = abovez / (abovez + belowz)
    return win_rate


def calc_daily_success_rate(history_daily_yields, benchmark_index_yields):
    """
    日胜率，策略盈利超过基准盈利的天数在总交易数中的占比。

    日胜率 = 当日策略收益跑赢当日基准收益的天数 / 总交易日数
    """
    daily_wins = np.array(history_daily_yields) - np.array(benchmark_index_yields)
    daily_wins = daily_wins > 0
    daily_success_rate = sum(daily_wins) / len(daily_wins)
    return daily_success_rate


def clc_risk_to_reward_ratio(history_daily_yields):
    """
    盈亏比，盈利天数 / 亏损天数
    """
    history_daily_yields = np.array(history_daily_yields)
    # 盈利
    history_daily_yields = history_daily_yields > 0
    reward_days = sum(history_daily_yields)
    return 1.0 * reward_days / (len(history_daily_yields) - reward_days)


def calc_information_ratio(annualized_returns, benchmark_annualized_returns,
                           history_daily_yields, benchmark_daily_yields, days):
    """
    信息比率, 衡量单位超额风险带来的超额收益。信息比率越大，说明该策略单位跟踪误差所获得的超额收益越高，
    因此，信息比率较大的策略的表现要优于信息比率较低的基准。合理的投资目标应该是在承担适度风险下，
    尽可能追求高信息比率。

    Information Ratio = (Rp−Rm) / σt
    Rp=策略年化收益率
    Rm=基准年化收益率
    σt=策略与基准每日收益差值的年化标准差
    """
    daily_rewards = np.array(history_daily_yields) - np.array(benchmark_daily_yields)
    daily_rewards_std = np.std(daily_rewards)
    daily_rewards_year_std = np.power(1 + daily_rewards_std, 250 / days) - 1
    return (annualized_returns - benchmark_annualized_returns) / daily_rewards_year_std


def calc_maximum_drawdown(history_total_yields):
    """
    最大回撤，描述策略可能出现的最糟糕的情况，最极端可能的亏损情况。
    Max Drawdown = Max(Px − Py) / Px
    Px,Py=策略某日股票和现金的总价值，y>x
    """
    # TODO: need check!
    drops = []
    for i in range(1, len(history_total_yields), 1):
        maxs = max(history_total_yields[:i])
        cur = history_total_yields[i]
        drop = cur - maxs if maxs != 0 else 0
        drops.append(drop)
    max_drop = min(drops)
    return max_drop
