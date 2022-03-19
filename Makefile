PLUGINS='amaconsole/plugins'
any2hash := $(wildcard ${PLUGINS}/hashcat/utils/*2hashcat.py ${PLUGINS}/john/*2john.py)

.DEFAULT_GOAL := build


data:
	@echo "ANY2HASH: ${any2hash}"
	install ${any2hash} -d amaconsole/utils/hashes/

home:
	python3 home.py

build: submodules data
	python3 setup.py build

requiroments:
	python3 -m pip install -r requirements.txt

requiromentsdev:
	python3 -m pip install -r requirements-dev.txt

install: requiroments build home
	python3 setup.py install

installdev: requiromentsdev build home
	python3 setup.py install

submodules:
	git submodule update --init --recursive

clean:
	rm -rf amaconsole/utils/hashes/*2{john,hashcat}.py
