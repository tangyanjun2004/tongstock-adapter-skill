# a-stock-tdx-adapter

OpenClaw 技能项目，封装了 TongStock API，提供按照指标筛选股票和单个股票数据查询功能。TongStock 是一个 Go 语言实现的 TDX（通达信）市场数据客户端，部署在本地 http://localhost:8991。

## 核心功能

### 股票信息查询
- 接受股票代码（如 600519）作为输入
- 调用多个 TongStock API 收集综合数据
- 返回包含关键炒股指标的结构化 JSON

### 股票F10信息
- 接受股票代码（如 600519）和块名称作为输入
- 调用 TongStock API 的公司块接口
- 返回已经转换成 markdown 格式的信息

### 股票筛选
- 接受多个股票代码和筛选标准
- 返回符合特定条件的股票（如金叉、超卖）
- 支持批量处理和并发 API 调用

## API 集成

该项目与 TongStock HTTP API 进行交互。服务地址可通过环境变量 `TONGSTOCK_BASE_URL` 配置，默认值为 `http://localhost:8991`。关键 API 端点包括：
- `/api/quote` - 实时报价
- `/api/finance` - 财务数据
- `/api/kline` - K 线数据
- `/api/indicator` - 技术指标（MACD/KDJ/MA/BOLL/RSI）
- `/api/screen` - 批量信号筛选
- `/api/xdxr` - 除权除息数据
- `/api/company` - 公司信息（F10）

API 格式示例可在 `reference/APIDoc/` 目录下找到，每个 JSON 文档包含：
- `timestamp` - 调用时间
- `endpoint` - 接口地址
- `params` - 传递的参数
- `response` - 得到的返回结果

## 项目结构

```
a-stock-tdx/
├── SKILL.md                 # 技能描述文件
├── scripts/
│   ├── src/                 # 源代码
│   │   ├── tongstock_api.py # TongStock API 包装器
│   │   ├── stock_info.py    # 股票信息查询
│   │   ├── stock_screener.py # 股票筛选
│   │   └── main.py          # 技能入口点
│   └── test/                # 测试文件和生成的测试结果
│       ├── test_*.py        # 单元测试
│       └── test_result/     # 测试结果目录
│           ├── test_*.md    # 生成的测试结果文件（Markdown 格式）
│           └── test_*.json  # 生成的测试结果文件（json 格式）
└── reference/
    ├── TongStock-Readme.md  # TongStock 项目描述
    ├── TongStock-SampleSKILL.md  # 使用示例
    ├── apidoc_general.py    # API json格式代码生成
    └── APIDoc/              # API 文档（输入/输出示例）
```

## 开发指南

### 环境配置

TongStock 服务地址可通过环境变量 `TONGSTOCK_BASE_URL` 配置：

```bash
# Linux/macOS
export TONGSTOCK_BASE_URL="http://localhost:8991"

# Windows (PowerShell)
$env:TONGSTOCK_BASE_URL="http://localhost:8991"

# Windows (CMD)
set TONGSTOCK_BASE_URL=http://localhost:8991
```

如果未设置环境变量，默认值为 `http://localhost:8991`。

### Python 环境

```bash
# 创建虚拟环境
cd scripts
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # 在 Windows 上：venv\Scripts\activate

# 安装依赖
pip install requests pytest

# 停用虚拟环境
deactivate
```

### 运行测试

```bash
# 运行所有测试
cd scripts
pytest

# 运行单个测试文件
pytest test/api_test.py

# 运行带有详细输出的测试
pytest -v
```

### API 文档生成

```bash
# 生成 API 文档（从 reference 目录运行）
cd reference
python apidoc_general.py
```
