import re
def _search(src, language):
    tests = Language.tests
    offset = language.formatting.offset
    with open(src, "r") as f:
        found = False
        found_python = False
        for line in f:
            if found:
                if found_python and not re.match(language.formatting.test, line) and not re.match(language.formatting.buf, line) and line.strip() != "":
                    i = 0
                    for c in line:
                        if c == " ":
                            i += 1
                        else:
                            break
                    tests[question][len(tests[question]) - 1].output += line[i:]
                elif language == Language.PYTHON and re.match(language.formatting.doctest, line):
                    question = line[2 :line.index("\n")]
                    number = line[3:(line[3:].index("-")) + 3 - 1]
                elif found_python and re.match(language.formatting.buf, line):
                    found_python = False
                elif language != Language.PYTHON and re.match(language.formatting.buf, line):
                    pass
                elif re.match(language.formatting.expect, line) and line != "\n":
                    tests[question][len(tests[question]) - 1].output += line.strip()[9 + offset:] + "\n"
                elif line == "\n" or re.match(language.formatting.no_tests, line):
                    found = False
                elif re.match(language.formatting.test, line):
                    tests[question] = tests.get(question, []) + [Doctest(language, number, line.strip()[2 + offset:])]
                    Doctest.max_q = max(Doctest.max_q, len(number.replace(".", "")))
                    if language == Language.PYTHON:
                        found_python = True
                else:
                    if language != Language.PYTHON:
                        import sys
                        sys.exit("Invalid doctest format")
                    # if not re.match(re.compile(r"def.*"), line):
                    #     print(line)
                    #     sys.exit("Invalid doctest format")

            elif re.match(language.formatting.doctest, line):
                found = True
                if language != Language.PYTHON:
                    question = line[2 + offset:line.index("\n")]
                    number = line[3 + offset:(line[3 + offset:].index("-")) + 3 + offset - 1]
                else:
                    question = line[2:line.index("\n")]
                    number = line[3:(line[3:].index("-")) + 3 - 1]

class Language:

    tests = {}

    def __init__(self, name, interpreter, prompt, extension, file=None):
        self.name = name
        self.interpreter = interpreter
        self.prompt = prompt
        self.extension = extension
        self.file = file
        self.formatting = None

    def search(self, tests={}):
        if not Language.tests:
            Language.tests = tests
        _search(self.file, self)

    def __eq__(self, other):
        return self.extension == other or self is other

    def __str__(self):
        return "Language: {!s}, Files: {!s}".format(self.name, self.files)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

class Formatting:

    def __init__(self, doctest, expect, test, no_tests, buf, offset):
        self.doctest = doctest
        self.expect = expect
        self.test = test
        self.no_tests = no_tests
        self.buf = buf
        self.offset = offset

class Doctest:

    subparts = {
    "": 0,
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
    "vi": 6,
    "vii": 7,
    "viii": 8,
    "ix": 9,
    "x": 10,
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8
    }

    max_q = 0

    def __init__(self, language, number, test, output=""):
        self.language = language
        self.number = number
        self.test = test
        self.output = output

    def run(self, actual):
        base = "{!s} {!s}\n{!s}{!s}".format(self.language.prompt, self.test, actual, "" if actual[len(actual) - 1] == "\n" else "\n")
        if actual.strip() == self.output.strip() or actual == self.output:
            return base + "-- OK! --\n", True
        tab = "     "
        spaced_actual = ""
        for c in actual:
            if c == "\n":
                spaced_actual += c + tab
            else:
                spaced_actual += c
        spaced_output = ""
        for c in self.output:
            if c == "\n":
                spaced_output += c + tab
            else:
                spaced_output += c
        return base + "Error: expected\n{!s}{!s}\nbut got\n{!s}{!s}\n".format(tab, spaced_output, tab, spaced_actual[:-1] if spaced_actual[len(spaced_actual) - 1] == "\n" else spaced_actual), False

    def __str__(self):
        return "Q{!s} - Input: {!s}, Output: {!s}".format(self.number, self.test, self.output)

    def __repr__(self):
        return self.__str__()

    def _extract(self):
        digits = total = 0
        roman = ""
        for c in self.number:
            if c.isalpha():
                if c in Doctest.subparts:
                    roman += c
            elif c.isnumeric():
                total = 10 * total + int(c) + Doctest.subparts[roman]
                digits += 1
                roman = ""
        total = 10 * total + Doctest.subparts[roman]
        while digits < Doctest.max_q:
            total *= 10
            digits += 1
        return total

    def __lt__(self, other):
        return self._extract() < other._extract()