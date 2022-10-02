FUNCTIONS := beatport deezer slack

.PHONY: tests

lint-functions:
	@for function in $(FUNCTIONS); do \
		echo "::Lint functions/$${function}"; \
		poetry run black functions/$${function}; \
		poetry run isort functions/$${function}; \
		poetry run mypy --strict functions/$${function}; \
	done;

lint:
	poetry run black ears tests
	poetry run isort ears tests
	poetry run mypy --strict ears

tests:
	poetry run pytest tests
