####
slog
####

The "slog" module extends the built-in Python logging library with custom logging levels and convenience functions for enabling and disabling logging.  It also includes some logging tools to help with unit tests.

Written by David C. Stauffer in March 2015 and separated into a stand-alone library in February 2022.


********************
Library dependencies
********************

This code is currently tested and maintained predominantly on Python v3.10, but will run on any version back to v3.6 or newer.

There are no external dependencies, but the code will use pytest as a test runner if it exists, reverting back to unittest otherwise, and has some tests that check features with numpy if that exists, and will otherwise skip those tests.

************
Installation
************

Currently, the code exists in a public GitHub repository at https://github.com/dstauffman/slog, but is intended to be released on PyPi in the near future.


**************
Using the code
**************

TODO: add example use cases here.

Extending the logging formatter
*******************************

TODO: add examples of how to further extend the custom logging wrappers.


**********************
Command Line Interface
**********************

In addition to importing the code as a library, some functionality is available through the command line interface.  The library should still be invoked as a module, and then has a few available commands, which themselves have further documentation.

For any of the given commands, you can get more information with a '-h' or '--help' option.

The following commands are available:

* help
* tests
* version
