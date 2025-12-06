
import sys

with open(sys.argv[1], 'r') as f:
    lines = list(map(str.strip(), f.readlines()))
