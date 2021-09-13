.PHONY: format
format: 
	black -l 79 --target-version py39 pairing tests


.PHONY: style
style:
	black -l 79 --target-version py39 --check pairing tests
	pylint --reports=n --rcfile=pylintrc pairing tests

.PHONY: test
test: 
	pytest tests/unit --junitxml=./reports/report_unit_tests.xml -v
