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

import subprocess
import re
import argparse
import urllib.request
import ssl
import platform
import os

parser = argparse.ArgumentParser(description="Test your work")
parser.add_argument("func", metavar="function_to_test", nargs="?", help="Function to be tested")
parser.add_argument("-v", dest="v", action="store_const", const=True, default=False, help="Verbose output")
args = parser.parse_args()

src = ""
if src not in os.listdir():
    sys.exit("Please do not change the names of the provided files")
version = "0.1.5"
if "scheme" not in os.listdir():
    url = "https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/scheme"
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, "scheme")

system = platform.system()
if system != "Windows":
    python = "python3"
else:
    python = "python"

class Doctest():

    def __init__(self, test, output=""):
        self.test = test
        self.output = output

    def run(self, actual):
        base = "scm> {!s}\n{!s}\n".format(self.test, self.output)
        if actual == self.output:
            return base + "-- OK! --\n", True
        tab = "     "
        spaced_actual = ""
        for c in actual:
            if c == "\n":
                spaced_actual = c + tab
            else:
                spaced_actual += c
        return base + "Error: expected\n     {!s}\nbut got\n{!s}{!s}\n".format(self.output, tab, spaced_actual), False

    def __str__(self):
        return "Input: {!s}, Output: {!s}".format(self.test, self.output)

doctest = re.compile(r"; Q\d(\.\d)* - .*")
expect = re.compile(r"; expect .*")
test = re.compile(r"; .*\n")
no_tests = re.compile(r";;; No Tests\n")
buf = re.compile(r";;; Tests\n")

tests = {}
with open(src, "r") as f:
    found = False
    for line in f:
        if found:
            if re.match(buf, line):
                pass
            elif re.match(expect, line):
                tests[question][len(tests[question]) - 1].output += line.strip()[9:] + "\n"
            elif line == "\n" or re.match(no_tests, line):
                found = False
            elif re.match(test, line):
                tests[question] = tests.get(question, []) + [Doctest(line.strip()[2:])]
            else:
                print(line)
                sys.exit("Invalid doctest format")
        elif re.match(doctest, line):
            found = True
            question = line[2:line.index("\n")]

if args.func:
    remove = list(filter(lambda func: func[-len(args.func):] == args.func, tests.keys()))
    if len(remove) > 1:
        sys.exit("Unexpected error")
    elif len(remove) == 0:
        sys.exit("Invalid function name")
    tests = {key:tests[key] for key in tests.keys() if key == remove[0]}

print("=====================================================================\nAssignment: Discussion {!s}\nOK-disc, version v{!s}\
\n=====================================================================\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
\nRunning tests\n".format(src[src.index('.') - 2:src.index('.')], version))

prev = None
total = correct = 0
check = '(load-all ".")'
scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
parens = scheme.communicate(input=check)
for line in parens:
    if "SyntaxError" in line:
        sys.exit("scm> {!s}\n # Error: unexpected end of file\n".format(check))
scheme.stdin.close()
result = ""
while tests:
    scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    for line in scheme.stdout:
        break
    if tests:
        t = next(iter(tests.keys()))
        if not prev:
            count = 1
            if args.v:
                result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
            prev = t
        curr = tests[t][0]
        curr.output = curr.output.strip()
        raw_out = scheme.communicate(input=curr.test)[0]   
        test_out = curr.run(raw_out[:raw_out.index("\nscm>")])
        total += 1
        if args.v:
            result += "Case {!s}:\n".format(count)
            result += "{!s}\n".format(test_out[0])
        elif not test_out[1]:
            result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
            result += "Case {!s}:\n".format(count)
            result += "{!s}\n".format(test_out[0])
            break
        correct += int(test_out[1])
        tests[t].remove(curr)
        count += 1
        if not tests[t]:
            tests.pop(t)
            prev = None
    scheme.stdin.close()

result += "---------------------------------------------------------------------\nTest summary\n"
if args.v:
    result += "    Passed: {!s}\n    Failed: {!s}\n[ooooook....] {!s}% passed\n".format(correct, total - correct, 100 * round(correct / total, 3))
else:
    if correct == total:
        result += "    {!s} test cases passed! No cases failed.\n".format(correct)
    else:
        result += "    {!s} test case(s) passed before encountering first failed test case\n".format(correct)

print(result)