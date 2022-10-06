#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import shutil
import re
import copy
import stat
from xml.dom.minidom import parse
import time
import math
import json


def main():
    print('sh')
    print(len(sys.argv))
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])

    print("\ntest for for i in range(len(sys.argv))")
    for i in range(len(sys.argv)):
        print(sys.argv[i])

if __name__ == '__main__':
    main()