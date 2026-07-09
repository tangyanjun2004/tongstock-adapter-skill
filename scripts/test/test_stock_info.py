#!/usr/bin/env python3
"""
Test Stock Info Module
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from stock_info import StockInfo

def test_stock_info():
    """Test getting stock info"""
    print("Testing stock information query...")

    stock_info = StockInfo()
    result = stock_info.get_detailed_info("600519")

    assert "error" not in result, f"Error: {result.get('error')}"
    assert "code" in result, "Result missing 'code' field"
    assert result["code"] == "600519", f"Expected code '600519', got '{result['code']}'"
    assert "market_data" in result, "Result missing 'market_data' field"
    assert "price" in result["market_data"], "Market data missing 'price' field"
    assert result["market_data"]["price"] > 0, f"Invalid price: {result['market_data']['price']}"
    assert "financial_info" in result, "Result missing 'financial_info' field"
    assert "net_profit" in result["financial_info"], "Financial info missing 'net_profit' field"
    assert result["financial_info"]["net_profit"] > 0, f"Invalid net profit: {result['financial_info']['net_profit']}"

    print("✅ Stock info obtained successfully")
    print(f"Stock code: {result['code']}")
    print(f"Stock name: {result['basic_info']['name']}")
    print(f"Current price: {result['market_data']['price']}")
    print(f"Net profit: {result['financial_info']['net_profit']}")
    print(f"Total shares: {result['basic_info']['total_shares']}")

def test_multiple_codes():
    """Test getting info for multiple stocks"""
    print("\nTesting multiple stock info queries...")

    stock_info = StockInfo()

    codes = ["600519", "000001"]

    for code in codes:
        print(f"\nQuerying {code}...")
        try:
            result = stock_info.get_detailed_info(code)
            assert "error" not in result, f"Error: {result.get('error')}"
            assert "code" in result, "Result missing 'code' field"
            assert result["code"] == code, f"Expected code '{code}', got '{result['code']}'"
            assert "market_data" in result and "price" in result["market_data"], "Result missing price information"
            assert result["market_data"]["price"] > 0, f"Invalid price: {result['market_data']['price']}"
            print(f"✅ Success")
        except Exception as e:
            pytest.fail(f"Error querying {code}: {e}")

if __name__ == "__main__":
    print("Stock Info Module Test")
    print("=" * 50)

    try:
        test_stock_info()
        test_multiple_codes()
        print("\n" + "=" * 50)
        print("✅ All tests passed")
    except AssertionError as e:
        print(f"\n❌ Assertion failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")