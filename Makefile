.PHONY: lint test exapmle publish test_all

MODULE="pystructopt"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test:
	pytest tests
	python examples/basic.py 3 --opt opt -e 1 -vvv -p a --foo 12

test_all:
	python test.py all

publish: test_all lint
	git diff --exit-code # check working directory is clean
	poetry publish --build
