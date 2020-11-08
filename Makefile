all:
# 	make build
	@echo Not implemented

run:
	python3 ok-disc.py -v

DS_STORE = ./build/.DS_Store
ifneq ("$(wildcard $(DS_Store))","")
	DEL_DS = rm $(DS_Store)
else 
	DEL_DS = @:
endif

# ifeq (build,$(firstword $(MAKECMDGOALS)))
# 	BUILD_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# 	$(eval $(BUILD_ARGS):dummy;@:)
# endif

.PHONY: build

build:
	@$(delete)
	@python3 -m zipapp build -m "ok_disc:main" -o ok
	@make clean
	@mkdir out
	@mv ok ./out/ok
	@cp ./assets/code/scheme ./out/scheme
#   https://erictleung.com/user-input-makefile
	@cp ./src/$(filter-out $@,$(MAKECMDGOALS)) ./out/

	@echo Files can be found in ./out
	@echo 'Use make zip <name-of-zip> to generate zip'

# for command line args
%: 
	@:


ZIP = $(filter-out $@,$(MAKECMDGOALS))
ifneq ("$(wildcard $(ZIP))","")
	DEL_ZIP = rm -r $(ZIP)
else 
	DEL_ZIP = @:
endif

ZIPS = ./zips
ifeq ("$(wildcard $(ZIPS))","")
	MK_ZIPS = mkdir $(ZIPS)
	DEL_ZIPS = @:
else 
	MK_ZIPS = @:
	DEL_ZIPS = rm -r $(ZIPS)
endif


zip:
	$(MK_ZIPS)
	$(DEL_ZIP)
	mkdir $(filter-out $@,$(MAKECMDGOALS))
	cp -a ./out/. $(filter-out $@,$(MAKECMDGOALS))/
	zip -r ./zips/$(filter-out $@,$(MAKECMDGOALS)).zip $(filter-out $@,$(MAKECMDGOALS))
	rm -r $(filter-out $@,$(MAKECMDGOALS))

zip-inner:
	python3 -m zipapp ok_disc -m "ok_disc:main"

build-deprecated:
	python3 -m compileall ok-disc.py
	mv ./__pycache__/ok-disc.cpython-37.pyc ok
	rm -r ./__pycache__

build-windows:
	python3 -m compileall ok-disc-win.py
	mv ./__pycache__/ok-disc-win.cpython-37.pyc ok
	rm -r ./__pycache__

build-disc:
	python3 -m compileall ok-disc-build.py
	mv ./__pycache__/ok-disc-build.cpython-37.pyc ok
	rm -r ./__pycache__

OUT = ./out
ifneq ("$(wildcard $(OUT))","")
	CLEAN = @rm -r $(OUT)
else 
	CLEAN = @:
endif

clean:
	$(CLEAN)

clean-zips:
	$(DEL_ZIPS)
