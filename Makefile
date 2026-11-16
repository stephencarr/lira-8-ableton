.PHONY: all test test-experimental-tuning clean

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
	node tests/test-audio-input.cjs
	LIRA_ID_SIGN=-1 node tests/test-audio-input.cjs

# Retained calculations from withdrawn alpha 10; not part of the shipped device.
test-experimental-tuning:
	node tests/test-tuning.cjs
	LIRA_ID_SIGN=-1 node tests/test-tuning.cjs

clean:
	rm -rf build
