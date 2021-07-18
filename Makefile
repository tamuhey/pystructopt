.PHONY: lint test exapmle publish test_all

MODULE="pystructopt"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test: run_example
	poetry run pytest

test_all:
	python test.py all

run_example:
	ls examples/*py | xargs poetry run python

publish: test_all lint
	git diff --exit-code # check working directory is clean
	poetry publish --build
