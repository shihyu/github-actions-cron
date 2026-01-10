#!/usr/bin/env python3
"""
幣安加密貨幣報價爬蟲
爬取 BTC/USDT 和 ETH/USDT 即時報價
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests

# 常數定義
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
DATA_DIR = Path(__file__).parent.parent / "data"


def fetch_binance_price(symbol: str) -> Dict[str, str]:
    """
    爬取單一交易對的價格

    Args:
        symbol: 交易對符號，例如 "BTCUSDT"

    Returns:
        包含 symbol 和 price 的字典

    Raises:
        Exception: 當 API 請求失敗時
    """
    url = f"{BINANCE_API_URL}?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BinancePriceCrawler/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"錯誤: 無法爬取 {symbol} 價格 - {e}")
        raise


def fetch_all_prices() -> List[Dict[str, str]]:
    """
    爬取所有交易對的價格

    Returns:
        包含所有交易對價格的列表

    Raises:
        Exception: 當所有交易對都爬取失敗時
    """
    prices = []
    for symbol in SYMBOLS:
        try:
            price_data = fetch_binance_price(symbol)
            # 格式化價格，移除多餘的小數位
            price_data["price"] = f"{float(price_data['price']):.2f}"
            prices.append(price_data)
            print(f"✓ {symbol}: ${price_data['price']}")
        except Exception as e:
            print(f"✗ {symbol}: 爬取失敗")
            continue

    # 如果所有交易對都爬取失敗，拋出異常
    if not prices:
        raise Exception("所有交易對爬取失敗，無法獲取任何價格資料")

    return prices


def save_to_json(data: Dict, filepath: str) -> None:
    """
    儲存資料為 JSON 檔案

    Args:
        data: 要儲存的資料
        filepath: 檔案路徑
    """
    # 確保目錄存在
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # 儲存 JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 資料已儲存至: {filepath}")


def main() -> None:
    """主函數"""
    print("=" * 50)
    print("幣安加密貨幣報價爬蟲")
    print("=" * 50)

    # 爬取價格（如果全部失敗會拋出異常）
    print("\n正在爬取價格...")
    prices = fetch_all_prices()

    # 準備輸出資料
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    output_data = {
        "timestamp": timestamp,
        "source": BINANCE_API_URL,
        "data": prices
    }

    # 儲存 JSON
    filename = f"price_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    filepath = DATA_DIR / filename
    save_to_json(output_data, str(filepath))

    # 顯示摘要
    print("\n" + "=" * 50)
    print("爬取完成!")
    print(f"時間: {timestamp}")
    print(f"交易對數量: {len(prices)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
