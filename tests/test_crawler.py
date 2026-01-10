"""
測試爬蟲功能
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from crawler import fetch_binance_price, fetch_all_prices, save_to_json


class TestFetchBinancePrice:
    """測試單一交易對價格爬取"""

    @patch("crawler.requests.get")
    def test_fetch_btc_price_success(self, mock_get):
        """測試成功爬取 BTC/USDT 價格"""
        # Mock API 回應
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbol": "BTCUSDT",
            "price": "90616.11000000"
        }
        mock_get.return_value = mock_response

        # 執行測試
        result = fetch_binance_price("BTCUSDT")

        # 驗證
        assert result["symbol"] == "BTCUSDT"
        assert "price" in result
        assert float(result["price"]) > 0

    @patch("crawler.requests.get")
    def test_fetch_eth_price_success(self, mock_get):
        """測試成功爬取 ETH/USDT 價格"""
        # Mock API 回應
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbol": "ETHUSDT",
            "price": "3092.25000000"
        }
        mock_get.return_value = mock_response

        # 執行測試
        result = fetch_binance_price("ETHUSDT")

        # 驗證
        assert result["symbol"] == "ETHUSDT"
        assert "price" in result
        assert float(result["price"]) > 0

    @patch("crawler.requests.get")
    def test_fetch_price_api_error(self, mock_get):
        """測試 API 錯誤處理"""
        # Mock API 錯誤回應
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        # 執行測試，預期拋出例外
        with pytest.raises(Exception):
            fetch_binance_price("BTCUSDT")


class TestFetchAllPrices:
    """測試爬取所有交易對價格"""

    @patch("crawler.fetch_binance_price")
    def test_fetch_all_prices_success(self, mock_fetch):
        """測試成功爬取所有交易對"""
        # Mock 單一爬取函數
        def mock_fetch_side_effect(symbol):
            prices = {
                "BTCUSDT": {"symbol": "BTCUSDT", "price": "90616.11"},
                "ETHUSDT": {"symbol": "ETHUSDT", "price": "3092.25"}
            }
            return prices.get(symbol)

        mock_fetch.side_effect = mock_fetch_side_effect

        # 執行測試
        result = fetch_all_prices()

        # 驗證
        assert len(result) == 2
        symbols = [item["symbol"] for item in result]
        assert "BTCUSDT" in symbols
        assert "ETHUSDT" in symbols

    @patch("crawler.fetch_binance_price")
    def test_fetch_all_prices_all_fail(self, mock_fetch):
        """測試所有交易對都爬取失敗時拋出異常"""
        # Mock 爬取失敗
        mock_fetch.side_effect = Exception("API Error")

        # 執行測試，預期拋出異常
        with pytest.raises(Exception, match="所有交易對爬取失敗"):
            fetch_all_prices()

    @patch("crawler.fetch_binance_price")
    def test_fetch_all_prices_partial_success(self, mock_fetch):
        """測試部分交易對爬取成功（至少一個成功就應該返回）"""
        # Mock 單一爬取函數：BTCUSDT 成功，ETHUSDT 失敗
        def mock_fetch_side_effect(symbol):
            if symbol == "BTCUSDT":
                return {"symbol": "BTCUSDT", "price": "90616.11"}
            else:
                raise Exception("API Error")

        mock_fetch.side_effect = mock_fetch_side_effect

        # 執行測試
        result = fetch_all_prices()

        # 驗證：至少有一個成功，不應該拋出異常
        assert len(result) == 1
        assert result[0]["symbol"] == "BTCUSDT"


class TestSaveToJson:
    """測試 JSON 儲存功能"""

    def test_save_to_json_success(self, tmp_path):
        """測試成功儲存 JSON 檔案"""
        # 準備測試資料
        test_data = {
            "timestamp": "2026-01-11T12:00:00Z",
            "source": "https://api.binance.com/api/v3/ticker/price",
            "data": [
                {"symbol": "BTCUSDT", "price": "90616.11"},
                {"symbol": "ETHUSDT", "price": "3092.25"}
            ]
        }

        # 測試檔案路徑
        test_file = tmp_path / "test_output.json"

        # 執行測試
        save_to_json(test_data, str(test_file))

        # 驗證檔案存在
        assert test_file.exists()

        # 驗證檔案內容
        with open(test_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data["timestamp"] == test_data["timestamp"]
        assert loaded_data["source"] == test_data["source"]
        assert len(loaded_data["data"]) == 2

    def test_save_to_json_creates_directory(self, tmp_path):
        """測試自動建立目錄"""
        # 測試檔案路徑（目錄不存在）
        test_file = tmp_path / "subdir" / "test_output.json"

        # 準備測試資料
        test_data = {"test": "data"}

        # 執行測試
        save_to_json(test_data, str(test_file))

        # 驗證檔案和目錄都存在
        assert test_file.exists()
        assert test_file.parent.exists()
