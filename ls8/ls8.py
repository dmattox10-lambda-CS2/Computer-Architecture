#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("expects \"cpu.py program.ls8\" ")
    sys.exit(1)

cpu.load(sys.argv[1])
cpu.run()