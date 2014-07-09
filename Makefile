
.PHONY: test

test: parsefin/test/test_functional.py
	trial parsefin

parsefin/test/test_functional.py: parsefin/test/data/* util/generate-tests.py
	python util/generate-tests.py --output $@ --input parsefin/test/data/ --relative-root parsefin/test/