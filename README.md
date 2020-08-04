<p align="center"><h1>ok-disc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/LarynQi/ok-disc/blob/master/assets/ok-logo.png" alt="drawing" height="50"/></h1></p>

A Python client for autograding Python and Scheme discussion files. Based on the [OK](https://github.com/okpy/ok-client) autograding system 

## Changelog
### v0.1.3 - 7/31/20
* Get rid of String formatting entirely (Bold, Italics, End)
* For verbose output, print out the entire output at once instead of multiple `print` statements

### v0.1.2 - 7/31/20
* Add auto-download `scheme` executable from personal website
  * Add ssl certification
* Compile `ok.py` into `ok` executable to hide source code
  * Add Makefile to automate compilation
* Have verbose and non-verbose outputs match real `ok`'s output exactly
  * Have non-verbose outputs display how many test cases passed (until first failed case if there is a failure)
* Generalize for Windows (`python` vs `python3`, String formatting)

### v0.1.1 - 7/30/20
* Add `(load-all ".")` to check for unmatched parentheses

### v0.1.0 - 7/30/20
* First release
* Local autograding handled for `.scm` files