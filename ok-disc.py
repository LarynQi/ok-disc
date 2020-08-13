#!/usr/bin/env python3
import subprocess
import re
import argparse
import sys
import urllib.request
import ssl
import platform
import os
from datetime import datetime
from datetime import timezone
from dateutil import tz

parser = argparse.ArgumentParser(description="Test your work")
parser.add_argument("func", metavar="function_to_test", nargs="?", help="Function to be tested")
parser.add_argument("-v", dest="v", action="store_const", const=True, default=False, help="Verbose output")
parser.add_argument("--decrypt", dest="decrypt", action="store_const", const=True, default=False, help="Decrypt next exam question")
args = parser.parse_args()

EXTENSIONS = ("py", "scm", "sql")
ssl._create_default_https_context = ssl._create_unverified_context
src = ""
q, extension = src.split(".")
PDT = tz.gettz("US/Pacific")
# TIME = datetime(2020, 8, 8, 1, 30, tzinfo=PDT)
now = datetime.now(tz=timezone.utc)
if args.decrypt:
    diff = (TIME - now).total_seconds()
    if diff <= 0:
        if src in os.listdir():
            sys.exit("Already decrypted")
        url = f"https://larynqi.github.io/assets/code/{src}"
        # url = f"https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/code/{src}"
        try:
            urllib.request.urlretrieve(url, src)
        except Exception as e:
            print(url)
            print(e)
        if extension == "scm" and "scheme" not in os.listdir():
            url = "https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/scheme"
            urllib.request.urlretrieve(url, "scheme")
        elif extension == "sql" and "sqlite3" not in os.listdir():
            url = "https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/sqlite3"
            urllib.request.urlretrieve(url, "sqlite3")
    else:
        local = tz.gettz()
        local = TIME.astimezone(local)
        days = int(diff // (3600 * 24))
        hours = int((diff // 3600) % 24)
        minutes = int((diff // 60) % 60)
        seconds = int(diff % 60)
        days_s = f"{days} days " if days > 0 else ""
        hours_s = f"{hours} hours " if hours > 0 else ""
        minutes_s = f"{minutes} minutes " if minutes > 0 else ""
        seconds_s = f"{seconds} seconds"
        sys.exit(f"Unlock the next question at {local.strftime('%m/%d/%Y %H:%M:%S %Z')} (in {days_s}{hours_s}{minutes_s}{seconds_s})")
    sys.exit(0)

if src not in os.listdir():
    sys.exit("You must decrypt first. If you've decrypted already, please do not change the names of the provided files")
version = "0.1.4 - Exam Tool"



if extension == "scm" and "scheme" not in os.listdir():
    url = "https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/scheme"
    urllib.request.urlretrieve(url, "scheme")

if extension == "sql" and "sqlite3" not in os.listdir():
    url = "https://github.com/LarynQi/LarynQi.github.io/raw/master/assets/sqlite3"
    urllib.request.urlretrieve(url, "sqlite3")

system = platform.system()
if system == "Darwin":
    python = "python3"
else:
    python = "python"

class Doctest():

    def __init__(self, language, test, output=""):
        self.language = language
        self.test = test
        self.output = output

    def run(self, actual):
        base = f"{self._convert()} {self.test}\n{self.output}\n"
        if actual.strip() == self.output.strip():
            return f"{base}-- OK! --\n", True
        tab = "     "
        spaced_actual = ""
        for c in actual:
            if c == "\n":
                spaced_actual += f"{c}{tab}"
            else:
                spaced_actual += c
        spaced_output = ""
        for c in self.output:
            if c == "\n":
                spaced_output += f"{c}{tab}"
            else:
                spaced_output += c
        return f"{base}Error: expected\n     {spaced_output}\nbut got\n{tab}{spaced_actual}\n", False

    def _convert(self):
        if self.language == "scheme":
            return "scm>"
        elif self.language == "sql":
            return "sqlite3>"
    def __str__(self):
        return f"Input: {self.test}, Output: {self.output}"

if extension == "scm":
    doctest = re.compile(r"; Q.* - .*")
    expect = re.compile(r"; expect .*")
    test = re.compile(r"; .*\n")
    no_tests = re.compile(r";;; No Tests\n")
    buf = re.compile(r";;; Tests\n")
elif extension == "sql":
    doctest = re.compile(r"-- Q.* - .*")
    expect = re.compile(r"-- expect .*")
    test = re.compile(r"-- .*\n")
    no_tests = re.compile(r"-- No Tests\n")
    buf = re.compile(r"-- Tests\n")

tests = {}
if extension == "sql":
    with open(src, "r") as f:
        found = False
        for line in f:
            if found:
                if re.match(buf, line):
                    pass
                elif re.match(expect, line):
                    tests[question][len(tests[question]) - 1].output += line.strip()[10:] + "\n"
                elif line == "\n" or re.match(no_tests, line):
                    found = False
                elif re.match(test, line):
                    tests[question] = tests.get(question, []) + [Doctest(extension, line.strip()[3:])]
                else:
                    print(line)
                    sys.exit("Invalid doctest format")
            elif re.match(doctest, line):
                found = True
                question = line[3:line.index("\n")]
elif extension == "scm":
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
                    tests[question] = tests.get(question, []) + [Doctest("scheme", line.strip()[2:])]
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

print(f"=====================================================================\nAssignment: Discussion 13 {'q' + q[-1]}\nOK-disc, version v{version}\
\n=====================================================================\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
\nRunning tests\n")

prev = None
total = correct = 0
result = save = ""

if extension == "py":
    v = "-v" if args.v else ""
    interpreter = subprocess.Popen([python, "-B", "-m", "doctest", src, "-v"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)    
    with open(src, "r") as f:
        for line in f:
            if line[:3] == "def":
                q = line[4:line.index("(")]
    if args.v:
        result += f"---------------------------------------------------------------------\nDoctests for {q}\n\n"
        expected_out = re.compile(r"Expected:\n.*Got:\n")
        count = 1
        found_expected = found_got = ok = False
        for line in interpreter.stdout:
            if line == "Trying:\n":
                result += f"Case {count}:\n>>> "
                found = True
                count += 1
                total += 1
            elif line == "Expecting:\n":
                found_expected = True
            elif line == "Got:\n":
                save = f"\nError: expected\n    {save}but got\n    "
                found_got = True
            elif line == "ok\n":
                result += save + "-- OK! --\n\n"
                correct += 1
            elif found_expected:
                save = line.strip() + "\n"
                found_expected = False
            elif found_got:
                result += f"{line.strip()}\n{save}{line.strip()}\n\n"
                found_got = False
            elif found:
                result += line.strip() + "\n"
                found = False
    else:
        expected_out = re.compile(r"Expected:\n.*Got:\n")
        count = 1
        found_expected = found_got = ok = False
        for line in interpreter.stdout:
            if line == "Trying:\n":
                save = f"Case {count}:\n>>> "
                found = True
                count += 1
                total += 1
            # elif line == "Expected:\n":
            #     result += f"Error: expected\n"
            #     found = True
            elif line == "Expecting:\n":
                found_expected = True
            elif line == "Got:\n":
                save += f"\nError: expected\n    {expected}but got\n    "
                found_got = True
            elif line == "ok\n":
                correct += 1
            elif found_expected:
                expected = line.strip() + "\n"
                found_expected = False
            elif found_got:
                line = line.strip() + "\n"
                result += f"{save[:save.index('Error') - 1] + line + save[save.index('Error') - 1:]}{line.strip()}\n\n"
                break
            elif found:
                save += line.strip() + "\n"
                found = False
if extension == "scm":
    check = '(load-all ".")'
    scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    parens = scheme.communicate(input=check)
    for line in parens:
        if "SyntaxError" in line:
            sys.exit(f"scm> {check}\n # Error: unexpected end of file\n")
    scheme.stdin.close()
    while tests:
        scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
        for line in scheme.stdout:
            break
        if tests:
            t = next(iter(tests.keys()))
            if not prev:
                count = 1
                if args.v:
                    result += f"---------------------------------------------------------------------\nDoctests for {t[t.index('-') + 2:]}\n\n"
                prev = t
            curr = tests[t][0]
            curr.output = curr.output.strip()
            raw_out = scheme.communicate(input=curr.test)[0]   
            test_out = curr.run(raw_out[:raw_out.index("\nscm>")])
            total += 1
            if args.v:
                result += f"Case {count}:\n"
                result += f"{test_out[0]}\n"
            elif not test_out[1]:
                result += f"---------------------------------------------------------------------\nDoctests for {t[t.index('-') + 2:]}\n\n"
                result += f"Case {count}:\n"
                result += f"{test_out[0]}\n"
                break
            correct += int(test_out[1])
            tests[t].remove(curr)
            count += 1
            if not tests[t]:
                tests.pop(t)
                prev = None
        scheme.stdin.close()
if extension == "sql":
    timeout = 0
    while tests:
        timeout += 1
        if timeout >= 1000:
            sys.exit("Timed out")
        interpreter = subprocess.Popen(["sqlite3", "--init", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
        if tests:
            t = next(iter(tests.keys()))
            if not prev:
                count = 1
                if args.v:
                    result += f"---------------------------------------------------------------------\nDoctests for {t[t.index('-') + 2:]}\n\n"
                prev = t
            curr = tests[t][0]
            curr.output = curr.output.strip()
            raw_out = interpreter.communicate(input=curr.test) 
            if raw_out[0] == "":
                raw_out = raw_out[1]
            test_out = curr.run(raw_out[:])
            total += 1
            if args.v:
                result += f"Case {count}:\n"
                result += f"{test_out[0]}\n"
            elif not test_out[1]:
                result += f"---------------------------------------------------------------------\nDoctests for {t[t.index('-') + 2:]}\n\n"
                result += f"Case {count}:\n"
                result += f"{test_out[0]}\n"
                break
            correct += int(test_out[1])
            tests[t].remove(curr)
            count += 1
            if not tests[t]:
                tests.pop(t)
                prev = None
        interpreter.stdin.close()

result += f"---------------------------------------------------------------------\nTest summary\n"
if args.v:
    result += f"    Passed: {correct}\n    Failed: {total - correct}\n[ooooook....] {100 * round(correct / total, 3)}% passed\n"
else:
    if correct == total:
        result += f"    {correct} test cases passed! No cases failed.\n"
    else:
        result += f"    {correct} test case(s) passed before encountering first failed test case\n"

print(result)
