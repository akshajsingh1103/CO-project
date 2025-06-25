# CO Project

## 1st Commit
- Initialized repo

## 2nd Commit
- Started out with c++
- Parsing through a given file and checking for instructions using regex

## 3rd Commit
- Basic structure for the assembler

## 4th Commit
- Changed to python from c++
- Parsing through a file whose path has been passed as an argument
- Checking for add instruction and printing the corresponding 32bit binary code

## 5th Commit
- Tried making the program work for different ISAs as well by making a single dict named operations and taking all the values from that dict only
- However checking for the exact syntax of the operations will not make it possible to make this program work with other ISAs
- But the program is working for the given ISA for only R type instructions for now

## 6th Commit
- Updated README.md

## 7th Commit
- Program now working for I type instructions as well

## 8th Commit
- Program now working for R, I and S instruction types
- Now considering negative numbers in immediate as well

## 9th Commit
- Working for B type

## 10th Commit
- Fixed B instruction type (I didn't see the sign extension earlier)
- R, I, S, B, U, J now all instruction types are working
- TODO: Label

## 11th Commit
- Program is now taking output path as 2nd arg

## 12th Commit
- Labels working

## 13th Commit
- Fixed J type

## 14th Commit
- Applied Virtual Halt

## 20th Commit
- Removed print stmt if virtual halt not present

## 26th Commit
- Added the basic code structure of our simulator which reads the file whose path has been given as the 1st arg and parse through the lines and outputs suitable memory addresses and register values as given in the project details to a file whose path has been given as the 2nd arg

## NOTE: On Linux, I had to manually add \n to all the simpleBin/test*.txt and bin_s/test*.txt and had to remove ^M (DOS-Windows line ending character) manually in order to make the program work
