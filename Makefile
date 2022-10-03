FUNCTIONS := beatport deezer slack

.PHONY: tests

lint-functions:
	@for function in $(FUNCTIONS); do \
		echo "::Lint functions/$${function}"; \
		poetry run black functions/$${function}; \
		poetry run isort functions/$${function}; \
		poetry run mypy --strict functions/$${function}; \
	done;

lint-terraform:
	cd terraform && terraform fmt

lint-package:
	poetry run black ears tests
	poetry run isort ears tests
	poetry run mypy --strict ears

lint: lint-package lint-functions lint-terraform

tests:
	poetry run pytest tests

version:
	@cat pyproject.toml | grep version | cut -d'=' -f2 | tr -d '" '

bump-patch:
	poetry version patch

bump-minor:
	poetry version patch

bump-major:
	poetry version patch

git-deploy:
	git add --all
	git commit -m "🔖 deploy $$(cat pyproject.toml | grep version | cut -d'=' -f2 | tr -d '" ')"
	git push origin main

deploy-patch: lint bump-patch git-deploy
deploy-minor: lint bump-minor git-deploy
deploy-major: lint bump-major git-deploy

all: lint tests