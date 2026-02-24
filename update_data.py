#!/usr/bin/env python3
"""
每日股票数据更新脚本
获取寒武纪和摩尔线程的最新股票数据并追加到CSV文件
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

def get_latest_stock_data():
    """获取最新的股票数据"""
    try:
        # 获取今天的日期
        today = datetime.now().strftime('%Y%m%d')
        
        # 获取寒武纪数据 (688256)
        print(f"正在获取寒武纪数据...")
        cambricon_df = ak.stock_zh_a_hist(symbol="688256", period="daily", start_date=today, end_date=today, adjust="")
        
        if cambricon_df.empty:
            # 如果今天没有数据，尝试获取最近一天
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            cambricon_df = ak.stock_zh_a_hist(symbol="688256", period="daily", start_date=yesterday, end_date=today, adjust="")
            if not cambricon_df.empty:
                cambricon_df = cambricon_df.tail(1)
        
        if cambricon_df.empty:
            print("未找到寒武纪数据")
            return None
        
        # 获取摩尔线程数据 (2438.HK)
        print(f"正在获取摩尔线程数据...")
        try:
            moore_df = ak.stock_hk_hist(symbol="02438", period="daily", start_date=today.replace('-', ''), end_date=today.replace('-', ''), adjust="qfq")
            if moore_df.empty:
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
                moore_df = ak.stock_hk_hist(symbol="02438", period="daily", start_date=yesterday.replace('-', ''), end_date=today.replace('-', ''), adjust="qfq")
                if not moore_df.empty:
                    moore_df = moore_df.tail(1)
        except Exception as e:
            print(f"获取摩尔线程数据失败: {e}")
            moore_df = pd.DataFrame()
        
        # 获取中证半导体指数
        print(f"正在获取中证半导体指数...")
        try:
            sector_df = ak.stock_zh_index_daily(symbol="sh000991")
            sector_df = sector_df.tail(1)
        except Exception as e:
            print(f"获取行业指数失败: {e}")
            sector_df = pd.DataFrame()
        
        # 提取数据
        date = cambricon_df.iloc[0]['日期']
        cambricon_price = float(cambricon_df.iloc[0]['收盘'])
        cambricon_change = float(cambricon_df.iloc[0]['涨跌幅'])
        cambricon_turnover = float(cambricon_df.iloc[0]['换手率'])
        
        # 计算寒武纪市值（亿元）
        # 总股本约47亿股
        cambricon_market_cap = round(cambricon_price * 47, 2)
        
        # 摩尔线程数据
        if not moore_df.empty:
            moore_price = float(moore_df.iloc[0]['收盘'])
            moore_change = float(moore_df.iloc[0]['涨跌幅'])
            # 摩尔线程总股本约47亿股，港币
            moore_market_cap = round(moore_price * 47 * 0.92, 2)  # 港币转人民币约0.92
        else:
            moore_price = None
            moore_change = None
            moore_market_cap = None
        
        # 行业指数数据
        if not sector_df.empty:
            sector_index = float(sector_df.iloc[0]['close'])
            # 计算涨跌幅
            if len(sector_df) > 1:
                prev_close = float(sector_df.iloc[-2]['close'])
                sector_change = round((sector_index - prev_close) / prev_close * 100, 2)
            else:
                sector_change = 0.0
        else:
            sector_index = None
            sector_change = None
        
        return {
            'date': date,
            'cambricon_price': cambricon_price,
            'cambricon_change': cambricon_change,
            'cambricon_turnover': cambricon_turnover,
            'cambricon_market_cap': cambricon_market_cap,
            'moore_price': moore_price,
            'moore_change': moore_change,
            'moore_market_cap': moore_market_cap,
            'sector_index': sector_index,
            'sector_change': sector_change
        }
    
    except Exception as e:
        print(f"获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_csv(data):
    """更新CSV文件"""
    csv_file = 'data/stock_data.csv'
    
    # 读取现有数据
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        
        # 检查是否已存在该日期的数据
        if data['date'] in df['date'].values:
            print(f"日期 {data['date']} 的数据已存在，跳过更新")
            return False
    else:
        df = pd.DataFrame()
    
    # 追加新数据
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # 保存
    df.to_csv(csv_file, index=False)
    print(f"成功更新数据: {data['date']}")
    return True

if __name__ == '__main__':
    print("开始获取股票数据...")
    data = get_latest_stock_data()
    
    if data:
        print(f"获取到数据: {data}")
        if update_csv(data):
            print("数据更新成功！")
            sys.exit(0)
        else:
            print("数据已是最新")
            sys.exit(0)
    else:
        print("获取数据失败")
        sys.exit(1)
