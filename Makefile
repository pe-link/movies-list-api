run:
	python3 ./src/app.py

lint:
	@echo "Executando flake8..."
	@flake8 . --count
	@if [ $$? -eq 0 ]; then \
    	echo "Nenhum erro encontrado pelo flake8."; \
	else \
    	echo "Erros encontrados pelo flake8."; \
	fi