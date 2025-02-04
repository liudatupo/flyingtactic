import pandas as pd
import yfinance as yf
import numpy as np

# 1. **获取 S&P 500 成分股列表**
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_tickers = pd.read_html(sp500_url)[0]['Symbol'].tolist()

# 2. **设定时间范围**
start_date = "2021-01-01"
end_date = "2024-01-01"

# 3. **初始化数据存储**
fundamentals = {}
momentum = {}

for ticker in sp500_tickers[:50]:  # 仅测试前50只股票，避免超时
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            continue

        # 计算动量因子（过去 12 个月收益率）
        momentum[ticker] = hist['Close'].pct_change(periods=252).iloc[-1]

        # 获取基本面数据
        info = stock.info
        pe_ratio = info.get('trailingPE', np.nan)  # 市盈率
        pb_ratio = info.get('priceToBook', np.nan)  # 市净率

        fundamentals[ticker] = {'PE': pe_ratio, 'PB': pb_ratio}
    
    except Exception as e:
        print(f"{ticker} 数据获取失败: {e}")

# 4. **整理数据**
df_fundamentals = pd.DataFrame.from_dict(fundamentals, orient='index')
df_momentum = pd.DataFrame.from_dict(momentum, orient='index', columns=['Momentum'])

df = df_fundamentals.join(df_momentum).dropna()  # 合并数据，并去除缺失值

# 5. **标准化评分**
df['PE_Score'] = 1 / df['PE']  # PE 低的股票得分高
df['PB_Score'] = 1 / df['PB']  # PB 低的股票得分高
df['Momentum_Score'] = df['Momentum']  # 动量高的股票得分高

# 计算综合评分（简单平均）
df['Total_Score'] = df[['PE_Score', 'PB_Score', 'Momentum_Score']].mean(axis=1)

# 6. **选择前 20 只最佳股票**
top_stocks = df.nlargest(20, 'Total_Score')

# 7. **输出结果**
print("\nTop 20 只精选股票：")
print(top_stocks[['PE', 'PB', 'Momentum', 'Total_Score']])