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

def run(self, args, python):
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
def run(self, args, python):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    keys = iter(list(tests.keys()))
    for t in keys:
        if tests[t][0].language == self:
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

def run(self, args, python):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    check = '(load-all ".")'
    scheme = subprocess.Popen([python, "scheme", "-i", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    parens = scheme.communicate(input=check)
    for line in parens:
        if "SyntaxError" in line:
            sys.exit("---------------------------------------------------------------------\n\n{!s} {!s}\n# Error: unexpected end of file\n\n---------------------------------------------------------------------\nTest summary\n    0 test case(s) passed before encountering first failed test case\n".format(self.prompt, check))
    scheme.stdin.close()
    keys = iter(list(tests.keys()))
    for t in keys:
        if tests[t][0].language == self:
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

# https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
# setattr(Language, 'run', run)

# https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance
# Language.SCHEME.run = types.MethodType(run, Language.SCHEME)
Language.SCHEME.run = run.__get__(Language.SCHEME)

Language.SQL = Language("sql", "sqlite3", "sqlite3>", "sql")
doctest = re.compile(r"-- Q.* - .*")
expect = re.compile(r"-- expect .*")
test = re.compile(r"-- .*\n")
no_tests = re.compile(r"-- No Tests\n")
buf = re.compile(r"-- Tests\n")
offset = 1
Language.SQL.formatting = Formatting(doctest, expect, test, no_tests, buf, offset)

def run(self, args, python):
    tests = self.tests
    src = self.file
    result = ""
    prev = None
    total = correct = 0
    keys = iter(list(tests.keys()))
    for t in keys:
        if tests[t][0].language == self:
            while True:
                interpreter = subprocess.Popen(["sqlite3", "--init", src], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
                if not prev:
                    count = 1
                    if args.v:
                        result += f"---------------------------------------------------------------------\nDoctests for {t[t.index('-') + 2:]}\n\n"
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
                    break
        else:
            break
    return result, correct, total

Language.SQL.run = run.__get__(Language.SQL)