#!/usr/bin/env python3
"""
OpenClaw Stock Analysis Skill for TongStock

Main entry point for the OpenClaw skill.
"""

import argparse
import json
import sys

from stock_info import StockInfo
from stock_screener import StockScreener
from typing import Dict, Optional, List, Union

def get_stock_info(code: str, days: int, weeks: int, months: int):
    """Get detailed stock information"""
    stock_info = StockInfo()
    result = stock_info.get_detailed_info(code, days, weeks, months)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def get_company_content(code: str, blocks: Optional[list[str]] = None):
    """Get company information content"""
    stock_info = StockInfo()
    result = stock_info.get_company_content(code, blocks)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def screen_stocks(codes: str, signal: str, ktype: str = "day", startday: str = "", endday: str = ""):
    """Screen stocks for specific signal"""
    screener = StockScreener()
    result = screener.screen_by_signal(codes, ktype, signal, startday=startday, endday=endday)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Stock Analysis Skill for TongStock"
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Stock info command
    info_parser = subparsers.add_parser("info", help="Get detailed stock information")
    info_parser.add_argument("code", help="Stock code to query")
    info_parser.add_argument(
        "--days", "-d",
        type=int,
        default=10,
        help="Number of days of daily technical indicators (default: 10)"
    )
    info_parser.add_argument(
        "--weeks", "-w",
        type=int,
        default=5,
        help="Number of weeks of weekly technical indicators (default: 5)"
    )
    info_parser.add_argument(
        "--months", "-m",
        type=int,
        default=3,
        help="Number of months of monthly technical indicators (default: 3)"
    )

    # Company info command
    company_parser = subparsers.add_parser("company", help="Get company information content")
    company_parser.add_argument("code", help="Stock code to query")
    company_parser.add_argument(
        "--blocks", "-b",
        nargs="*",
        help="Company blocks to retrieve (e.g., '公司概况' '财务分析'; default: all blocks)"
    )

    # Stock screening command
    screen_parser = subparsers.add_parser("screen", help="Screen stocks by signal")
    screen_parser.add_argument("codes", help="Comma-separated stock codes")
    screen_parser.add_argument(
        "--signal", "-s",
        choices=["golden_cross", "death_cross", "overbought", "oversold"],
        help="Screening signal type"
    )
    screen_parser.add_argument(
        "--ktype", "-k",
        default="day",
        choices=["1m", "5m", "15m", "30m", "60m", "day", "week", "month", "quarter", "year"],
        help="K-line type (1m, 5m, 15m, 30m, 60m, day, week, month, quarter, year) (default: day)"
    )
    screen_parser.add_argument(
        "--startday", "-t",
        type=str,
        default="",
        help="Start date in YYYYMMDD format (optional, e.g., 20260110)"
    )
    screen_parser.add_argument(
        "--endday", "-e",
        type=str,
        default="",
        help="End date in YYYYMMDD format (optional, e.g., 20260120; default: today)"
    )

    # List supported signals command
    subparsers.add_parser("signals", help="List supported screening signals")

    # List supported company blocks command
    blocks_parser = subparsers.add_parser("blocks", help="List company information blocks for a stock")
    blocks_parser.add_argument("code", help="Stock code to get blocks for")

    args = parser.parse_args()

    if args.command == "info":
        get_stock_info(args.code, args.days, args.weeks, args.months)

    elif args.command == "company":
        get_company_content(args.code, args.blocks)

    elif args.command == "screen":
        # 直接传递原始字符串，利用 screen_by_signal 的自动解析功能
        screen_stocks(args.codes, args.signal, args.ktype, args.startday, args.endday)

    elif args.command == "signals":
        screener = StockScreener()
        print(json.dumps(screener.get_supported_signals(), ensure_ascii=False, indent=2))

    elif args.command == "blocks":
        # Get company blocks for the specific stock
        stock_info = StockInfo()
        result = stock_info.get_detailed_info(args.code)
        if "error" in result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result["company_info"]["structure"], ensure_ascii=False, indent=2))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()