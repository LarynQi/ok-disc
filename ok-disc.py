import sys

VERSION_MESSAGE = "\n" + """
ERROR: You are using Python {}.{}, but ok-disc is developed on Python 3.7.
This can lead to unexpected behavior. Make sure you are using the right
command (e.g. `python3 ok` instead of `python ok`) and that you have
Python 3.7+ installed.
""".strip() + "\n"

if sys.version_info[:2] < (3, 7):
    print(VERSION_MESSAGE.format(*sys.version_info[:2]))
    sys.exit(1)

import argparse
import urllib.request
import ssl
import platform
import os
from languages import *

src = ""
version = "0.1.7"

parser = argparse.ArgumentParser(prog="ok", description="A lightweight autograder to test your work!")
parser.add_argument("func", metavar="function_to_test", nargs="?", default=None, help="function to be tested (optional)")
parser.add_argument("-v", "--verbose", dest="v", action="store_const", const=True, default=False, help="verbose output")
parser.add_argument("-q", metavar="question_name", dest="q", nargs=1, type=str, default=None, help="question to be tested")
parser.add_argument("--version", dest="ask_version", action="store_const", const=True, default=False, help="print the version number and exit")

args = parser.parse_args()

if args.ask_version:
    sys.exit("ok-disc==v{!s}".format(version))

LANGUAGES = (Language.PYTHON, Language.SCHEME, Language.SQL)
files = []
extensions_present = []
try:
    for f in os.listdir():
        split = f.split(".")
        if len(split) > 1 and split[0] == src and split[1] in LANGUAGES:
            files.append(f)
            add = LANGUAGES[LANGUAGES.index(split[1])]
            add.file = f
            if add not in extensions_present:
                extensions_present.append(add)
except Exception as e:
    print(e)
    sys.exit("Unexpected files present")

REPO = "https://github.com/LarynQi/ok-disc"
tests = {}
for ext in extensions_present:
    if ext.interpreter and ext.interpreter not in os.listdir():
        url = "{!s}/raw/master/assets/code/{!s}".format(REPO, ext.interpreter)
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(url, ext.interpreter)
    ext.search(tests)

system = platform.system()
if system != "Windows":
    python = "python3"
    windows = False
else:
    python = "python"
    windows = True

if args.func or args.q:
    args.func = args.func if args.func else args.q[0]
    remove = list(filter(lambda func: func[-len(args.func):] == args.func, tests.keys()))
    if len(remove) > 1:
        sys.exit("An unexpected error has occurred")
    elif len(remove) == 0:
        sys.exit("Invalid function name")
    tests = {key:tests[key] for key in tests.keys() if key == remove[0]}
    Language.tests = tests

Language.tests = {k:v for k, v in sorted(tests.items(), key=lambda t: tests[t[0]])}
tests = Language.tests

print("=====================================================================\nAssignment: Discussion {!s}\nOK-disc, version v{!s}\
\n=====================================================================\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
\nRunning tests\n".format(src[len(src) - 2:len(src)], version))

result = ""
correct = total = 0
i = 0
cycled = -1
first = True
while tests:
    if i == cycled:
        break
    ext = extensions_present[i]
    run = ext.run(args, python, windows=windows)
    if run[1] == 0 and not args.v:
        if cycled == -1:
            cycled = i
            if not first:
                continue
    else:
        cycled = -1
    result, correct, total = result + run[0], correct + run[1], total + run[2]
    i = (i + 1) % len(extensions_present)
    first = False

result += "---------------------------------------------------------------------\nTest summary\n"
if args.v:
    result += "    Passed: {!s}\n    Failed: {!s}\n[ooooook....] {!s}% passed\n".format(correct, total - correct, round(100 * correct / total, 3))
else:
    if correct == total:
        result += "    {!s} test cases passed! No cases failed.\n".format(correct)
    else:
        result += "    {!s} test case(s) passed before encountering first failed test case\n".format(correct)

print(result)