# Lines that start with a '#' are comments
# These lines will not be treated as code or executed

########
# VIRTUAL ENVIRONMENTS
########

# Python (and other languages) can create 'virtual environments'
# which are basically folder- or repository-level instances of
# the language

# The HUGE advantage here is being able to install only the necessary
# libraries, packages, etc. per project and avoid conflicts

## Create A Virtual Environment

#   python -m venv virtual-environment-name
#   
#   this will create a folder 'virtual-environment-name' which, when
#   activated, will be the default src/dest for imports, installs, etc.

########
# INSTALLING WITH PIP
########

# pip is included with most installations of Python as the default package
# manager

## Installing with pip

#   pip install requests
#   pip install flask==1.0.1


########
# DOCSTRINGS
########

# DocStrings are a best practice that explain what your
# function does and what it should return

def add_two_numbers(num1,num2) -> int:
    '''
    Returns the sum of two integers as an integer

    Ex: (num1 = 1, num2 = 99) = 100
    '''

    return num1 + num2

########
# IMPORTS
########

# Since Python is a 'run-time' language, sets of features,
# AKA 'libraries', beyond base functionality are only enabled/imported
# as needed.

# Base Python installations come with many common/useful
# libraries already installed.

# Imports can occur in many lots of ways:

# 1) importing from an installed library
from requests import request

# 2) importing from a file
from imports.import_file1 import smile
from imports.import_file2 import *

def show_inline_import():
    from imports.import_file1 import frown
    
    print(frown())


##################
#  SCRATCH AREA
# ################

print(smile())
print(wink())
print(kiss())

# Why does this one fail?
print(frown())
# show_inline_import()