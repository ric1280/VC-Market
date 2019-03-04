'''
Created on 03/07/2018

@author: ricar
'''

from pyparsing import *


#code = """\n # TODO: Add comment\n # \n # Author: ricar\n ###############################################################################\n \n \n   a[2][4] <-5.5\n  assign    (   "a[2]"   ,    45.6   )   \n wejbfjfbwebwbvwevn\n   pfact <- function(number) \n {\n \t\n \tfactors <- c()\n \tfactor <- 2\n \t\n \tif(number == 1)\n \t\treturn (1)\n \t\n \twhile( number != 1){\n \t\t\n \t\tif(number%%factor == 0){\n \t\t\tnumber <- number/factor;\n \t\t\tfactors <- c(factors, factor)\t\n \t\t}else{\n \t\t\tfactor <- factor + 1\n \t\t}\n \t}\n \t\n \treturn (factors)\n \t\n \t\n \t\n }\n \n #result <- pfact(234536332)\n \n result <- pfact(quiz)"""

var = Word( alphanums + "_-")

block_code = SkipTo("{") +  nestedExpr(opener='{', closer='}')
matrix_indexing =  Or([ZeroOrMore("["+Word(nums)+"]"), ZeroOrMore("[["+Word(nums)+"]]")])

var_assign = var + Suppress(matrix_indexing+Optional(White()) +"<-" + restOfLine)

var_assign2 = var +  Suppress(matrix_indexing+Optional(White()) + "=" + restOfLine)

var_assign3 =  Suppress("assign"+ Optional(White())+"("+ Optional(White()) + '"')+var+Suppress(matrix_indexing+'"'+Optional(White())+","+ restOfLine)

function = Suppress(var + matrix_indexing+ Optional(White()) + "<-" + Optional(White()) +"function" +Optional(White())+"(" + Suppress(SkipTo(")", include= True)) + block_code)

function2 = Suppress(var + matrix_indexing+ Optional(White()) + "=" + Optional(White()) +"function" +Optional(White())+ "(" + Suppress(SkipTo(")", include= True)) + block_code)

comment = Suppress(Optional(pythonStyleComment))

Exp =  Or( [comment , function , function2 , var_assign , var_assign2 ,var_assign3, Suppress(restOfLine)] )

def exprs(num_of_lines):
       
        grammar = Empty()
        for line in range(0,num_of_lines):
            grammar = grammar + Exp 
        return grammar


def getVariablesfromCode(code):
    
    countLine = ZeroOrMore(SkipTo("\n"))
    
    code_splited_by_lines =  countLine.parseString(code)
    num_of_lines = len(code_splited_by_lines)
    
    
    
    grammar = exprs(num_of_lines)
    variables = grammar.parseString( code )
    
    ##list(set()) is used to eliminate duplicates from the variable list
    return list(set(variables))

