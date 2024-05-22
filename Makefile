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
	$(_V)cd "$(BUILD)" && $(BEEBASM) -i "../dfs224.asm.txt" -v > "dfs224.beebasm.lst"
	$(_V)$(SHELLCMD) rm-file -f "$(BUILD)/dfs224.beebasm.bin"
	$(_V)$(SHELLCMD) rename "$(BUILD)/dfs224.bin" "$(BUILD)/dfs224.beebasm.bin"
	$(_V)$(PYTHON) "bin/convert_dfs_txt.py" "dfs224.asm.txt" -o "$(BUILD)/dfs224.s65"
	$(_V)$(TASS) $(TASSARGS) "$(BUILD)/dfs224.s65" -o "$(BUILD)/dfs224.bin" "-L$(BUILD)/dfs224.lst"

.PHONY:_folders
_folders:
	$(_V)$(SHELLCMD) mkdir "$(BUILD)"

##########################################################################
##########################################################################

.PHONY:clean
clean:
	$(_V)$(SHELLCMD) rm-tree "$(BUILD)"
