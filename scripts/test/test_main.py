#!/usr/bin/env python3
"""
Test main.py commands and save results to test/result directory
"""

import subprocess
import json
import os
import sys

# 获取项目根目录（scripts 文件夹的绝对路径）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_command(command):
    """Run a command and return the output"""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            cwd=PROJECT_ROOT
        )

        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except Exception as e:
                print(f"Error parsing output: {e}")
                return result.stdout
        else:
            print(f"Error executing command: {result.stderr}")
            return None

    except Exception as e:
        print(f"Exception running command: {e}")
        return None

def save_result(filename, data):
    """Save data to JSON file in test/result directory"""
    result_dir = os.path.join(os.path.dirname(__file__), "test_result")
    os.makedirs(result_dir, exist_ok=True)

    file_path = os.path.join(result_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(data, dict) or isinstance(data, list):
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                f.write(str(data))

        print(f"Result saved to: {file_path}")
        return True

    except Exception as e:
        print(f"Error saving result: {e}")
        return False

def test_info_command():
    """Test info command"""
    print("\nTesting info command:")
    print("Command: python src/main.py info 600519 -d 20 -w 3 -m 2")

    command = "python src/main.py info 600519 -d 20 -w 3 -m 2"
    result = run_command(command)

    if result is not None:
        save_result("info.json", result)
    else:
        print("Test failed")

def test_company_command():
    """Test company command"""
    print("\nTesting company command:")
    print('Command: python src/main.py company 600519 -b "经营分析"')

    command = 'python src/main.py company 600519 -b "经营分析"'
    result = run_command(command)

    if result is not None:
        save_result("company.json", result)
    else:
        print("Test failed")

def test_screen_command():
    """Test screen command"""
    print("\nTesting screen command:")
    print('Command: python src/main.py screen "600519,000001,601138"')

    command = 'python src/main.py screen "600519,000001,601138"'
    result = run_command(command)

    if result is not None:
        save_result("screen.json", result)
    else:
        print("Test failed")

def test_signals_command():
    """Test signals command"""
    print("\nTesting signals command:")
    print("Command: python src/main.py signals")

    command = "python src/main.py signals"
    result = run_command(command)

    if result is not None:
        save_result("signals.json", result)
    else:
        print("Test failed")

def main():
    """Main test function"""
    print("Testing main.py commands")
    print("=" * 50)

    test_info_command()
    test_company_command()
    test_screen_command()
    test_signals_command()

    print("\n" + "=" * 50)
    print("All tests completed")

if __name__ == "__main__":
    main()
