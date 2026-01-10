# 幣安加密貨幣報價爬蟲專案

## 任務目標
建立一個 Python 爬蟲專案，爬取幣安（Binance）的 BTC/USDT 和 ETH/USDT 即時報價，使用 GitHub Actions 自動排程執行。

## 專案結構組織
```
github-actions-cron/
├── .github/
│   └── workflows/
│       ├── main.yml          # 每分鐘執行的排程
│       └── manual.yml        # 手動觸發測試
├── src/
│   └── crawler.py            # 爬蟲主程式
├── tests/
│   └── test_crawler.py       # 測試檔案
├── data/
│   └── .gitkeep              # 報價資料目錄
├── requirements.txt          # Python 依賴
├── pyproject.toml           # uv 專案配置
├── Makefile                 # 建置工具
└── README.md                # 專案說明
```

## 功能規劃

### 爬蟲功能
- 爬取目標：幣安（Binance）公開 API
- 爬取內容：BTC/USDT、ETH/USDT 即時報價
- 輸出格式：JSON 檔案，包含時間戳記和價格資料
- 輸出位置：`data/price_{timestamp}.json`
- 執行頻率：**每 5 分鐘**（GitHub Actions 限制）

### GitHub Actions 配置
1. **main.yml** - 自動排程
   - 觸發條件：`schedule: cron '*/5 * * * *'` (每 5 分鐘)
   - 執行環境：ubuntu-latest
   - Python 版本：3.11
   - 使用 uv 管理依賴
   - **注意**：GitHub Actions cron 最小間隔為 5 分鐘，無法設定 30 秒

2. **manual.yml** - 手動觸發
   - 觸發條件：`workflow_dispatch`
   - 用於測試和除錯

### 執行頻率說明
- **目標**：每 30 秒抓一次（用戶需求）
- **GitHub Actions 限制**：最小 5 分鐘
- **替代方案**：
  1. 使用 GitHub Actions 每 5 分鐘執行（推薦，簡單）
  2. 本地運行：使用 cron/systemd timer 每 30 秒執行
  3. 部署到 VPS：使用 cron 每 30 秒執行

## Makefile 規範

### 必備目標
```makefile
.DEFAULT_GOAL := help

help:          ## 顯示可用指令
build:         ## 安裝依賴 (使用 uv)
run:           ## 執行爬蟲
test:          ## 執行測試
clean:         ## 清理輸出檔案和快取
```

## Build/Debug/Test 指令

### 開發環境建置
```bash
# 安裝 uv (如果尚未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝依賴
make build
# 或
uv sync
```

### 執行爬蟲
```bash
make run
# 或
uv run python src/crawler.py
```

### 執行測試
```bash
make test
# 或
uv run pytest tests/
```

### 清理
```bash
make clean
```

## 驗收標準

### 爬蟲功能
- [ ] 能成功爬取 GitHub API 資料
- [ ] 輸出 JSON 檔案格式正確
- [ ] 包含時間戳記和爬取內容
- [ ] 錯誤處理機制完整

### GitHub Actions
- [ ] main.yml 配置正確，排程設定為每分鐘
- [ ] manual.yml 可手動觸發
- [ ] workflow 成功執行並輸出結果
- [ ] 可查看執行紀錄

### 測試
- [ ] 測試覆蓋率 > 80%
- [ ] 測試包含：API 呼叫、檔案輸出、錯誤處理
- [ ] 所有測試通過

## 子任務拆解

### Phase 1: 專案初始化
1. 建立目錄結構
2. 建立 pyproject.toml 和 requirements.txt
3. 建立 Makefile
4. 建立 README.md

### Phase 2: 爬蟲實作
1. 實作 crawler.py 基本框架
2. 實作幣安 API 爬取邏輯（BTC/USDT, ETH/USDT）
3. 實作檔案輸出功能
4. 實作錯誤處理和重試機制

### Phase 3: 測試實作 (TDD)
1. 撰寫測試案例
2. 執行測試確認通過
3. 補充邊界測試

### Phase 4: GitHub Actions 配置
1. 建立 main.yml (每分鐘排程)
2. 建立 manual.yml (手動觸發)
3. 測試 workflow 配置

### Phase 5: 驗證與清理
1. 執行完整測試流程
2. 清理臨時檔案
3. 更新 README.md

## 專案配置

### 爬蟲目標
- 資料來源：幣安（Binance）公開 API
- API Endpoint：`https://api.binance.com/api/v3/ticker/price`
- 交易對：
  - BTC/USDT (symbol=BTCUSDT)
  - ETH/USDT (symbol=ETHUSDT)
- 方法：GET
- 回應格式：JSON
- 無需認證（公開 API）

### API 使用範例
```bash
# 單一交易對
curl "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# 多個交易對
curl "https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]"
```

### 輸出格式
```json
{
  "timestamp": "2026-01-11T12:00:00Z",
  "source": "https://api.binance.com/api/v3/ticker/price",
  "data": [
    {
      "symbol": "BTCUSDT",
      "price": "43521.50"
    },
    {
      "symbol": "ETHUSDT",
      "price": "2245.80"
    }
  ]
}
```

## 注意事項
- **GitHub Actions 限制**：cron 最小間隔為 5 分鐘，無法達到 30 秒執行
- **替代方案**：若需 30 秒執行，建議本地運行或部署到 VPS
- **幣安 API Rate Limit**：
  - 無認證：每分鐘 1200 請求
  - Weight: ticker/price endpoint = 2
  - 每 5 分鐘執行完全足夠
- **測試建議**：使用 manual.yml 手動觸發測試
- **時區**：使用 UTC 時間戳記
