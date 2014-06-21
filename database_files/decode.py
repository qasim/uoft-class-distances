import binhex
import sys

#binhex.hexbin('test.bin', sys.stdout)

file = open('test.bin', 'r')
print file.read()
