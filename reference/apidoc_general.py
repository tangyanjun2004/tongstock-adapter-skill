#!/usr/bin/env python3
"""
API Doc Script for TongStock

This script calls all TongStock API endpoints with various parameter combinations
and saves their input/output data to reference/APIDoc directory for documentation purposes.

Test stock code: 600519 (贵州茅台)
"""

import requests
import json
import os
from datetime import datetime
import pytest

BASE_URL = "http://localhost:8991"
TEST_STOCK_CODE = "600519"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "APIDoc"))

def ensure_dir(directory):
    """Ensure the output directory exists"""
    os.makedirs(directory, exist_ok=True)

def save_response(endpoint: str, response_data: dict, params: dict = None):
    """Save API response to JSON file"""
    # Create filename from endpoint
    filename = endpoint.strip("/").replace("/", "_")
    if params:
        param_str = "_".join([f"{k}={v}" for k, v in sorted(params.items())])
        filename = f"{filename}_{param_str}"
    filename = f"{filename}.json"
    file_path = os.path.join(OUTPUT_DIR, filename)

    data_to_save = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "params": params or {},
        "response": response_data
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)

    print(f"Saved: {filename}")

def _call_api_endpoint(endpoint: str, params: dict = None):
    """Call a single API endpoint and save response"""
    url = f"{BASE_URL}{endpoint}"

    try:
        print(f"Testing: {endpoint}")
        if params:
            print(f"Params: {params}")

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        save_response(endpoint, data, params)

    except Exception as e:
        print(f"Error: {e}")
        error_data = {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        save_response(endpoint, error_data, params)

class TestTongStockAPI:
    """Test all TongStock API endpoints with various parameter combinations"""

    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        ensure_dir(OUTPUT_DIR)

    def test_health_check(self):
        """Test health check endpoint"""
        _call_api_endpoint("/health")

    def test_get_quote(self):
        """Test real-time quote endpoint"""
        _call_api_endpoint("/api/quote", {"code": TEST_STOCK_CODE})

    @pytest.mark.parametrize("exchange, category", [
        ("sz", "stock"),
        ("sz", "etf"),
        ("sz", "fund"),
        ("sh", "stock"),
        ("sh", "etf"),
        ("bj", "stock")
    ])
    def test_get_codes_list(self, exchange, category):
        """Test stock codes list endpoint with different exchanges and categories"""
        _call_api_endpoint("/api/codes/list", {"exchange": exchange, "category": category})

    @pytest.mark.parametrize("exchange", ["sz", "sh", "bj"])
    def test_get_codes_stats(self, exchange):
        """Test stock codes stats endpoint with different exchanges"""
        _call_api_endpoint("/api/codes/stats", {"exchange": exchange})

    @pytest.mark.parametrize("ktype, start, count", [
        ("day", 0, 0),
        ("day", 10, 20),
        ("week", 0, 0),
        ("week", 5, 10),
        ("month", 0, 0),
        ("1m", 0, 0),
        ("1m", 0, 30)
    ])
    def test_get_kline(self, ktype, start, count):
        """Test K-line data endpoint with different timeframes and parameters"""
        params = {"code": TEST_STOCK_CODE, "type": ktype}
        if start > 0:
            params["start"] = str(start)
        if count > 0:
            params["count"] = str(count)
        _call_api_endpoint("/api/kline", params)

    def test_get_finance(self):
        """Test financial data endpoint"""
        _call_api_endpoint("/api/finance", {"code": TEST_STOCK_CODE})

    def test_get_xdxr(self):
        """Test ex-rights/dividend data endpoint"""
        _call_api_endpoint("/api/xdxr", {"code": TEST_STOCK_CODE})

    def test_get_company(self):
        """Test company information (F10) endpoint"""
        _call_api_endpoint("/api/company", {"code": TEST_STOCK_CODE})

    @pytest.mark.parametrize("block", [
        "最新提示",
        "公司概况",
        "财务分析",
        "股本结构",
        "股东研究",
        "机构持股",
        "分红融资",
        "高管治理",
        "资金动向",
        "资本运作",
        "热点题材",
        "公司公告",
        "公司报道",
        "经营分析",
        "行业分析",
        "研报评级"
    ])
    def test_get_company_content(self, block):
        """Test company information content endpoint with different filenames"""
        _call_api_endpoint("/api/company/content", {"code": TEST_STOCK_CODE, "block": block})

    @pytest.mark.parametrize("ktype, days", [
        ("day", 5),
        ("week", 5),
        ("month", 3)
    ])
    def test_get_indicator(self, ktype, days):
        """Test technical indicators endpoint with different timeframes and days"""
        _call_api_endpoint("/api/indicator-filter", {"code": TEST_STOCK_CODE, "type": ktype, "days": str(days)})

    @pytest.mark.parametrize("signal, ktype", [
        ("golden_cross", "day"),
        ("golden_cross", "week"),
        ("death_cross", "day"),
        ("death_cross", "week"),
        ("overbought", "day"),
        ("oversold", "day")
    ])
    def test_screen_stocks(self, signal, ktype):
        """Test stock screening endpoint with different signals and timeframes"""
        _call_api_endpoint("/api/screen", {"codes": TEST_STOCK_CODE, "type": ktype, "signal": signal})

    def test_get_block_files(self):
        """Test block files list endpoint"""
        _call_api_endpoint("/api/block/files")

    @pytest.mark.parametrize("block_file, block_type, sort", [
        ("block_zs.dat", 0, False),
        ("block_zs.dat", 1, False),
        ("block_zs.dat", 0, True),
        ("block_fg.dat", 0, False),
        ("block_gn.dat", 0, False),
        ("block.dat", 0, False)
    ])
    def test_get_block_list(self, block_file, block_type, sort):
        """Test block list endpoint with different block files and parameters"""
        params = {"file": block_file}
        if block_type > 0:
            params["type"] = str(block_type)
        if sort:
            params["sort"] = "true"
        _call_api_endpoint("/api/block/list", params)

    @pytest.mark.parametrize("name, block_file", [
        ("沪深300", "block_zs.dat"),
        ("创业板指", "block_zs.dat"),
        ("云计算", "block_gn.dat"),
        ("金融", "block_fg.dat")
    ])
    def test_get_block_show_by_name(self, name, block_file):
        """Test block show endpoint by block name"""
        _call_api_endpoint("/api/block/show", {"name": name, "file": block_file})

    def test_get_block_show_by_code(self):
        """Test block show endpoint by stock code"""
        _call_api_endpoint("/api/block/show", {"code": TEST_STOCK_CODE})

    @pytest.mark.parametrize("date, history", [
        ("", False),
        ("20240101", False),
        ("20240101", True)
    ])
    def test_get_minute_data(self, date, history):
        """Test minute data endpoint with different parameters"""
        params = {"code": TEST_STOCK_CODE}
        if date:
            params["date"] = date
        if history:
            params["history"] = "true"
        _call_api_endpoint("/api/minute", params)

    @pytest.mark.parametrize("start, count, date, history", [
        (0, 0, "", False),
        (10, 20, "", False),
        (0, 0, "20240101", True)
    ])
    def test_get_trade_data(self, start, count, date, history):
        """Test trade data endpoint with different parameters"""
        params = {"code": TEST_STOCK_CODE}
        if start > 0:
            params["start"] = str(start)
        if count > 0:
            params["count"] = str(count)
        if date:
            params["date"] = date
        if history:
            params["history"] = "true"
        _call_api_endpoint("/api/trade", params)

    def test_get_auction_data(self):
        """Test auction data endpoint"""
        _call_api_endpoint("/api/auction", {"code": TEST_STOCK_CODE})

    @pytest.mark.parametrize("exchange", ["sz", "sh", "bj"])
    def test_get_count(self, exchange):
        """Test security count endpoint with different exchanges"""
        _call_api_endpoint("/api/count", {"exchange": exchange})

    @pytest.mark.parametrize("code, ktype", [
        ("999999", "day"),
        ("999999", "week"),
        ("399001", "day"),
        ("399001", "week"),
        ("885001", "day")
    ])
    def test_get_index_data(self, code, ktype):
        """Test index data endpoint with different indices and timeframes"""
        _call_api_endpoint("/api/index", {"code": code, "type": ktype})

def main():
    """Main function for running all tests manually"""
    print("=" * 50)
    print("TongStock API Documentation Generator")
    print("=" * 50)

    ensure_dir(OUTPUT_DIR)

    print("\nTesting API endpoints with various parameter combinations...")

    # Run all tests
    test_runner = pytest.main([__file__, "-v"])

    print("\n" + "=" * 50)
    if test_runner == 0:
        print("API documentation generation complete!")
    else:
        print(f"API documentation generation completed with {test_runner} errors!")

    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print(f"Total files: {len(os.listdir(OUTPUT_DIR))}")

if __name__ == "__main__":
    main()