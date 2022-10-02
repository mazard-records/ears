FUNCTIONS := beatport deezer slack
VERSION   := $(shell cat ../pyproject.toml | grep "version" | cut -d"=" -f2 | tr -d '"' | tr -d " ")
UNAME     := $(shell uname -s)

ifeq ($(UNAME),Linux)
	SED_OPTS := 
endif
ifeq ($(UNAME),Darwin)
	SED_OPTS := ""
endif

.PHONY: $(FUNCTIONS)/requirements.txt

requirements: $(wildcard */requirements.txt)
	@for i in $?; do sed -i $(SED_OPTS) 's/ears.*/ears>=$(VERSION)/g' "$${i}"; done;
	@echo "Functions requirements.txt updated"
