# 寒武纪股票数据自动更新仓库

本仓库通过GitHub Actions每日自动更新寒武纪(688256)和摩尔线程的股票数据。

## 数据文件

- `data/stock_data.csv` - 每日股票数据（包含寒武纪和摩尔线程）

## 数据字段

| 字段 | 说明 |
|------|------|
| date | 日期 (YYYY-MM-DD) |
| cambricon_price | 寒武纪股价 |
| cambricon_change | 寒武纪涨跌幅 (%) |
| cambricon_turnover | 寒武纪换手率 (%) |
| cambricon_market_cap | 寒武纪市值 (亿元) |
| moore_price | 摩尔线程股价 |
| moore_change | 摩尔线程涨跌幅 (%) |
| moore_market_cap | 摩尔线程市值 (亿元) |
| sector_index | 中证半导体指数 |
| sector_change | 行业指数涨跌幅 (%) |

## 更新时间

每个交易日晚上20:00 (UTC+8) 自动更新

## 数据来源

- AKShare (https://akshare.akfamily.xyz/)
