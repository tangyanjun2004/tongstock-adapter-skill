#!/usr/bin/env python3
"""
Stock Screening Module

This module provides stock screening capabilities using TongStock API.
"""

from tongstock_api import TongStockAPI
from typing import List, Dict, Optional, Union
import re

class StockScreener:
    """Class to screen stocks based on technical indicators and signals"""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize with TongStock service base URL

        Args:
            base_url: Base URL of the TongStock HTTP service. If not provided,
                     will read from TONGSTOCK_BASE_URL environment variable,
                     or default to http://localhost:8991
        """
        self.api = TongStockAPI(base_url=base_url)

    def screen_by_signal(self, codes: Union[str, List[str]], ktype: str, signal: str, startday: str, endday: str) -> Dict:
        """Screen stocks for specific signals

        Args:
            codes: Stock codes to screen, can be a string with separators (comma, space, semicolon) or a list of strings
            ktype: K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year)
            signal: Signal type to screen for (golden_cross, death_cross, overbought, oversold)
            startday: Start date in format YYYYMMDD (optional, e.g., "20260110")
            endday: End date in format YYYYMMDD (optional, e.g., "20260120")

        Returns:
            Screening results with passing stocks
        """
        # 处理输入的股票代码，支持字符串和列表格式
        if isinstance(codes, str):
            # 按常见分隔符（逗号、空格、分号）拆分字符串
            codes = [code.strip() for code in re.split(r'[,;\s]+', codes) if code.strip()]

        if not codes:
            return {"matched": 0, "results": []}

        # 去除可能存在的重复代码
        unique_codes = list(set(codes))

        result = self.api.screen_stocks(unique_codes, ktype, signal, startday, endday)
        return self._parse_screening_result(result)

    def screen_by_criteria(self, codes: List[str], criteria: Dict, ktype: str = "day") -> List[Dict]:
        """Screen stocks by custom criteria"""
        passing_stocks = []

        for code in codes:
            try:
                if self._meets_criteria(code, criteria, ktype):
                    passing_stocks.append(code)
            except Exception as e:
                print(f"Error checking {code}: {e}")

        return passing_stocks

    def _meets_criteria(self, code: str, criteria: Dict, ktype: str) -> bool:
        """Check if a stock meets specific criteria"""
        indicator = self.api.get_indicator(code, ktype, days=1)
        if "error" in indicator:
            return False

        quote = self.api.get_quote(code)
        if "error" in quote:
            return False

        # Check each criteria
        for key, value in criteria.items():
            if key == "price_greater_than":
                if quote.get("Price", 0) <= value:
                    return False
            elif key == "price_less_than":
                if quote.get("Price", float("inf")) >= value:
                    return False
            elif key == "rsi_greater_than":
                if indicator.get("rsi", {}).get("rsi6", 0) <= value:
                    return False
            elif key == "rsi_less_than":
                if indicator.get("rsi", {}).get("rsi6", 100) >= value:
                    return False
            elif key == "macd_golden_cross":
                if indicator.get("macd", {}).get("signal") != "golden_cross":
                    return False
            elif key == "kdj_oversold":
                if indicator.get("kdj", {}).get("signal") != "oversold":
                    return False
            elif key == "kdj_overbought":
                if indicator.get("kdj", {}).get("signal") != "overbought":
                    return False
            elif key == "ma_bullish":
                if indicator.get("ma", {}).get("trend") != "bullish":
                    return False

        return True

    def _parse_screening_result(self, result: Dict) -> Dict:
        """Parse API screening result"""
        if "error" in result:
            return {"matched": 0, "results": []}

        # 解析 API 实际返回的格式：{'matched': 0, 'results': None, 'total': 1}
        return {
            "matched": result.get("matched", 0),
            "results": result.get("results", []) or []
        }

    def get_supported_signals(self) -> List[str]:
        """Get list of supported screening signals"""
        return ["golden_cross", "death_cross", "overbought", "oversold"]