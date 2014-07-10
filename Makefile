
.PHONY: test clean generate

test: generate
	trial parsefin

generate: parsefin/test/test_functional.py

parsefin/test/test_functional.py: parsefin/test/data/* util/generate-tests.py
	python util/generate-tests.py --output $@ --input parsefin/test/data/ --relative-root parsefin/test/

clean:
	rm parsefin/test/test_functional.py