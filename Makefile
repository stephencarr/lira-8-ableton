.PHONY: all test clean

all:
	python3 src/build.py
	python3 src/build-pads.py
	python3 src/build-delay.py

test: all
	python3 tests/check.py
	python3 tests/check-pads.py
	python3 tests/check-delay.py
	node tests/test-pads.cjs
	LIRA_ID_SIGN=-1 node tests/test-pads.cjs
	node tests/test-expression.cjs

clean:
	rm -rf build
