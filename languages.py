from utils import *
import subprocess
import types

Language.PYTHON = Language("python", "", ">>>", "py")

doctest = re.compile(r"# Q.* - .*")
# https://stackoverflow.com/questions/940822/regular-expression-syntax-for-match-nothing
expect = re.compile(r"$^")
test = re.compile(r" *>>> .*\n")
no_tests = re.compile(r"$^")
buf = re.compile(r' *"""')
offset = 2

Language.PYTHON.formatting = Formatting(doctest, expect, test, no_tests, buf, offset)

def run(self, args, python, **kwargs):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    wrong = False
    keys = iter(list(tests.keys()))
    for t in keys:
        if not wrong and tests[t][0].language == self:
            while True:
                interpreter = subprocess.Popen([python, "-B", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
                if not prev:
                    count = 1
                    if args.v:
                        result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    prev = t
                curr = tests[t][0]
                curr.output = curr.output.strip()
                raw_out = interpreter.communicate(input=curr.test)
                interpreter.stdin.close()
                out = ""
                for o in raw_out:
                    out += o
                try:
                    test_out = curr.run(out[:out.index("\n{!s}".format(self.prompt))])
                except Exception as e:
                    import sys
                    sys.exit(out)
                total += 1
                if args.v:
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                elif not test_out[1]:
                    result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                    wrong = True
                    break
                correct += int(test_out[1])
                tests[t].remove(curr)
                count += 1
                if not tests[t]:
                    tests.pop(t)
                    prev = None
                    break
        else:
            break
    return result, correct, total

Language.PYTHON.run = run.__get__(Language.PYTHON)

Language.SCHEME = Language("scheme", "scheme", "scm>", "scm")
doctest = re.compile(r"; Q.* - .*")
expect = re.compile(r"; expect .*")
test = re.compile(r"; .*\n")
no_tests = re.compile(r";;; No Tests\n")
buf = re.compile(r";;; Tests\n")
offset = 0
Language.SCHEME.formatting = Formatting(doctest, expect, test, no_tests, buf, offset)

def run(self, args, python, windows):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    wrong = False
    check = '(load-all ".")'
    scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    parens = scheme.communicate(input=check)
    for line in parens:
        if "SyntaxError" in line:
            import sys
            sys.exit("---------------------------------------------------------------------\n\n{!s} {!s}\n# Error: unexpected end of file\n\n---------------------------------------------------------------------\nTest summary\n    0 test case(s) passed before encountering first failed test case\n".format(self.prompt, check))
    scheme.stdin.close()
    keys = iter(list(tests.keys()))
    for t in keys:
        if not wrong and tests[t][0].language == self:
            while True:
                interpreter = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
                for line in interpreter.stdout:
                    break
                if not prev:
                    count = 1
                    if args.v:
                        result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    prev = t
                curr = tests[t][0]
                curr.output = curr.output.strip()
                raw_out = interpreter.communicate(input=curr.test)[0]
                if windows:
                    raw_out = raw_out[1 + len(self.prompt) + 1:]
                interpreter.stdin.close()
                test_out = curr.run(raw_out[:raw_out.index("\n{!s}".format(self.prompt))])
                total += 1
                if args.v:
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                elif not test_out[1]:
                    result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                    wrong = True
                    break
                correct += int(test_out[1])
                tests[t].remove(curr)
                count += 1
                if not tests[t]:
                    tests.pop(t)
                    prev = None
                    break
        else:
            break
    return result, correct, total

Language.SCHEME.run = run.__get__(Language.SCHEME)

Language.SQL = Language("sql", "sqlite_shell.py", "sqlite3>", "sql")
doctest = re.compile(r"-- Q.* - .*")
expect = re.compile(r"-- expect .*")
test = re.compile(r"-- .*\n")
no_tests = re.compile(r"-- No Tests\n")
buf = re.compile(r"-- Tests\n")
offset = 1
Language.SQL.formatting = Formatting(doctest, expect, test, no_tests, buf, offset)

def run(self, args, python, **kwargs):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    wrong = False
    keys = iter(list(tests.keys()))
    for t in keys:
        if not wrong and tests[t][0].language == self:
            while True:
                interpreter = subprocess.Popen([python, "sqlite_shell.py", "-init", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
                if not prev:
                    count = 1
                    if args.v:
                        result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    prev = t
                curr = tests[t][0]
                curr.output = curr.output.strip()
                raw_out = interpreter.communicate(input=curr.test)
                interpreter.stdin.close()
                if raw_out[0] == "":
                    raw_out = raw_out[1]
                elif raw_out[1] == "":
                    raw_out = raw_out[0]
                test_out = curr.run(raw_out[:])
                total += 1
                if args.v:
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                elif not test_out[1]:
                    result += "---------------------------------------------------------------------\nDoctests for {!s}\n\n".format(t[t.index('-') + 2:])
                    result += "Case {!s}:\n".format(count)
                    result += "{!s}\n".format(test_out[0])
                    wrong = True
                    break
                correct += int(test_out[1])
                tests[t].remove(curr)
                count += 1
                if not tests[t]:
                    tests.pop(t)
                    prev = None
                    break
        else:
            break
    return result, correct, total

Language.SQL.run = run.__get__(Language.SQL)