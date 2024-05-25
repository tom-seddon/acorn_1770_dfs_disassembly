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
versions, which were supplied (whether on disk or ROM) with official
Acorn hardware. These versions are a lot scrappier, but hopefully code
vs data and all relevant labels and references have been captured.

* DFS 2.25 (supplied on Master Compact welcome disk)
* DFS 2.29 (patched version supplied on Master 128 welcome disk)
* DFS 2.45 (part of MOS 3.50)

# more DFS versions

List of DFS versions:
https://mdfs.net/System/ROMs/Filing/Disk/Acorn/versions

# dir-locals.el

```
((nil . ((compile-command . "cd ~/beeb/acorn_dfs_2.26_disassembly && make tom_laptop"))))
```
