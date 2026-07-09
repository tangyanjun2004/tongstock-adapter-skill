# tongstock-adapter-skill

OpenClaw 技能项目，封装了 TongStock API，提供按照指标筛选股票和单个股票数据查询功能。TongStock 是一个 Go 语言实现的 TDX（通达信）市场数据客户端，其项目地址在https://github.com/tangyanjun2004/tongstock，该项目对原作者的项目进行一些改进，从而更好地支持本SKill.

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

该项目与 TongStock HTTP API 进行交互。服务地址可通过环境变量 `TONGSTOCK_BASE_URL` 配置，默认值为 `http://localhost:8080`。关键 API 端点包括：
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
export TONGSTOCK_BASE_URL="http://localhost:8080"

# Windows (PowerShell)
$env:TONGSTOCK_BASE_URL="http://localhost:8080"

# Windows (CMD)
set TONGSTOCK_BASE_URL=http://localhost:8080
```

如果未设置环境变量，默认值为 `http://localhost:8080`。

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

## 使用指南

### 安装方式

#### 方式一：本地构建安装

1. 运行构建脚本生成 release 包：
   ```bash
   python build.py
   ```
   Windows 用户也可直接运行 `build.bat`，Linux/macOS 用户可运行 `build.sh`

2. 在 `release/` 目录下找到生成的 zip 压缩包

3. 将压缩包解压到 OpenClaw 的 skills 目录下

#### 方式二：使用 Release 包

直接从项目 Release 页面下载预打包的技能包，解压后放置到 OpenClaw 的 skills 目录即可。

### 技能使用

安装完成后，在 OpenClaw 中即可使用以下功能：
- 股票信息查询：输入股票代码获取详细指标
- 股票F10信息：输入股票代码和块名称获取公司信息
- 股票筛选：根据技术指标条件筛选股票

## 构建 Release 包

项目提供了构建脚本用于打包发布。生成的压缩包位于 `release/` 目录下。

### 使用方式

```bash
# 使用默认时间戳作为版本号
python build.py

# 指定版本号
python build.py --version v1.0.0
```

Windows 用户也可以直接运行批处理脚本：

```cmd
build.bat
```

Linux/macOS 用户可以运行 Shell 脚本：

```bash
chmod +x build.sh
./build.sh
```

构建脚本会自动将 `SKILL.md` 和 `scripts/src` 目录下的所有文件打包成符合技能标准 zip 压缩包。
