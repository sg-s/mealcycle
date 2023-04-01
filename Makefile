
PID := $(shell cat streamlit.pid)

.PHONY: nightly start-app stop-app restart-app test coverage-report



start-app:
	@echo "Starting streamlit app.."
	@bash start-app.sh

stop-app:
	@echo "Stopping streamlit app..."
	-kill $(PID)


restart-app: stop-app start-app
	@echo "Restarting app..."


test:
	poetry run coverage run -m pytest -sx 
	-rm coverage.svg
	poetry run coverage-badge -o coverage.svg

coverage-report: .coverage
	poetry run coverage html --omit="*/test*"
	open htmlcov/index.html