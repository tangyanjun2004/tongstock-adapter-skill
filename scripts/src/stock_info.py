#!/usr/bin/env python3
"""
Stock Information Query Module

This module provides detailed stock information by calling multiple TongStock API endpoints.
"""

from tongstock_api import TongStockAPI
from typing import Dict, Optional, List, Union
import re

class StockInfo:
    """Class to retrieve and organize detailed stock information"""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize with TongStock service base URL

        Args:
            base_url: Base URL of the TongStock HTTP service. If not provided,
                     will read from TONGSTOCK_BASE_URL environment variable,
                     or default to http://localhost:8991
        """
        self.api = TongStockAPI(base_url=base_url)

    def get_detailed_info(
        self,
        code: str,
        days: int = 10,
        weeks: int = 5,
        months: int = 3
    ) -> Dict:
        """Get comprehensive stock information

        Args:
            code: Stock code (e.g., "600519")
            days: Number of days for daily technical indicators (default: 10)
            weeks: Number of weeks for weekly technical indicators (default: 5)
            months: Number of months for monthly technical indicators (default: 3)

        Returns:
            Structured stock information including basic info, market data, financial info,
            technical indicators, dividend info, and company info structure
        """
        if not code or len(code) < 6:
            return {"error": "Invalid stock code"}

        try:
            # Call multiple API endpoints
            quote = self.api.get_quote(code)
            finance = self.api.get_finance(code)
            indicator_day = self.api.get_indicator(code, ktype="day", days=days)
            indicator_week = self.api.get_indicator(code, ktype="week", days=weeks)
            indicator_month = self.api.get_indicator(code, ktype="month", days=months)
            xdxr = self.api.get_xdxr(code)
            company = self.api.get_company(code)

            # Collect errors from all endpoints
            errors = []
            if "error" in quote:
                errors.append(f"Quote API error: {quote['error']}")
            if "error" in finance:
                errors.append(f"Finance API error: {finance['error']}")
            if "error" in indicator_day:
                errors.append(f"Day indicator API error: {indicator_day['error']}")
            if "error" in indicator_week:
                errors.append(f"Week indicator API error: {indicator_week['error']}")
            if "error" in indicator_month:
                errors.append(f"Month indicator API error: {indicator_month['error']}")
            if "error" in xdxr:
                errors.append(f"Xdxr API error: {xdxr['error']}")
            if "error" in company:
                errors.append(f"Company API error: {company['error']}")

            # Organize information into structured format
            result = {
                "code": code,
                "errors": errors,
                "basic_info": self._extract_basic_info(quote, finance),
                "market_data": self._extract_market_data(quote),
                "financial_info": self._extract_financial_info(finance),
                "technical_indicators": {
                    "day": {
                        "history": self._extract_technical_indicators(indicator_day),
                        "summary": indicator_day.get("summary", {})
                    },
                    "week": {
                        "history": self._extract_technical_indicators(indicator_week),
                        "summary": indicator_week.get("summary", {})
                    },
                    "month": {
                        "history": self._extract_technical_indicators(indicator_month),
                        "summary": indicator_month.get("summary", {})
                    }
                },
                "dividend_info": self._extract_dividend_info(xdxr),
                "company_info": {
                    "structure": self._extract_company_structure(company)
                }
            }

            return result
        except Exception as e:
            return {"error": f"Failed to get detailed info: {e}"}

    def get_company_content(
        self,
        code: str,
        blocks: Optional[List[str]] = None
    ) -> Dict:
        """Get company information content for specific blocks

        Args:
            code: Stock code (e.g., "600519")
            blocks: List of block names to retrieve.
                If None, retrieves all available blocks.

        Returns:
            Dictionary with block names as keys and their content as values
        """
        if not code or len(code) < 6:
            return {"error": "Invalid stock code"}

        try:
            # Get company structure to determine available blocks
            company = self.api.get_company(code)
            if "error" in company:
                return {"error": f"Company API error: {company['error']}"}

            # Determine which blocks to retrieve
            if blocks is None:
                # If no blocks specified, get all available blocks
                if isinstance(company, list):
                    block_names = [block_info.get("Name", "") for block_info in company if block_info.get("Name")]
                else:
                    block_names = []
            else:
                # Use specified block names directly
                block_names = blocks

            # Get content for each block
            company_content = {}
            for block_name in block_names:
                content = self.api.get_company_content(code, block_name)
                if "error" not in content:
                    # Extract actual content from API response
                    if isinstance(content, dict) and "content" in content:
                        actual_content = content["content"]
                    else:
                        # If response structure is different, use content directly
                        actual_content = content
                    company_content[block_name] = self._simplify_company_content(actual_content)

            return company_content
        except Exception as e:
            # Check if it's an API error or other type of exception
            if "http" in str(e).lower() or "server" in str(e).lower() or "client" in str(e).lower():
                return {"error": f"API error: {str(e)}"}
            return {"error": f"Failed to get company content: {e}"}

    def _simplify_company_content(self, content: Union[Dict, str]) -> str:
        """Convert company content to Markdown format

        Args:
            content: Raw content from API

        Returns:
            Markdown formatted content
        """
        # If content is a dict, convert to string first
        if isinstance(content, dict):
            content = str(content)

        # Convert all content to Markdown format
        return self._text_to_markdown(content)

    def _text_to_markdown(self, text: str) -> str:
        """Convert text content with tables and sections to Markdown

        Args:
            text: Raw text content from API

        Returns:
            Markdown formatted text
        """
        
        # -------------------------------------------------------------
        # 步骤 A & B：提取目录章节
        # -------------------------------------------------------------
        start_marker = "★本栏包括"
        marker_idx = text.find(start_marker)
        if marker_idx == -1:
            remaining_text = text
            main_sections = []
        else:
            content_from_marker = text[marker_idx:]
            end_of_dir_match = re.search(r'\r\n\r\n', content_from_marker)
            if not end_of_dir_match:
                raise ValueError("未找到目录结束的空行标志")
                
            directory_block = content_from_marker[:end_of_dir_match.start()]
            clean_directory_line = re.sub(r'[\r\n]\s*', '', directory_block)
            main_sections = re.findall(r'【(.*?)】', clean_directory_line)
            
            remaining_text = content_from_marker[end_of_dir_match.end():]
        
        lines = remaining_text.replace('\r\n', '\n').split('\n')
        
        # -------------------------------------------------------------
        # 步骤 C & D：状态机 + 智能边框表格处理
        # -------------------------------------------------------------
        markdown_output: List[str] = []
        table_buffer: List[str] = []      
        current_main_section = None
        bracket_pattern = re.compile(r'【(.*?)】')
        
        for line in lines:
            line_strip = line.strip()
            
            # 新增要求 2：遇到 〖免责条款〗 或包含该字段，立即终止后续处理并丢弃
            if "〖免责条款〗" in line_strip:
                break
            
            # 1. 过滤纯边框符号线
            if re.match(r'^[┌├└┬┼┴┐┤┘─\s]+$', line_strip) and line_strip != "":
                continue
                
            # 2. 判断是否为包含数据的“表格行”：只要行内包含竖线 '│'
            is_table_row = '│' in line
            
            if is_table_row:
                table_buffer.append(line)
                continue
            else:
                # 遇到非表格行，立即渲染外溢
                if table_buffer:
                    markdown_output.extend(self._flush_border_table_buffer(table_buffer))
                    table_buffer = []
            
            # 3. 处理空行
            if not line_strip:
                markdown_output.append("")
                continue
                
            # 4. 处理常规标题和正文
            match = bracket_pattern.search(line_strip)
            if match:
                title_text = match.group(1)
                remark_text = line_strip[match.end():].strip()
                
                if title_text in main_sections:
                    current_main_section = title_text
                    md_header = f"## 【{title_text}】"
                else:
                    md_header = f"### 【{title_text}】" if current_main_section else f"### 【{title_text}】"
                    
                if remark_text:
                    md_header += f" {remark_text}"
                markdown_output.append(md_header)
            else:
                markdown_output.append(line)
                
        # 兜底清理末尾表格（如果被免责条款提前中断，这里通常不会触发，符合预期逻辑）
        if table_buffer:
            markdown_output.extend(self._flush_border_table_buffer(table_buffer))
            
        return "\n".join(markdown_output)

    def _flush_border_table_buffer(self, table_lines: List[str]) -> List[str]:
        """
        辅助函数：将缓冲区内的制表符边框表格行，转换为标准的 Markdown 表格。
        强化版：彻底清除各种顽固空格（全角/半角），确保多列换行合并 100% 生效。
        """
        if not table_lines:
            return []
            
        raw_rows: List[List[str]] = []
        
        # 1. 清洗每一行：不仅去掉两端│，还要用正则把所有的全角空格、半角空格全部彻底 strip 干净
        for line in table_lines:
            clean_line = line.strip().strip('│')
            cols = [c.strip() for c in clean_line.split('│')]
            
            # 【核心修正点 1】：强力清洗！把所有只包含空格（含全角\u3000）的单元格彻底变为空字符串 ""
            cleaned_cols = []
            for cell in cols:
                # 清除包含全角空格、换行符、普通空格等所有空白
                cell_clean = re.sub(r'^[\s\u3000\xa0]+|[\s\u3000\xa0]+$', '', cell)
                cleaned_cols.append(cell_clean)
                
            if cleaned_cols:
                raw_rows.append(cleaned_cols)
                
        if not raw_rows:
            return []
            
        # 2. 智能核心：多列折行平铺合并
        merged_rows: List[List[str]] = []
        for row in raw_rows:
            is_continuation_line = False
            
            if merged_rows and len(row) > 1:
                # 取出中间所有列的数据
                middle_cols = row[1:-1] if len(row) > 2 else []
                
                # 【核心修正点 2】：更安全的判定条件
                # 只要中间的属性列全为空字符串，说明它绝对是上一行的残渣折行
                if all(c == "" for c in middle_cols):
                    is_continuation_line = True

            if is_continuation_line:
                # 这是一个由于上一行文本过长导致的“残留折行”
                prev_row = merged_rows[-1]
                # 将当前行每个单元格的内容，精准拼接到上一行对应列的后面
                for i in range(len(row)):
                    if i < len(prev_row):
                        if row[i]:
                            prev_row[i] += row[i]
                    else:
                        prev_row.append(row[i])
            else:
                # 这是一行有全新核心数据的独立行
                merged_rows.append(row)
                
        # 3. 统一列数并渲染为标准 Markdown 表格
        max_cols = max(len(row) for row in merged_rows) if merged_rows else 0
        markdown_table: List[str] = []
        
        for i, row in enumerate(merged_rows):
            if len(row) < max_cols:
                row.extend([""] * (max_cols - len(row)))
                
            markdown_table.append("| " + " | ".join(row) + " |")
            
            if i == 0:
                separator = "|" + "|".join(["---"] * max_cols) + "|"
                markdown_table.append(separator)
                
        return markdown_table

    def _extract_basic_info(self, quote: Dict, finance: Dict) -> Dict:
        """Extract basic stock information"""
        info = {
            "name": quote.get("Name", ""),
            "code": quote.get("Code", "")
        }

        if "error" not in finance:
            info.update({
                "total_shares": finance.get("ZongGuBen"),  # 总股本
                "float_shares": finance.get("LiuTongGuBen"),  # 流通股
                "nav_per_share": finance.get("MeiGuJingZiChan"),  # 每股净资产
                "issued_shares": finance.get("FaXingGuBen"),  # 发行股
                "listing_date": finance.get("ShangShiRiQi")  # 上市日期
            })

        return info

    def _extract_market_data(self, quote: Dict) -> Dict:
        """Extract market data (price, volume, etc.)"""
        if "error" in quote:
            return {}

        return {
            "price": quote.get("Price"),
            "change": quote.get("Price", 0) - quote.get("LastClose", 0),
            "change_pct": (quote.get("Price", 0) - quote.get("LastClose", 0)) / quote.get("LastClose", 1) * 100,
            "open": quote.get("Open"),
            "high": quote.get("High"),
            "low": quote.get("Low"),
            "last_close": quote.get("LastClose"),
            "volume": quote.get("Volume"),
            "amount": quote.get("Amount"),
            "inner_volume": quote.get("SVol"),
            "outer_volume": quote.get("BVol"),
            "bid_ask": quote.get("BidAsk", [])
        }

    def _extract_financial_info(self, finance: Dict) -> Dict:
        """Extract financial information"""
        if "error" in finance:
            return {}

        return {
            "net_profit": finance.get("JingLiRun"),  # 净利润（万元）
            "revenue": finance.get("ZhuYingShouRu"),  # 主营业务收入（万元）
            "shareholders": finance.get("GuDongRenShu"),  # 股东人数（人）
            "total_assets": finance.get("ZongZiChan"),  # 总资产（万元）
            "net_assets": finance.get("JingZiChan"),  # 净资产（万元）
            "eps": finance.get("MeiGuXiShou"),  # 每股收益（元）
            "pe_ratio": finance.get("ShiYingLv"),  # 市盈率
            "pb_ratio": finance.get("ShiBenLv"),  # 市净率
            "operating_profit": finance.get("YingYeLiRun"),  # 营业利润（万元）
            "gross_profit_margin": finance.get("MaoLiLv"),  # 毛利率
            "roe": finance.get("JunQuanROE")  # 净资产收益率
        }

    def _extract_technical_indicators(self, indicator: Dict) -> List[Dict]:
        """Extract and format technical indicators as array of daily/weekly/monthly data"""
        if "error" in indicator:
            return []

        period_data = []

        # New indicator-filter API returns data in history array
        if "history" in indicator and isinstance(indicator["history"], list):
            for item in indicator["history"]:
                point = {
                    "timestamp": item.get("timestamp", ""),
                    "kline": item.get("kline", {}),
                    "ma": item.get("ma", {}),
                    "macd": item.get("macd", {}),
                    "kdj": item.get("kdj", {}),
                    "rsi": item.get("rsi", {}),
                    "boll": item.get("boll", {}),
                    "volume": item.get("volume", {}),
                    "signals": item.get("signals", [])
                }
                period_data.append(point)
        else:
            # Fallback for old indicator API format
            period_data.append({
                "timestamp": self._get_latest_timestamp(indicator),
                "price": self._extract_price_info(indicator),
                "ma": self._extract_ma(indicator),
                "macd": self._extract_macd(indicator),
                "kdj": self._extract_kdj(indicator),
                "rsi": self._extract_rsi(indicator),
                "boll": self._extract_boll(indicator),
                "volume": self._extract_volume_info(indicator),
                "signals": self._extract_signals(indicator)
            })

        return period_data

    def _extract_dividend_info(self, xdxr: Dict) -> List[Dict]:
        """Extract dividend information (last 3 months only)"""
        if "error" in xdxr:
            return []

        # Get all dividend records and filter to last 3 months
        records = []
        if isinstance(xdxr, list):
            records = xdxr
        elif "data" in xdxr and isinstance(xdxr["data"], list):
            records = xdxr["data"]

        # In a real implementation, we would filter by date
        # For now, we just return the first few records (simulating last 3 months)
        return records[:3]

    # Fallback methods for old indicator API format (may not be used)
    def _get_latest_timestamp(self, indicator: Dict) -> str:
        if "timestamp" in indicator:
            return indicator["timestamp"]
        if "Time" in indicator:
            return indicator["Time"]
        return ""

    def _extract_price_info(self, indicator: Dict) -> Dict:
        if "price" in indicator:
            price_data = indicator["price"]
            if isinstance(price_data, dict):
                return price_data
            elif isinstance(price_data, list) and len(price_data) > 0:
                return price_data[-1]
        return {
            "current": 0,
            "change": 0,
            "change_pct": 0
        }

    def _extract_volume_info(self, indicator: Dict) -> Dict:
        volume_data = indicator.get("volume", {})
        if isinstance(volume_data, dict):
            return volume_data
        elif isinstance(volume_data, list) and len(volume_data) > 0:
            return volume_data[-1]
        return {
            "current": 0,
            "avg5": 0,
            "ratio": 0,
            "signal": "normal"
        }

    def _extract_macd(self, indicator: Dict) -> Dict:
        macd_data = indicator.get("macd", {})
        return {
            "dif": macd_data.get("dif", 0),
            "dea": macd_data.get("dea", 0),
            "hist": macd_data.get("hist", 0),
            "signal": macd_data.get("signal", "normal")
        }

    def _extract_kdj(self, indicator: Dict) -> Dict:
        kdj_data = indicator.get("kdj", {})
        return {
            "k": kdj_data.get("k", 50),
            "d": kdj_data.get("d", 50),
            "j": kdj_data.get("j", 50),
            "signal": kdj_data.get("signal", "normal")
        }

    def _extract_ma(self, indicator: Dict) -> Dict:
        ma_data = indicator.get("ma", {})
        return {
            "ma5": ma_data.get("ma5", 0),
            "ma10": ma_data.get("ma10", 0),
            "ma20": ma_data.get("ma20", 0),
            "ma60": ma_data.get("ma60", 0),
            "ma120": ma_data.get("ma120", 0),
            "trend": ma_data.get("trend", "neutral")
        }

    def _extract_boll(self, indicator: Dict) -> Dict:
        boll_data = indicator.get("boll", {})
        return {
            "upper": boll_data.get("upper", 0),
            "middle": boll_data.get("middle", 0),
            "lower": boll_data.get("lower", 0),
            "position": boll_data.get("position", 0.5),
            "signal": boll_data.get("signal", "normal")
        }

    def _extract_rsi(self, indicator: Dict) -> Dict:
        rsi_data = indicator.get("rsi", {})
        return {
            "rsi6": rsi_data.get("rsi6", 50),
            "rsi12": rsi_data.get("rsi12", 50),
            "rsi24": rsi_data.get("rsi24", 50),
            "signal": rsi_data.get("signal", "neutral")
        }

    def _extract_signals(self, indicator: Dict) -> List[str]:
        signals = []
        if "signals" in indicator:
            signals.extend(indicator["signals"])
        return signals

    def _extract_summary(self, indicator: Dict) -> Dict:
        if "summary" in indicator:
            return indicator["summary"]
        return {
            "signal": "neutral",
            "strength": 50,
            "trend": "neutral"
        }

    def _extract_company_structure(self, company: Union[List[Dict], Dict]) -> List[str]:
        """Extract company information structure as list of block names

        Args:
            company: Company information from get_company API

        Returns:
            List of block names
        """
        structure = []

        if isinstance(company, list):
            for block_info in company:
                name = block_info.get("Name")
                if name:
                    structure.append(name)
        elif isinstance(company, dict):
            # If company is a dict, check if it contains a list of blocks or is a single block
            # This is a fallback in case the API returns a different structure
            pass

        return structure
