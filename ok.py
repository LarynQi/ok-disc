import subprocess
import re
import argparse
import sys

parser = argparse.ArgumentParser(description="Test your work")
parser.add_argument("func", metavar="function_to_test", help="Function to be tested")
parser.add_argument("-v", dest="v", action="store_const", const=True, default=False, help="Verbose output")
args = parser.parse_args()

src = ""
version = "0.1.1"

class Doctest():

    def __init__(self, test, output=""):
        self.test = test
        self.output = output

    def run(self, actual):
        base = f"scm> {self.test}\n{self.output}\n"
        if actual == self.output:
            return f"{base}-- OK! --\n", True
        return f"{base}Error: expected\n     {self.output}\nbut got\n     {actual}\n", False

    def __str__(self):
        return f"Input: {self.test}, Output: {self.output}"

doctest = re.compile(r"; Q\d\.\d - .*")
expect = re.compile(r"; expect .*")
test = re.compile(r"; \(.*\)\n")
no_tests = re.compile(r";;; No Tests\n")
buf = re.compile(r";;; Tests\n")

tests = {}
with open(src, "r") as f:
    found = False
    for line in f:
        if found:
            if re.match(buf, line):
                pass
            elif re.match(test, line):
                tests[question] = tests.get(question, []) + [Doctest(line.strip()[2:])]
            elif re.match(expect, line):
                tests[question][len(tests[question]) - 1].output += line.strip()[9:] + "\n"
            elif line == "\n" or re.match(no_tests, line):
                found = False
            else:
                print(line)
                sys.exit("Invalid doctest format")
        elif re.match(doctest, line):
            found = True
            question = line[2:line.index("\n")]

if args.func != "all":
    remove = list(filter(lambda func: func[-len(args.func):] == args.func, tests.keys()))
    if len(remove) > 1:
        sys.exit("Unexpected error")
    elif len(remove) == 0:
        sys.exit("Invalid function name")
    tests = {key:tests[key] for key in tests.keys() if key == remove[0]}

print(f"=====================================================================\nAssignment: Discussion {src[src.index('.') - 2:src.index('.')]}\nOK-disc, version v{version}\
\n=====================================================================\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
\nRunning tests\n")

prev = None
total = correct = 0
check = '(load-all ".")'
scheme = subprocess.Popen(["scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
parens = scheme.communicate(input=check)
for line in parens:
    if "SyntaxError" in line:
        sys.exit(f"scm> {check}\n # Error: unexpected end of file\n")
scheme.stdin.close()
while tests:
    scheme = subprocess.Popen(["scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    for line in scheme.stdout:
        break
    if tests:
        t = next(iter(tests.keys()))
        if not prev:
            count = 1
            print(f"---------------------------------------------------------------------\nDoctests for \033[1m{t[t.index('-') + 2:]}\033[0m\n")
            prev = t
        curr = tests[t][0]
        curr.output = curr.output.strip()
        raw_out = scheme.communicate(input=curr.test)[0]
        print(f"\033[4mCase {count}\033[0m:")
        test_out = curr.run(raw_out[:raw_out.index("\nscm>")])
        print(test_out[0])
        if args.v:
            correct += int(test_out[1])
            total += 1
        elif not test_out[1]:
            break
        tests[t].remove(curr)
        count += 1
        if not tests[t]:
            tests.pop(t)
            prev = None
        scheme.stdin.close()

if args.v:
    print(f"---------------------------------------------------------------------\n\
Test summary\n\
    Passed: {correct}\n\
    Failed: {total - correct}\n\
[ooooook....] {100 * round(correct / total, 3)}% passed\n")
sys.exit(0)
