.DEFAULT_GOAL := help

.PHONY: help
help:  ## 顯示此說明訊息
	@echo "可用目標："
	@echo "  make build   - 安裝依賴（使用 uv）"
	@echo "  make run     - 執行爬蟲"
	@echo "  make test    - 執行測試"
	@echo "  make clean   - 清理建置產物和資料"
	@echo ""
	@echo "使用範例："
	@echo "  make build && make run"
	@echo "  make test"

.PHONY: build
build:  ## 安裝依賴
	@echo "安裝依賴..."
	@command -v uv >/dev/null 2>&1 || (echo "錯誤: uv 未安裝，請執行: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	uv sync

.PHONY: run
run:  ## 執行爬蟲
	@echo "執行爬蟲..."
	uv run python src/crawler.py

.PHONY: test
test:  ## 執行測試
	@echo "執行測試..."
	uv run pytest tests/ -v

.PHONY: clean
clean:  ## 清理建置產物和資料
	@echo "清理建置產物..."
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "清理完成"
