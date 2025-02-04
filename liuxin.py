import akshare as ak
import pandas as pd
import numpy as np
import concurrent.futures
import time

# 1. **获取 Wind 全 A 股票池**
stock_list = ak.stock_info_a_code_name()['code'].tolist()
stock_limit = len(stock_list)  # 设定测试股票数量（全部：len(stock_list)）
stock_list = stock_list[:stock_limit]
print(f"共获取 {len(stock_list)} 只 A 股股票")

# 将股票名单保存到 Excel 文件中
df_stock_list = pd.DataFrame(stock_list, columns=['Stock Code'])
df_stock_list.to_excel("stock_list.xlsx", index=False)
print("股票名单已保存到 stock_list.xlsx")
git remote add origin git@github.com:your_username/your_repository.git