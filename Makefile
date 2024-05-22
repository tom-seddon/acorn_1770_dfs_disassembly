PYTHON:=/usr/bin/python3
BEEBASM:=beebasm
TASS:=64tass

##########################################################################
##########################################################################

ifeq ($(VERBOSE),1)
_V:=
_TASSQ:=
else
_V:=@
_TASSQ:=-q
endif

##########################################################################
##########################################################################

BUILD:=build
SHELLCMD:=$(PYTHON) submodules/shellcmd.py/shellcmd.py
TASSARGS:=--nostart -Wall $(_TASSQ) --case-sensitive --line-numbers --verbose-list

##########################################################################
##########################################################################

.PHONY:build
build: _folders
	$(_V)$(TASS) $(TASSARGS) "dfs224.s65" -o "$(BUILD)/dfs224.bin" "-L$(BUILD)/dfs224.lst"
	$(_V)$(TASS) $(TASSARGS) "dfs224.s65" -Ddfs226=true -o "$(BUILD)/dfs226.bin" "-L$(BUILD)/dfs226.lst"
	$(_V)$(PYTHON) "bin/romdiffs.py" -a "$(BUILD)" -b "orig" "dfs224.bin" "dfs226.bin"

##########################################################################
##########################################################################

.PHONY:convert_and_build
convert_and_build:
	$(_V)$(MAKE) _convert_and_build "OPTIONS="
	$(_V)$(MAKE) _convert_and_build "OPTIONS=BUGFIX"
	$(_V)$(MAKE) _convert_and_build "OPTIONS=FASTGB"
	$(_V)$(MAKE) _convert_and_build "OPTIONS=FASTGB BUGFIX"
	$(_V)$(MAKE) _convert_and_build "OPTIONS=TURBO"
	$(_V)$(MAKE) _convert_and_build "OPTIONS=SQUEEZE"
	$(_V)$(MAKE) _convert_and_build "OPTIONS=NMOS"

.PHONY:_convert_and_build
_convert_and_build: OPTIONS?=$(error Must set OPTIONS)
_convert_and_build: _TASS_DEFINES=$(patsubst %,-D%=true,$(OPTIONS))
_convert_and_build: _BEEBASM_DEFINES=$(patsubst %,-D _%=-1,$(OPTIONS))
_convert_and_build: _folders
	$(_V)echo Options: $(OPTIONS)
	$(_V)cd "$(BUILD)" && $(BEEBASM) $(_BEEBASM_DEFINES) -i "../dfs224.asm.txt" -v > "dfs224.beebasm.lst"
	$(_V)$(SHELLCMD) rm-file -f "$(BUILD)/dfs224.beebasm.bin"
	$(_V)$(SHELLCMD) rename "$(BUILD)/dfs224.bin" "$(BUILD)/dfs224.beebasm.bin"
	$(_V)$(PYTHON) "bin/convert_dfs_txt.py" "dfs224.asm.txt" -o "$(BUILD)/dfs224.s65"
	$(_V)$(TASS) $(TASSARGS) $(_TASS_DEFINES) "$(BUILD)/dfs224.s65" -o "$(BUILD)/dfs224.bin" "-L$(BUILD)/dfs224.lst"
	$(_V)$(SHELLCMD) cmp "$(BUILD)/dfs224.beebasm.bin" "$(BUILD)/dfs224.bin"

##########################################################################
##########################################################################

.PHONY:_folders
_folders:
	$(_V)$(SHELLCMD) mkdir "$(BUILD)"

##########################################################################
##########################################################################

.PHONY:clean
clean:
	$(_V)$(SHELLCMD) rm-tree "$(BUILD)"

##########################################################################
##########################################################################

.PHONY:tom_laptop
tom_laptop:
	$(_V)$(MAKE)
