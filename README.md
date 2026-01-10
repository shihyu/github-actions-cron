# 幣安加密貨幣報價爬蟲

使用 GitHub Actions 自動爬取幣安（Binance）的 BTC/USDT 和 ETH/USDT 即時報價。

## 功能特點

- 爬取幣安公開 API，獲取 BTC/USDT 和 ETH/USDT 即時價格
- 使用 GitHub Actions 自動排程，每 5 分鐘執行一次
- 輸出 JSON 格式，包含時間戳記和價格資料
- 無需 API 認證，使用公開端點
- 使用 `uv` 進行快速依賴管理

## 快速開始

### 前置需求

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Python 套件管理工具

### 安裝 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安裝依賴

```bash
make build
```

### 執行爬蟲

```bash
make run
```

### 執行測試

```bash
make test
```

### 清理

```bash
make clean
```

## 專案結構

```
github-actions-cron/
├── .github/
│   └── workflows/
│       └── main.yml          # 自動排程（每 5 分鐘）+ 手動觸發
├── src/
│   └── crawler.py            # 爬蟲主程式
├── tests/
│   └── test_crawler.py       # 測試檔案
├── data/                     # 報價資料輸出目錄
├── pyproject.toml           # 專案配置
├── requirements.txt         # Python 依賴
├── Makefile                 # 建置工具
└── README.md
```

## GitHub Actions 設定

### 自動排程 + 手動觸發（main.yml）

- 執行頻率：每 5 分鐘（`*/5 * * * *`）
- 觸發方式：
  - 自動執行（排程）
  - 手動觸發（在 GitHub Actions 頁面點擊 "Run workflow"）
- **注意**：GitHub Actions cron 最小間隔為 5 分鐘

## 輸出格式

爬蟲會在 `data/` 目錄下產生 JSON 檔案，格式如下：

```json
{
  "timestamp": "2026-01-11T12:00:00Z",
  "source": "https://api.binance.com/api/v3/ticker/price",
  "data": [
    {
      "symbol": "BTCUSDT",
      "price": "90616.11"
    },
    {
      "symbol": "ETHUSDT",
      "price": "3092.25"
    }
  ]
}
```

## API 資訊

- **端點**：`https://api.binance.com/api/v3/ticker/price`
- **方法**：GET
- **認證**：無需認證（公開 API）
- **Rate Limit**：每分鐘 1200 請求（無認證）

## 注意事項

- GitHub Actions 的 cron 最小間隔為 5 分鐘
- 幣安 API 有 rate limit 限制，請避免過度請求

## License

MIT