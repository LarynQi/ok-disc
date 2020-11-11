<p align="center"><h1>ok-disc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/LarynQi/ok-disc/blob/master/assets/img/ok-logo.png" alt="drawing" height="50"/></h1></p>

A Python client for autograding Python, Scheme, and SQL files. Based on the [OK](https://github.com/okpy/ok-client) autograding system 

## Changelog

### v0.1.5 - 11/7/20
* `ok-disc`
  * Fix Python version compatability by forgoing compilation
  * Instead, use `bombast` and send obfuscated source code
  * Converted all fstrings to `.format`'s for `bombast` to run properly
* Directory structure
  * `src`: Source code files (e.g. `mentor12.scm`)
  * `out`: Output folder containing source code file, `ok` executable, and any necessary interpreters (to be zipped)
  * `zips`: Contains zips ready to be released
* `Makefile`
  * Updated `make build` to generate `out` files
  * Added `make zip` target to compress `out` into a zip
  * Updated `make clean` to conform to new directory structure (cleans `out` folder)
  * Addded `make clean-zips` to remove generated zips
* Scripts:
  * `copy.sh`: Copies zip file to target destination in website repo
  * `deploy.sh`: Copies zip file to target destination in website repo and pushes a commit to redeploy website
 
### v0.1.4 - 8/4/20
* Ensure files in the current directory have not been renamed
* Fixed tabbing for multi-line erroneous output (resolved [#9](https://github.com/LarynQi/ok-disc/issues/9))
* Improved/more generalized doctest recognition
  * Allow for question numbers like `Q1.5i`
* `python3 ok` now shows logs for the first failed test case if any failed (resolved [#10](https://github.com/LarynQi/ok-disc/issues/10))

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
