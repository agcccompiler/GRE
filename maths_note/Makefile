# Makefile for GRE Math Notes LaTeX Document
# 作者: 数学笔记
# 用途: 编译GRE数学核心知识点总结

# 文件名（不含扩展名）
TARGET = 1
SOURCE = $(TARGET).tex
PDF = $(TARGET).pdf

# LaTeX编译器
LATEX = pdflatex
BIBTEX = bibtex

# 编译选项ma
LATEX_FLAGS = -interaction=nonstopmode -shell-escape

# 默认目标
all: $(PDF)

# 主要编译规则
$(PDF): $(SOURCE)
	@echo "正在编译 $(SOURCE)..."
	$(LATEX) $(LATEX_FLAGS) $(SOURCE)
	@echo "编译完成！生成 $(PDF)"

# 快速编译（单次编译）
quick: $(SOURCE)
	@echo "快速编译 $(SOURCE)..."
	$(LATEX) $(LATEX_FLAGS) $(SOURCE)

# 完整编译（包括参考文献，如果需要的话）
full: $(SOURCE)
	@echo "完整编译 $(SOURCE)..."
	$(LATEX) $(LATEX_FLAGS) $(SOURCE)
	$(BIBTEX) $(TARGET)
	$(LATEX) $(LATEX_FLAGS) $(SOURCE)
	$(LATEX) $(LATEX_FLAGS) $(SOURCE)

# 清理临时文件
clean:
	@echo "清理临时文件..."
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg *.nav *.snm *.vrb

# 清理所有生成的文件（包括PDF）
cleanall: clean
	@echo "清理所有生成的文件..."
	rm -f $(PDF)

# 查看PDF文件
view: $(PDF)
	@echo "打开 $(PDF)..."
	@if command -v open >/dev/null 2>&1; then \
		open $(PDF); \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(PDF); \
	elif command -v evince >/dev/null 2>&1; then \
		evince $(PDF); \
	else \
		echo "无法自动打开PDF，请手动打开 $(PDF)"; \
	fi

# 安装依赖检查
check-deps:
	@echo "检查LaTeX环境..."
	@if command -v $(LATEX) >/dev/null 2>&1; then \
		echo "✓ $(LATEX) 已安装"; \
	else \
		echo "✗ $(LATEX) 未安装，请安装TeX Live或MiKTeX"; \
		exit 1; \
	fi
	@if command -v $(BIBTEX) >/dev/null 2>&1; then \
		echo "✓ $(BIBTEX) 已安装"; \
	else \
		echo "✗ $(BIBTEX) 未安装"; \
	fi

# 帮助信息
help:
	@echo "GRE数学笔记编译Makefile"
	@echo ""
	@echo "可用目标："
	@echo "  all        - 编译生成PDF（默认）"
	@echo "  quick      - 快速编译（单次）"
	@echo "  full       - 完整编译（多次，适用于有参考文献的文档）"
	@echo "  clean      - 清理临时文件"
	@echo "  cleanall   - 清理所有文件（包括PDF）"
	@echo "  view       - 编译并打开PDF"
	@echo "  check-deps - 检查LaTeX环境"
	@echo "  help       - 显示此帮助信息"
	@echo ""
	@echo "使用方法："
	@echo "  make        # 编译生成PDF"
	@echo "  make view   # 编译并查看PDF"
	@echo "  make clean  # 清理临时文件"

# 伪目标声明
.PHONY: all quick full clean cleanall view check-deps help

# 默认目标
.DEFAULT_GOAL := all
