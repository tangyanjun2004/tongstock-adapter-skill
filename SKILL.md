---
name: tongstock-adapter-skill
description: "通达信股票数据分析技能 - 提供某只股票基本信息和技术指标查询，公司F10资料获取（包括：公司概况、财务分析、股本结、股东研究、机构持股、分红融资、高管治理、资金动向、资本运作、公司公告、公司报道、经营分析、研报评级等），和通过信号进行筛选的功能"
license: MIT
metadata:
  TONGSTOCK_BASE_URL: "http://localhost:8991"
---

# 通达信股票分析技能

## 功能概述

该技能通过封装 TongStock (https://github.com/tangyanjun2004/tongstock) HTTP API，提供强大的股票数据分析能力。支持以下核心功能：

1. **股票详细信息查询** - 获取股票的实时行情、财务数据、技术指标、分红信息等综合数据
2. **公司F10资料查询** - 获取公司概况、财务分析、股东研究等详细信息，并转换为Markdown格式
3. **股票信号筛选** - 根据技术指标信号（金叉、死叉、超买、超卖）筛选股票

## 前置条件

- Python 3.7+
- TongStock 服务运行地址可通过环境变量 `TONGSTOCK_BASE_URL` 配置，默认值为 `http://localhost:8991`
- 依赖包：requests, pytest

## 命令详解

### 1. 查询股票详细信息 (`info`)

获取单只股票的综合信息，包括实时行情、财务数据、技术指标、分红信息等。

**命令格式：**

```bash
python scripts/main.py info <股票代码> [--days <日K天数>] [--weeks <周K周数>] [--months <月K月数>]
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| 股票代码 | string | 是 | - | 股票代码，如 600519、000001 |
| --days, -d | int | 否 | 10 | 日K线技术指标数据天数 |
| --weeks, -w | int | 否 | 5 | 周K线技术指标数据周数 |
| --months, -m | int | 否 | 3 | 月K线技术指标数据月数 |

**返回格式：**

```json
{
  "code": "600519",
  "errors": [],
  "basic_info": {
    "name": "贵州茅台",
    "code": "600519",
    "total_shares": 125619.78,
    "float_shares": 125619.78,
    "nav_per_share": 180.52,
    "issued_shares": 125619.78,
    "listing_date": "2001-08-27"
  },
  "market_data": {
    "price": 1199.3,
    "change": 10.5,
    "change_pct": 0.883,
    "open": 1188.77,
    "high": 1200.98,
    "low": 1177.0,
    "last_close": 1188.8,
    "volume": 25776,
    "amount": 307193.344,
    "inner_volume": 11660,
    "outer_volume": 14116,
    "bid_ask": [
      {
        "BidPrice": 1199.0,
        "AskPrice": 1199.3,
        "BidVolume": 2,
        "AskVolume": 37
      }
    ]
  },
  "financial_info": {
    "net_profit": 7500000.0,
    "revenue": 15000000.0,
    "shareholders": 150000,
    "total_assets": 30000000.0,
    "net_assets": 20000000.0,
    "eps": 60.0,
    "pe_ratio": 20.0,
    "pb_ratio": 6.6,
    "operating_profit": 8000000.0,
    "gross_profit_margin": 91.5,
    "roe": 33.0
  },
  "technical_indicators": {
    "day": {
      "history": [
        {
          "timestamp": "2026-07-08",
          "kline": {
            "close": 1199.3,
            "open": 1188.77,
            "high": 1200.98,
            "low": 1177.0,
            "volume": 25776,
            "amount": 30719334.4,
            "change": 10.5,
            "change_pct": 0.883
          },
          "ma": {
            "ma5": 1198.49,
            "ma10": 1194.67,
            "ma20": 1222.34,
            "ma60": 1311.22,
            "ma120": 1370.68,
            "trend": "bearish"
          },
          "macd": {
            "dif": -27.90,
            "dea": -30.69,
            "hist": 2.80,
            "signal": "golden_cross"
          },
          "kdj": {
            "k": 55.59,
            "d": 43.88,
            "j": 79.03,
            "signal": "neutral"
          },
          "rsi": {
            "rsi6": 46.88,
            "rsi12": 41.60,
            "rsi24": 39.47,
            "signal": "neutral"
          },
          "boll": {
            "upper": 1292.13,
            "middle": 1222.34,
            "lower": 1152.55,
            "position": 0.33,
            "signal": "normal"
          },
          "volume": {
            "current": 25776,
            "avg5": 35849.6,
            "ratio": 0.72,
            "signal": "normal"
          },
          "signals": ["golden_cross", "空头排列"]
        }
      ],
      "summary": {
        "signal": "卖出",
        "strength": 30,
        "trend": "bearish"
      }
    },
    "week": {...},
    "month": {...}
  },
  "dividend_info": [
    {
      "Category": 1,
      "Date": "2025-06-25",
      "FenHong": 30.0,
      "SongGu": 0,
      "ZhuanGu": 0
    }
  ],
  "company_info": {
    "structure": ["最新提示", "公司概况", "财务分析", "股本结构", "股东研究", "..."]
  }
}
```

**使用示例：**

```bash
# 查询贵州茅台的详细信息（默认参数）
python scripts/main.py info 600519

# 查询平安银行，指定日K20天、周K10周、月K6个月
python scripts/main.py info 000001 --days 20 --weeks 10 --months 6

# 使用短参数名
python scripts/main.py info 000001 -d 20 -w 10 -m 6
```

---

### 2. 查询公司F10资料 (`company`)

获取指定股票的公司信息内容，支持选择特定信息块，结果自动转换为Markdown格式。

**命令格式：**

```bash
python scripts/main.py company <股票代码> [--blocks <块名1> <块名2> ...]
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| 股票代码 | string | 是 | - | 股票代码，如 600519 |
| --blocks, -b | string[] | 否 | 全部 | 要获取的信息块名称，可指定多个，如 "公司概况" "财务分析" |

**常见的可用信息块：**

- 最新提示
- 公司概况
- 财务分析
- 股本结构
- 股东研究
- 机构持股
- 分红融资
- 高管治理
- 资金动向
- 资本运作
- 热点题材
- 公司公告
- 公司报道
- 经营分析
- 行业分析
- 研报评级

> **注意**：每只股票具体有哪些信息块，需要调用 `info` 命令查询，其返回结果的 `company_info.structure` 字段中包含了该股票的所有可用信息块列表。也可以直接使用 `blocks` 命令来获取指定股票的所有信息块列表。

**返回格式：**

```json
{
  "公司概况": "## 【1.基本资料】\n| 公司名称 | 贵州茅台酒股份有限公司 |\n| 英文全称 | Kweichow Moutai Co., Ltd. |\n| 证券简称 | 贵州茅台 |\n| 证券代码 | 600519 |\n...",
  "财务分析": "## 【1.财务概述】\n..."
}
```

**使用示例：**

```bash
# 获取贵州茅台的全部公司信息
python scripts/main.py company 600519

# 只获取公司概况和财务分析
python scripts/main.py company 600519 --blocks "公司概况" "财务分析"

# 使用短参数名
python scripts/main.py company 600519 -b "公司概况" "财务分析"
```

---

### 3. 股票信号筛选 (`screen`)

根据技术指标信号筛选股票，支持金叉、死叉、超买、超卖等信号类型。

**命令格式：**

```bash
python scripts/main.py screen <股票代码列表> --signal <信号类型> [--ktype <K线类型>] [--startday <开始日期>] [--endday <结束日期>]
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| 股票代码列表 | string | 是 | - | 多个股票代码，用逗号、空格或分号分隔，如 "600519,000001,000858" |
| --signal, -s | string | 否 | - | 筛选信号类型，可选值：golden_cross, death_cross, overbought, oversold |
| --ktype, -k | string | 否 | day | K线类型，可选值：1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year |
| --startday, -t | string | 否 | - | 开始日期，格式：YYYYMMDD，如 "20260110" |
| --endday, -e | string | 否 | 今日 | 结束日期，格式：YYYYMMDD，如 "20260120" |

**信号类型说明：**

| 信号值 | 中文说明 | 含义 |
|--------|----------|------|
| golden_cross | 金叉 | MACD的DIF上穿DEA，或KDJ的K上穿D，买入信号 |
| death_cross | 死叉 | MACD的DIF下穿DEA，或KDJ的K下穿D，卖出信号 |
| overbought | 超买 | KDJ的J > 100 或 RSI > 80，可能回调 |
| oversold | 超卖 | KDJ的J < 0 或 RSI < 20，可能反弹 |

**返回格式：**

```json
{
  "matched": 2,
  "results": [
    {
        "code": "000001",
        "name": "平安银行",
        "last": {
            "Time": "2026-07-08T15:00:00+08:00",
            "Open": 10.44000000000007,
            "High": 10.63000000000007,
            "Low": 10.340000000000071,
            "Close": 10.60000000000007,
            "Volume": 950760,
            "Amount": 10026245.76
        },
        "ma": {
            "10": [
            10.32400000000024
            ],
            "120": [
            10.96050000000003
            ],
            "20": [
            10.613500000000148
            ],
            "5": [
            10.42800000000016
            ],
            "60": [
            10.905500000000215
            ]
        },
        "macd": {
            "DIF": [
            -0.14591639014970958
            ],
            "DEA": [
            -0.16468477843975632
            ],
            "Hist": [
            0.018768388290046734
            ],
            "Fast": 12,
            "Slow": 26,
            "Signal": 9
        },
        "kdj": {
            "K": [
            79.11438037288036
            ],
            "D": [
            60.64532390947552
            ],
            "J": [
            116.05249329969004
            ],
            "N": 5,
            "M1": 3,
            "M2": 3
        },
        "boll": {
            "Upper": [
            11.364959247070992
            ],
            "Middle": [
            10.613500000000148
            ],
            "Lower": [
            9.862040752929303
            ],
            "N": 20,
            "K": 2
        },
        "rsi": {
            "12": [
            50.91585209537262
            ],
            "24": [
            47.06768677521982
            ],
            "6": [
            63.399994680190424
            ]
        },
        "signals": [
            {
            "Code": "000001",
            "Date": "2026-07-08T15:00:00+08:00",
            "Type": "金叉",
            "Indicator": "MACD",
            "Details": "DIF(-0.15) DEA(-0.16)",
            "Strength": 0.018768388290046734
            },
            {
            "Code": "000001",
            "Date": "2026-07-08T15:00:00+08:00",
            "Type": "超买",
            "Indicator": "KDJ",
            "Details": "J=116.05",
            "Strength": 0.1605249329969004
            }
        ],
        "cycles": null
    },
    {
      "code": "000001",
      "name": "平安银行",
      "date": "2026-07-08",
      "price": 12.58,
      "signals": ["golden_cross"],
      "indicators": {...}
    }
  ]
}
```

**使用示例：**

```bash
# 筛选出现金叉信号的股票（日K）
python scripts/main.py screen "600519,000001,000858" --signal golden_cross

# 筛选超卖股票（周K）
python scripts/main.py screen "600519,000001" --ktype week

# 指定日期范围筛选
python scripts/main.py screen "600519,000001" --signal death_cross --startday 20260101 --endday 20260708

# 使用短参数名
python scripts/main.py screen "600519,000001" -s golden_cross -k day -t 20260101 -e 20260708
```

---

### 4. 列出支持的筛选信号 (`signals`)

获取所有可用的股票筛选信号列表。

**命令格式：**

```bash
python scripts/main.py signals
```

**参数说明：**

无参数。

**返回格式：**

```json
["golden_cross", "death_cross", "overbought", "oversold"]
```

**使用示例：**

```bash
python scripts/main.py signals
```

---

## 错误处理

当发生错误时，返回的JSON中会包含 `error` 或 `errors` 字段：

```json
{
  "code": "600519",
  "errors": ["Quote API error: connection refused"],
  "basic_info": {...},
  ...
}
```

或：

```json
{
  "error": "Invalid stock code"
}
```

## 示例工作流

### 工作流1：个股深度分析

```bash
# 1. 获取股票详细信息
python scripts/main.py info 600519

# 2. 获取公司概况和财务分析
python scripts/main.py company 600519 --blocks "公司概况" "财务分析"
```

### 工作流2：股票筛选

```bash
# 1. 先查看支持的信号
python scripts/main.py signals

# 2. 筛选金叉股票
python scripts/main.py screen "600519,000001,000858,601318" --signal golden_cross

# 3. 对筛选出的股票进行详细分析
python scripts/main.py info 600519
```

### 工作流3：技术指标分析

```bash
# 获取多周期技术指标
python scripts/main.py info 600519 --days 20 --weeks 10 --months 6
```

## 限制说明

- 仅支持查询中国A股市场（上海、深圳、北京）
- 数据来源于通达信官方行情服务器，可能存在延迟
- 仅供学习研究使用，不建议用于实盘交易
- 需要本地TongStock服务运行
