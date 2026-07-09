# CLAUDE.md

## 项目概述

这是 `a-stock-tdx-adapter` - 一个 OpenClaw 技能项目，封装了 TongStock API，提供按照指标筛选股票和单个股票数据查询功能。TongStock 是一个 Go 语言实现的 TDX（通达信）市场数据客户端，部署在本地 http://localhost:8991。

## 项目结构

```
a-stock-tdx/
├── SKILL.md                 # 技能描述文件
├── scripts/
│   ├── src/                 # 源代码
│   │   ├── tongstock_api.py  # TongStock API 包装器
│   │   ├── stock_info.py    # 股票信息查询
│   │   ├── stock_screener.py # 股票筛选
│   │   └── main.py          # 技能入口点
│   └── test/                # 测试文件和生成的测试结果
│       ├── test_*.py        # 单元测试
│       └── test_result/     # 测试结果目录
│           ├── test_*.md    # 生成的测试结果文件（Markdown 格式）
│           └── test_*.json    # 生成的测试结果文件（json 格式）
└── reference/
    ├── TongStock-Readme.md  # TongStock 项目描述
    ├── TongStock-SampleSKILL.md  # TongStock 使用示例，在生成SKILL时可以参考
    ├── apidoc_general.py      # API json格式代码生成
    └── APIDoc/              # API 文档（输入/输出示例）

```

## 开发约束
## API格式的获取
- 在编写代码需要知道TongStock API的输入输出格式时，请阅读reference目录下的APIDoc下的json文档来获取不同参数下的response
- 这个目录下的每一个json的格式都是如下格式
```json
  "timestamp": "", //调用时间
  "endpoint": "",  //接口地址
  "params": {},  //传递的参数
  "response": {}  //得到的返回结果
```
### 测试文件位置
所有测试文件必须放在 `scripts/test` 目录中。这包括：
- 单元测试文件（应遵循 `test_*.py` 命名约定）
- 集成测试文件
- 任何其他测试相关文件

### 测试结果生成
特别约束：所有生成的测试结果（如 `test_text_to_markdown_v2.py` 生成的 Markdown 文件）必须保存在 `scripts/test/test_result` 目录中。这确保了：
1. 测试文件和结果保持在一个位置
2. 根目录和其他目录保持干净
3. 更容易管理和版本控制测试相关的工件
4. CI/CD 过程可以轻松定位和处理测试输出

## 常见开发命令

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

## API 集成
该项目与 TongStock HTTP API 在 http://localhost:8991 进行交互。关键 API 端点包括：
- `/api/quote` - 实时报价
- `/api/finance` - 财务数据
- `/api/kline` - K 线数据
- `/api/indicator` - 技术指标（MACD/KDJ/MA/BOLL/RSI）
- `/api/screen` - 批量信号筛选
- `/api/xdxr` - 除权除息数据
- `/api/company` - 公司信息（F10）

## 核心功能

### 股票信息查询
- 接受股票代码（如 600519）作为输入
- 调用多个 TongStock API 收集综合数据
- 返回包含关键炒股指标的结构化 JSON

### 股票F10信息
- 接受股票代码（如 600519）和块名称作为输入
- 调用TongStock API 的公司块接口
- 返回已经转成成markdow格式的信息

### 股票筛选
- 接受多个股票代码和筛选标准
- 返回符合特定条件的股票（如金叉、超卖）
- 支持批量处理和并发 API 调用


