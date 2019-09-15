# check to make sure all libraries are necessary
import random
import decimal
import time
from decimal import *
from random import uniform
_=singular.lib('random.lib')
_=singular.lib('sing.lib')
_=singular.lib('poly.lib')
_=singular.lib('absfact.lib')
_=singular.lib('ring.lib')

# generates trivariate polynomials and multiplies them together before testing

# class that holds the data for each polynomial
class poly():
    def __init__(self, Numterms, maxcoeff, maxexp, Numvars):
        self.t = Numterms
        self.c = maxcoeff
        self.e = maxexp
        self.v = Numvars

# class that holds the data for a single term in a polynomial

class term():
    def __init__(self, variables, constant, exponent):
        self.v = variables
        self.c = constant
        self.e = exponent
        self.f = int(random.uniform(1,variables))

# function that creates the names of the variables
# needs to be expanded upon

def createVarNames(numvars):
    varNames=[]
    if(numvars<27):
        for x in range(numvars):
            varNames.append(chr(x+65))
    else:
        return "too many variables!"
    return varNames

def createRingString(numvars):
    base = '('
    for x in range(numvars):
        base = base+(chr(x+65))+','
    base = base[:-1] + ')'
    return base

# function that does the heavy lifting of creating polynomials, builds a list of term objects

def createPolynomial(newpoly):
    polynomial = []
    for Y in range(newpoly.t):
        polynomial.append(term(newpoly.v, int(random.uniform(1,newpoly.c)), newpoly.e))
    return polynomial

# function that converts polynomial lists into strings interpretable by singular (sans errant unary operators)

def fixpoly(polyinlistform):
    stringPoly = ''
    varNames = createVarNames(polyinlistform[0].v)
    for X in range(len(polyinlistform)):
        stringPoly = stringPoly+'+'+str(polyinlistform[X].c)
        for Y in range(0,polyinlistform[X].f):
            stringPoly = stringPoly+varNames[int(random.uniform(0, polyinlistform[X].v))]+str(int(random.uniform(1,polyinlistform[X].e)))
    return stringPoly[1:]

# friendly user interface for math nerds

def start():
    print('Hello! Please enter the number of polynomials you would like to test:')
    attempts = int(input())
    print('Please enter the number of terms each polynomial should have:')
    terms = int(input())
    print('Please enter the maximum size of the coefficient on each of the terms:')
    maxcoeff = int(input())
    print('Please enter the maximum size of the exponent any variable can have inside of a single term:')
    maxexp = int(input())
    print('Please enter the number of variables you would like:')
    Numvars = int(input())
    return test(attempts, terms, maxcoeff, maxexp, Numvars)

# central testing function to clear polynomials pre manual beta invariant screening

def test(attempts, terms, maxcoeff, maxexp,Numvars):
    count = 0
    total = str(attempts)
    current = singular.ring(0,createRingString(Numvars),'ds')
    polys = []
    for x in range(attempts):
        polynomial = singular(fixpoly(createPolynomial(poly(terms,maxcoeff,maxexp,Numvars))))
        if singular.dim_slocus(polynomial)==2:
            polys.append(polynomial)
        if len(polys) == 2:
            multipliedPoly = polys[0]*polys[1]
            polys = []
            if singular.dim_slocus(multipliedPoly) ==1:
                print(multipliedPoly)
            if singular.dim_slocus(multipliedPoly) == 1 and singular.is_is(multipliedPoly.jacob())==0 and len(singular.minAssGTZ(multipliedPoly))==1:
                print(multipliedPoly)
                count=count+1
                num = num+1
    print(str(count)+" out of "+total+" were successful.")
    return 'complete'
# no common factors, one dimension singular sets

