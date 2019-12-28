# Mini-Lisp
NCU Compiler 2019 Final Project

## Overview

LISP is an ancient programming language based on S-expressions and lambda calculus. All operations in Mini-LISP are written in parenthesized prefix notation. For example, a simple mathematical formula `(1 + 2) * 3` written in Mini-LISP is:
``` 
(* (+ 1 2) 3)
```
As a simplified language, Mini-LISP has only three types (Boolean, number and function) and a few operations.

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

## Type Definition

* boolean: `#t` for true and `#f` for false.
* number: signed integer.
* function: See [Function](#function).

## Operation Overview

### Numerical Operators

|   Name   | Symbol |   Example   | Example Output |
|:--------:|:------:|:-----------:|:--------------:|
|   Plus   |   `+`  |  `(+ 1 2)`  |       `3`      |
|   Minus  |   `-`  |  `(- 1 2)`  |      `-1`      |
| Multiply |   `*`  |  `(* 2 3)`  |       `6`      |
|  Divide  |   `/`  |  `(/ 10 3)` |       `3`      |
|  Modulus |  `mod` | `(mod 8 3)` |       `2`      |
|  Greater |   `>`  |  `(> 1 2)`  |      `#f`      |
|  Smaller |   `<`  |  `(< 1 2)`  |      `#t`      |
|   Equal  |   `=`  |  `(= 1 2)`  |      `#f`      |

### Logical Operators

| Name | Symbol |    Example    | Example Output |
|:----:|:------:|:-------------:|:--------------:|
|  And |  `and` | `(and #t #f)` |      `#f`      |
|  Or  |  `or`  |  `(or #t #f)` |      `#t`      |
|  Not |  `not` |   `(not #t)`  |      `#f`      |

### Others

* `define`
    * def-stmt ::= (define ID EXP)
* `fun`
  ```bazaar
  fun-exp ::= (fun fun-id fun-body)
  fun-id ::= (id*)
  fun-body ::= exp  
  
  fun-call ::= fun-exp param* | fun-name param*
  ```

* `if`
    ```bazaar
     if-stmt ::= (if test-exp then-exp else-exp)
    ``` 

> All operators are reserved words, you cannot use any of these words as ID.

 
