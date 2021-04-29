import sys
from lox import run_file, run_prompt

if len(sys.argv) > 2:
    print("Usage: lox.py [script]")
    exit(64)
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
else:
    run_prompt()