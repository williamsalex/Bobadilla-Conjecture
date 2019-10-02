# TO USE: type start() and follow prompts after pasting into a Sage MATH terminal

# check to make sure all libraries are necessary
import random
from random import uniform
_=singular.lib('random.lib')
_=singular.lib('sing.lib')
_=singular.lib('poly.lib')
_=singular.lib('absfact.lib')
_=singular.lib('ring.lib')
_=singular.lib('nctools.lib')

# holds the different characteristics for the polynomials to be generated

class poly():
    def __init__(self, Numterms, maxcoeff, maxexp, Numvars):
        self.t = Numterms
        self.c = maxcoeff
        self.e = maxexp
        self.v = Numvars

# dictates the possibilities available to the generated term and randomly selects the number of variables in the term

class term():
    def __init__(self, variables, constant, exponent):
        self.v = variables
        self.c = constant
        self.e = exponent
        self.f = int(random.uniform(1,variables))

# creates variable names

def createVarNames(numvars):
    varNames=[]
    if(numvars<52):
        for x in range(numvars):
            if(x<27):
                varNames.append(chr(x+65))
            else:
                varNames.append(chr(x+96))
    else:
        return "too many variables!"
    return varNames

def createRingString(numvars):
    base = '('
    for x in range(numvars):
        base = base+(chr(x+65))+','
    base = base[:-1] + ')'
    return base

# uses sage's jacobian matrix calculator so it doesnt screw with singular's strangely non abelian ring

def findJacobian(polynomial, numvars):
    listvars = createVarNames(numvars)
    for x in listvars:
        x = var(str(x))
    fixedString = createRingString(numvars).replace(","," ")[1:-1]
    fixedString = SR.var(fixedString)
    return jacobian(str(polynomial),fixedString)

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
    polys = []
    variables = createVarNames(Numvars)
    print("------------------")
    for x in range(attempts):
        current = singular.ring(0,createRingString(Numvars),'ds')
        polynomial = singular(fixpoly(createPolynomial(poly(terms,maxcoeff,maxexp,Numvars))))
        L = list(singular.jacob(polynomial))
        reducedL = []
        for X in L:
            reducedL.append(radical(X))
        i = singular.ideal(reducedL)
        if singular.dim_slocus(polynomial) == 1 and list(singular.is_is(i))[-1]==0 and len(singular.minAssGTZ(polynomial))==1:
            singularaxis = []
            for y in variables:
                x = str(polynomial)
                if singular(x+'+'+y+'100').milnor() != -1:
                    singularaxis.append(singular((x+'+'+y+'100')).milnor())
                    singularaxis.append(singular((x+'+'+y+'101')).milnor())
            if len(singularaxis) == 2:
                B = MatrixSpace(QQ,2,3)
                M = B([[1,99,singularaxis[0]],[1,100,singularaxis[1]]])
                if (M.echelon_form()[1][2]) != 1:
                    polycopy = str(polynomial)
                    for y in variables:
                        current = singular.ring(0,createRingString(Numvars),'ds')
                        polynomial = singular(polycopy)
                        x = str(polynomial)
                        x = x.replace(y,'0')
                        sansVar = (createRingString(Numvars).replace(y+",","")).replace(","+y,"")
                        current = singular.ring(0,sansVar,'ds')
                        var2 = []
                        if singular.dim_slocus(singular(x))==0:
                            current = singular.ring(0,createRingString(Numvars),'ds')
                            polynomial = singular(polycopy)
                            for x in variables:
                                if x != y:
                                    var2.append(x)
                            partialdivs = []
                            for x in var2:
                                partialdivs.append(polynomial.diff(x))
                            f = singular.ideal(partialdivs)
                            print('--')
                            print(polycopy)
                            print('--')
                            print(f)
                            print('--')
                            if f.milnor() != -1:
                                polys.append(polycopy)
                                count=count+1
                                print("beta invariant: "+(M.echelon_form()[1][2]-M.echelon_form()[0][2]+f.milnor()))
                                print("general milnor number: "+str(f.milnor()))
                                print("lambda one: "+str(M.echelon_form()[0][2]))
                                print("lambda naught: "+str(M.echelon_form()[1][2]))
                                print("------------------")
    print(str(count)+" out of "+total+" were successful.")
    return polys