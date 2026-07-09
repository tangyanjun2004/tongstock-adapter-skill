#!/usr/bin/env python3
"""
Test environment variable configuration for TongStock API
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from tongstock_api import TongStockAPI
from stock_info import StockInfo
from stock_screener import StockScreener

def test_tongstock_api_default_url():
    """Test that default URL is http://localhost:8991 for TongStockAPI"""
    print("Testing TongStockAPI default URL (without environment variable)...")

    # Ensure environment variable is not set
    if "TONGSTOCK_BASE_URL" in os.environ:
        del os.environ["TONGSTOCK_BASE_URL"]

    api = TongStockAPI()
    assert api.base_url == "http://localhost:8991", f"Expected 'http://localhost:8991', got '{api.base_url}'"
    print("[OK] TongStockAPI default URL test passed")

def test_tongstock_api_env_var_url():
    """Test that URL can be set via environment variable for TongStockAPI"""
    print("\nTesting TongStockAPI environment variable configuration...")

    test_url = "http://test.example.com:1234"
    os.environ["TONGSTOCK_BASE_URL"] = test_url

    api = TongStockAPI()
    assert api.base_url == test_url, f"Expected '{test_url}', got '{api.base_url}'"
    print("[OK] TongStockAPI environment variable test passed")

def test_tongstock_api_explicit_url():
    """Test that explicit URL parameter takes precedence for TongStockAPI"""
    print("\nTesting TongStockAPI explicit URL parameter...")

    # Set environment variable to something else
    os.environ["TONGSTOCK_BASE_URL"] = "http://should.be.ignored"

    explicit_url = "http://explicit.example.com:5678"
    api = TongStockAPI(base_url=explicit_url)
    assert api.base_url == explicit_url, f"Expected '{explicit_url}', got '{api.base_url}'"
    print("[OK] TongStockAPI explicit URL parameter test passed")

def test_stock_info_default_url():
    """Test that default URL works for StockInfo"""
    print("\nTesting StockInfo default URL...")

    if "TONGSTOCK_BASE_URL" in os.environ:
        del os.environ["TONGSTOCK_BASE_URL"]

    stock_info = StockInfo()
    assert stock_info.api.base_url == "http://localhost:8991", f"Expected 'http://localhost:8991', got '{stock_info.api.base_url}'"
    print("[OK] StockInfo default URL test passed")

def test_stock_info_env_var_url():
    """Test that environment variable works for StockInfo"""
    print("\nTesting StockInfo environment variable...")

    test_url = "http://stockinfo.example.com:1234"
    os.environ["TONGSTOCK_BASE_URL"] = test_url

    stock_info = StockInfo()
    assert stock_info.api.base_url == test_url, f"Expected '{test_url}', got '{stock_info.api.base_url}'"
    print("[OK] StockInfo environment variable test passed")

def test_stock_info_explicit_url():
    """Test that explicit URL parameter works for StockInfo"""
    print("\nTesting StockInfo explicit URL parameter...")

    os.environ["TONGSTOCK_BASE_URL"] = "http://should.be.ignored"

    explicit_url = "http://stockinfo-explicit.example.com:5678"
    stock_info = StockInfo(base_url=explicit_url)
    assert stock_info.api.base_url == explicit_url, f"Expected '{explicit_url}', got '{stock_info.api.base_url}'"
    print("[OK] StockInfo explicit URL test passed")

def test_stock_screener_default_url():
    """Test that default URL works for StockScreener"""
    print("\nTesting StockScreener default URL...")

    if "TONGSTOCK_BASE_URL" in os.environ:
        del os.environ["TONGSTOCK_BASE_URL"]

    screener = StockScreener()
    assert screener.api.base_url == "http://localhost:8991", f"Expected 'http://localhost:8991', got '{screener.api.base_url}'"
    print("[OK] StockScreener default URL test passed")

def test_stock_screener_env_var_url():
    """Test that environment variable works for StockScreener"""
    print("\nTesting StockScreener environment variable...")

    test_url = "http://screener.example.com:1234"
    os.environ["TONGSTOCK_BASE_URL"] = test_url

    screener = StockScreener()
    assert screener.api.base_url == test_url, f"Expected '{test_url}', got '{screener.api.base_url}'"
    print("[OK] StockScreener environment variable test passed")

def test_stock_screener_explicit_url():
    """Test that explicit URL parameter works for StockScreener"""
    print("\nTesting StockScreener explicit URL parameter...")

    os.environ["TONGSTOCK_BASE_URL"] = "http://should.be.ignored"

    explicit_url = "http://screener-explicit.example.com:5678"
    screener = StockScreener(base_url=explicit_url)
    assert screener.api.base_url == explicit_url, f"Expected '{explicit_url}', got '{screener.api.base_url}'"
    print("[OK] StockScreener explicit URL test passed")

def test_trailing_slash_removal():
    """Test that trailing slash is removed"""
    print("\nTesting trailing slash removal...")

    url_with_slash = "http://test.example.com/"
    api = TongStockAPI(base_url=url_with_slash)
    assert api.base_url == "http://test.example.com", f"Expected 'http://test.example.com', got '{api.base_url}'"
    print("[OK] Trailing slash removal test passed")

if __name__ == "__main__":
    print("TongStock API Environment Configuration Test")
    print("=" * 60)

    try:
        test_tongstock_api_default_url()
        test_tongstock_api_env_var_url()
        test_tongstock_api_explicit_url()
        test_stock_info_default_url()
        test_stock_info_env_var_url()
        test_stock_info_explicit_url()
        test_stock_screener_default_url()
        test_stock_screener_env_var_url()
        test_stock_screener_explicit_url()
        test_trailing_slash_removal()

        print("\n" + "=" * 60)
        print("[OK] All tests passed!")
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
