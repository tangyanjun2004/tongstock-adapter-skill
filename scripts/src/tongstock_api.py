#!/usr/bin/env python3
"""
TongStock API Wrapper

This module provides Python wrapper functions for all TongStock HTTP API endpoints.
"""

import requests
import json
import os
from typing import Optional, List, Dict, Any

class TongStockAPI:
    """TongStock API wrapper class"""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize the API wrapper

        Args:
            base_url: Base URL of the TongStock HTTP service. If not provided,
                     will read from TONGSTOCK_BASE_URL environment variable,
                     or default to http://localhost:8991
        """
        if base_url is None:
            base_url = os.environ.get("TONGSTOCK_BASE_URL", "http://localhost:8991")
        self.base_url = base_url.rstrip("/")

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """Internal helper method to make API requests"""
        url = f"{self.base_url}{endpoint}"
        params = params or {}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            # Decode response with UTF-8, replacing unrecognizable characters
            try:
                # Decode with UTF-8, replacing unrecognized characters with �
                decoded_content = response.content.decode('utf-8', errors='replace')
                # Parse JSON
                import json
                return json.loads(decoded_content)
            except Exception as e:
                print(f"Error decoding or parsing response: {e}")
                return {"error": str(e)}

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def health_check(self) -> Dict:
        """Health check endpoint"""
        return self._make_request("/health")

    def get_quote(self, code: str) -> Dict:
        """Get real-time quote

        Args:
            code: Stock code (e.g., "600519")

        Returns:
            Real-time quote data
        """
        return self._make_request("/api/quote", {"code": code})

    def get_codes_list(self, exchange: str = "sz", category: str = "stock") -> Dict:
        """Get stock codes list

        Args:
            exchange: Exchange code (sz, sh, bj)
            category: Stock category (stock, etf, fund, index, bond, gem)

        Returns:
            List of stock codes
        """
        return self._make_request("/api/codes/list", {
            "exchange": exchange,
            "category": category
        })

    def get_codes_stats(self, exchange: str = "sz") -> Dict:
        """Get stock codes stats

        Args:
            exchange: Exchange code (sz, sh, bj)

        Returns:
            Statistics about stock codes
        """
        return self._make_request("/api/codes/stats", {"exchange": exchange})

    def get_kline(self, code: str, ktype: str = "day", start: int = 0, count: int = 0) -> Dict:
        """Get K-line data

        Args:
            code: Stock code (e.g., "600519")
            ktype: K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year)
            start: Start index (optional)
            count: Number of records to return (optional)

        Returns:
            K-line data
        """
        params = {
            "code": code,
            "type": ktype
        }

        if start > 0:
            params["start"] = str(start)

        if count > 0:
            params["count"] = str(count)

        data = self._make_request("/api/kline", params)

        # If API doesn't honor start/count, apply them ourselves
        if start > 0 or count > 0:
            if isinstance(data, list):
                if start > 0 and start < len(data):
                    data = data[start:]
                if count > 0 and len(data) > count:
                    data = data[:count]

        return data

    def get_finance(self, code: str) -> Dict:
        """Get financial data

        Args:
            code: Stock code (e.g., "600519")

        Returns:
            Financial indicators data
        """
        return self._make_request("/api/finance", {"code": code})

    def get_xdxr(self, code: str) -> Dict:
        """Get ex-rights/dividend data

        Args:
            code: Stock code (e.g., "600519")

        Returns:
            Ex-rights and dividend history
        """
        return self._make_request("/api/xdxr", {"code": code})

    def get_company(self, code: str) -> Dict:
        """Get company information (F10)

        Args:
            code: Stock code (e.g., "600519")

        Returns:
            Company information structure
        """
        return self._make_request("/api/company", {"code": code})

    def get_company_content(self, code: str, block: str) -> Dict:
        """Get company information content

        Args:
            code: Stock code (e.g., "600519")
            block: Block name(e.g., "最新提示", "公司概况", "财务分析", "股本结构", "股东研究", "机构持股","分红融资","高管治理","资金动向","资本运作"."热点题材","公司公告","公司报道","经营分析","行业分析","研报评级")

        Returns:
            Detailed company information
        """
        return self._make_request("/api/company/content", {
            "code": code,
            "block": block
        })

    def get_indicator(self, code: str, ktype: str = "day", days: int = 1) -> Dict:
        """Get technical indicators

        Args:
            code: Stock code (e.g., "600519")
            ktype: K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year)
            days: Number of days of historical data to include

        Returns:
            Technical indicators data
        """
        return self._make_request("/api/indicator-filter", {
            "code": code,
            "type": ktype,
            "days": str(days)
        })

    def screen_stocks(self, codes: List[str], ktype: str, signal: str, startday: str, endday: str) -> Dict:
        """Screen stocks for signals

        Args:
            codes: List of stock codes to screen
            ktype: K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year)
            signal: Signal type to screen for (golden_cross, death_cross, overbought, oversold)
            startday: Start date in format YYYYMMDD (optional, e.g., "20260110")
            endday: End date in format YYYYMMDD (optional, e.g., "20260120")

        Returns:
            Screening results with passing stocks
        """
        codes_str = ",".join(codes)
        params = {
            "codes": codes_str,
            "type": ktype,
            "signal": signal,
            "startday":startday,
            "endday":endday
        }

        return self._make_request("/api/screen", params)

    def get_block_files(self) -> Dict:
        """Get block files list"""
        return self._make_request("/api/block/files")

    def get_block_list(self, block_file: str = "block_zs.dat", block_type: int = 0, sort: bool = False) -> Dict:
        """Get block list

        Args:
            block_file: Block file name (block_zs.dat, block_fg.dat, block_gn.dat, block.dat)
            block_type: Block type filter (optional)
            sort: Whether to sort by number of stocks (optional, defaults to False)

        Returns:
            List of blocks
        """
        params = {"file": block_file}
        if block_type > 0:
            params["type"] = str(block_type)
        if sort:
            params["sort"] = str(sort).lower()
        return self._make_request("/api/block/list", params)

    def get_block_show(self, name: Optional[str] = None, code: Optional[str] = None, block_file: str = "block_zs.dat") -> Dict:
        """Get block details or stock's block information

        Args:
            name: Block name to query
            code: Stock code to query
            block_file: Block file to search in (block_zs.dat, block_fg.dat, block_gn.dat, block.dat)

        Returns:
            Block details and member stocks
        """
        params = {}
        if name:
            params["name"] = name
            params["file"] = block_file
        elif code:
            params["code"] = code
        else:
            return {"error": "Either name or code must be provided"}

        return self._make_request("/api/block/show", params)

    def get_minute_data(self, code: str, date: str = "", history: bool = False) -> Dict:
        """Get minute data

        Args:
            code: Stock code (e.g., "600519")
            date: Date for historical data (YYYYMMDD format, optional)
            history: Whether to get historical data (optional, defaults to False)

        Returns:
            Minute-level transaction data
        """
        params = {"code": code}
        if date:
            params["date"] = date
        if history:
            params["history"] = str(history).lower()
        return self._make_request("/api/minute", params)

    def get_trade_data(self, code: str, start: int = 0, count: int = 0, date: str = "", history: bool = False) -> Dict:
        """Get trade data

        Args:
            code: Stock code (e.g., "600519")
            start: Start index (optional)
            count: Number of records to return (optional)
            date: Date for historical data (YYYYMMDD format, optional)
            history: Whether to get historical data (optional, defaults to False)

        Returns:
            Detailed trade transaction data
        """
        params = {"code": code}
        if start > 0:
            params["start"] = str(start)
        if count > 0:
            params["count"] = str(count)
        if date:
            params["date"] = date
        if history:
            params["history"] = str(history).lower()
        return self._make_request("/api/trade", params)

    def get_auction_data(self, code: str) -> Dict:
        """Get auction data

        Args:
            code: Stock code (e.g., "600519")

        Returns:
            Auction transaction data
        """
        return self._make_request("/api/auction", {"code": code})

    def get_count(self, exchange: str = "sz") -> Dict:
        """Get security count

        Args:
            exchange: Exchange code (sz, sh, bj)

        Returns:
            Number of securities on the exchange
        """
        return self._make_request("/api/count", {"exchange": exchange})

    def get_index_data(self, code: str = "999999", ktype: str = "day") -> Dict:
        """Get index data

        Args:
            code: Index code (e.g., "999999" for SSE Composite Index)
            ktype: K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year)

        Returns:
            Index data
        """
        return self._make_request("/api/index", {
            "code": code,
            "type": ktype
        })