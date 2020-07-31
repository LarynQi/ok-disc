run:
	python3 ok-disc.py -v
build:
	python3 -m compileall ok-disc.py
	mv ./__pycache__/ok-disc.cpython-37.pyc ok
	rm -r ./__pycache__

clean:
	rm ok
	rm scheme
	