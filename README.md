# Mini-Lisp
NCU Compiler 2019 Final Project

## Overview

LISP is an ancient programming language based on *S-expressions* and *lambda calculus*. All operations in Mini-LISP are written in parenthesized prefix notation. For example, a simple mathematical formula `(1 + 2) * 3` written in Mini-LISP is:
``` 
(* (+ 1 2) 3)
```
As a simplified language, Mini-LISP has only three types (Boolean, number and function) and a few operations.

for more details goto `Mini-Lisp.pdf` and `Compiler Final Project.pdf`

## Features

### Basic Features

* [x] Syntax Validation
* [x] Print
* [x] Numerical Operations
* [x] Logical Operations
* [x] if Expression
* [x] Variable Definition
* [x] Function
* [x] Named Function

### Bonus Features

* [X] Recursion
* [X] Type Checking
* [X] Nested Function
* [X] First-class Function

## Usage

clone the project
``` 
git clone https://github.com/accelsao/Mini-Lisp.git
```
feed lisp standard input file
```
python main.py < [filename].lsp
```
with debug mode
```
python main.py < [filename].lsp --debug
```

## Install
Mini-Lisp requires the following dependencies:
* python 3
* lark 

install by the following command line
```
pip install -r requirements.txt
```