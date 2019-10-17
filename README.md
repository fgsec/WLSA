# WLSA
Weblogic Security Assessment

**UNDER DEVELOPMENT**

## Purpose

Imagine that during an engagement you were able to download an entire weblogic cluster, and you now want to filter and parse only important stuff, like functions that may be vulnerable to RCE, LFI and so on. This tool will do exactly that, searching all folders for XML files, parsing files and even decompiling classes (with the help from JAD). 

## Install

```
pip3 install -r requirements.txt
```

## Usage

```
python3 main.py -folder /projects/weblogic_cluster/
```

## Todo

* Create Viewer class, to export in general formats (HTML,XML and so on).
* Develop the "action" system, to do actions based on rules.
* Add more detection rules.
* Improve detection logic to accept regexp


