#!/usr/bin/env python3
"""
Test Stock Screener Module
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from stock_screener import StockScreener

def test_supported_signals():
    """Test getting supported signals"""
    print("Testing supported signals...")

    screener = StockScreener()
    signals = screener.get_supported_signals()

    print(f"✅ Supported signals: {', '.join(signals)}")

    # Check if expected signals are present
    expected = ["golden_cross", "death_cross", "overbought", "oversold"]
    assert isinstance(signals, list), "Expected list of signals"
    assert all(sig in expected for sig in signals), f"Unexpected signals: {[sig for sig in signals if sig not in expected]}"
    assert all(sig in signals for sig in expected), f"Missing signals: {[sig for sig in expected if sig not in signals]}"

def test_single_signal_screening():
    """Test screening with single signal"""
    print("\nTesting single signal screening...")

    screener = StockScreener()

    # Test with a single code
    result = screener.screen_by_signal(["600519"], "golden_cross")
    assert isinstance(result, dict), "Expected dictionary with matched and results"
    assert "matched" in result, "Result should include matched count"
    assert "results" in result, "Result should include results list"
    assert isinstance(result["matched"], int), "matched should be an integer"
    assert isinstance(result["results"], list), "results should be a list"
    print(f"✅ Screening result: matched={result['matched']}, results count={len(result['results'])}")

def test_multiple_codes_screening():
    """Test screening with multiple codes"""
    print("\nTesting multiple codes screening...")

    screener = StockScreener()

    # Test with multiple codes
    codes = ["600519", "000001"]
    result = screener.screen_by_signal(codes, "oversold")
    assert isinstance(result, dict), "Expected dictionary with matched and results"
    assert "matched" in result, "Result should include matched count"
    assert "results" in result, "Result should include results list"
    print(f"✅ Screening result for {len(codes)} codes: matched={result['matched']}, results count={len(result['results'])}")

def test_screening_with_date_range():
    """Test screening with date range"""
    print("\nTesting screening with date range...")

    screener = StockScreener()

    # Test with a date range
    result = screener.screen_by_signal(["600519"], "golden_cross", "day", "20260110", "20260120")
    assert isinstance(result, dict), "Expected dictionary with matched and results"
    assert "matched" in result, "Result should include matched count"
    assert "results" in result, "Result should include results list"
    print(f"✅ Screening result with date range: matched={result['matched']}, results count={len(result['results'])}")

def test_custom_criteria_screening():
    """Test screening with custom criteria"""
    print("\nTesting custom criteria screening...")

    screener = StockScreener()

    # Test with custom criteria
    codes = ["600519", "000001"]
    criteria = {
        "price_greater_than": 0,
        "price_less_than": 10000
    }

    result = screener.screen_by_criteria(codes, criteria)
    assert isinstance(result, list), "Expected list of results"
    assert len(result) > 0, "Expected at least one stock to match the criteria"
    print(f"✅ Custom criteria screening result: {result}")

if __name__ == "__main__":
    print("Stock Screener Module Test")
    print("=" * 50)

    try:
        test_supported_signals()
        test_single_signal_screening()
        test_multiple_codes_screening()
        test_custom_criteria_screening()
        print("\n" + "=" * 50)
        print("✅ All tests passed")
    except AssertionError as e:
        print(f"\n❌ Assertion failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")