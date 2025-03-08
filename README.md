Disassembly of several versions of Acorn 1770 DFS. This project is
based on
[Greg Cook's disassembly of DFS 2.24](http://regregex.bbcmicro.net/dfs224.asm.txt).

# Goals

Goals:

* size up feasibility of adding additional stuff to Greg's ROM: B/B+
  compatibility (including utils commands, Tube host, and fancy B+128
  boot message), and any fixes or whatever from later DFS versions
  that would be good to have. (These updates would be expressed as
  additions to Greg's DFS 2.24 disassembly, similar to the existing
  build options)

Non-goals:

* particularly readable source code (sorry!) - I just added in .ifs as
  required, hopefully the minimum number necessary
* discovery of feature flags or code progression between versions -
  the various versions are selected by individual bools
* addition of significant additional comments not already found
  elsewhere

# Versions covered

Greg's disassembly covers the DFS supplied with the Master 128:

* DFS 2.24 (part of MOS 3.20)

I've added some additional stuff for the B+ version. The DFS code is
largely similar to DFS 2.24, and there's also some additional code for
Tube (previously investigated - see links in source), UTILS (comments
and labels copied from original DFS 1.20 code), and B+ fancy startup
message.

* DFS 2.26 (last B/B+/B+128-compatible version)

I also filled in some code to make it build the following other
versions, which appear to be official builds from Acorn. These
versions are a lot scrappier, but hopefully code vs data and all
relevant labels and references have been captured.

* DFS 2.25 (supplied on Master Compact welcome disk)
* DFS 2.28 (don't know where this came from! - but it's widely
  available and looks like an official build)
* DFS 2.29 (patched version supplied on Master 128 welcome disk)
* DFS 2.42 (supplied on the Olivetti PC 128 S Welcome disk)
* DFS 2.44 (part of [FinMOS 3.29](https://stardot.org.uk/forums/viewtopic.php?t=18510))
* DFS 2.45 (part of MOS 3.50)

# Build

## Prerequisites

* Python 3.x

On Unix:

* [`64tass`](http://tass64.sourceforge.net/) (I use r3120)
* GNU Make

(Prebuilt Windows EXEs for 64tass and make are included in the repo.)

## git clone

This repo has submodules. Clone it with `--recursive`:

    git clone --recursive https://github.com/tom-seddon/acorn_1770_dfs_disassembly
	
Alternatively, if you already cloned it non-recursively, you can do
the following from inside the working copy:

    git submodule init
	git submodule update

(The code won't build without fiddling around if you download one of
the archive files from GitHub - a GitHub limitation. It's easiest to
clone it as above.)

## Build steps

Type `make` from the root of the working copy.

The build process is supposed to be silent when there are no errors.

The output is 8 ROM images, as per the list above:

* `build/dfs224.bin` - DFS 2.24
* `build/dfs225.bin` - DFS 2.25
* `build/dfs226.bin` - DFS 2.26
* `build/dfs228.bin` - DFS 2.28
* `build/dfs229.bin` - DFS 2.29
* `build/dfs242.bin` - DFS 2.42
* `build/dfs244.truncated.bin` - DFS 2.44 (incomplete - additional MOS
  and ADFS code is not included)
* `build/dfs245.truncated.bin` - DFS 2.45 (incomplete - additional MOS
  and ADFS code is not included)

The repo includes original ROM images for all of the above and the
build process checks that the build output matches.

# More DFS versions

List of DFS versions:
https://mdfs.net/System/ROMs/Filing/Disk/Acorn/versions

# dir-locals.el

```
((nil . ((compile-command . "cd ~/beeb/acorn_dfs_2.26_disassembly && make tom_laptop"))))
```
