import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

import akshare as ak

# 获取数据
stock_yjyg_em_df = ak.stock_yjyg_em(date="20241231")

# 检查数据是否存在
if stock_yjyg_em_df is None:
    print("未获取到数据，请检查参数或重试。")
else:
    # 保存为 Excel 文件
    stock_yjyg_em_df.to_excel("stock_yjyg_em_data.xlsx", index=False)
    print("数据已保存到 stock_yjyg_em_data.xlsx")