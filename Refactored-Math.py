# TO USE: type start() and follow prompts after pasting into a Sage MATH terminal

# check to make sure all libraries are necessary
import random
from random import uniform
import re
from multiprocessing import Pool
_=singular.lib('random.lib')
_=singular.lib('sing.lib')
_=singular.lib('poly.lib')
_=singular.lib('absfact.lib')
_=singular.lib('ring.lib')
_=singular.lib('nctools.lib')

# holds the different characteristics for the polynomials to be generated

class poly():
    def __init__(self, numterms, maxcoeff, maxexp, numvars):
        self.t = numterms
        self.c = maxcoeff
        self.e = maxexp
        self.v = numvars

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

def findVariables(polynomial):
    stringyPoly = str(polynomial)
    regex = re.compile('[^a-zA-Z]')
    variables = regex.sub('', stringyPoly)
    return list(dict.fromkeys(list(variables)))

def fixJacob(sageGarbage):
    global currentRing
    lst = str(list(sageGarbage)[0])[1:-1].split(",")
    list2 = []
    for x in lst:
        list2.append(singular(x))
    return list2

# function that does the heavy lifting of creating polynomials, builds a list of term objects

def createPolynomial(newpoly):
    polynomial = []
    for Y in range(newpoly.t):
        polynomial.append(term(newpoly.v, int(random.uniform(1,newpoly.c)), newpoly.e))
    stringPoly = ''
    varNames = createVarNames(polynomial[0].v)
    for X in range(len(polynomial)):
        stringPoly = stringPoly+'+'+str(polynomial[X].c)
        for Y in range(0,polynomial[X].f):
            stringPoly = stringPoly+varNames[int(random.uniform(0, polynomial[X].v))]+str(int(random.uniform(1,polynomial[X].e)))
    return stringPoly[1:]

def reduction(inboundPoly):
    subject = singular(inboundPoly)
    singular.set_ring(currentRing)
    jacobianMatrix = findJacobian(subject, len(findVariables(subject)))
    return singular.radical(fixJacob(jacobianMatrix))

def testForICIS(subject, reduction):
    singular.set_ring(currentRing)
    if singular.dim_slocus(subject) == 1:
        if list(singular.is_is(reduction))[-1]==0:
            if len(singular.minAssGTZ(reduction))==1:
                return True
    return False

def findSingularAxis(polynomial):
    singularaxis = []
    variables = findVariables(polynomial)
    for y in variables:
        if singular(polynomial+'+'+y+'100').milnor() != -1:
            singularaxis.append(singular((polynomial+'+'+y+'100')).milnor())
            singularaxis.append(singular((polynomial+'+'+y+'101')).milnor())
    return singularaxis
    # if len(singularaxis) == 2:
    #     return singularaxis
    # else:
    #     return False

def rowReduceAxis(singularaxis):
    B = MatrixSpace(QQ,2,3)
    M = B([[1,99,singularaxis[0]],[1,100,singularaxis[1]]])
    return M.echelon_form()
    # if = 1 break -- [1][2]

### polynomial is a string
### variables are a list of variable names
def findSingularVariable(polynomial, variables):
    numvars = len(variables)
    for variable in variables:
        current = singular.set_ring(currentRing)
        stringPoly = polynomial
        stringPoly = stringPoly.replace(variable, '0')
        withoutVariable = (createRingString(numvars).replace(variable+",","")).replace(","+variable,"")
        newRing = singular.ring(0,withoutVariable, 'ds')
        var2 = []
        if singular.dim_slocus(singular(stringPoly))==0:
            current = singular.set_ring(currentRing)
            for variable2 in variables:
                if variable2 != variable:
                    var2.append(variable2)
            partialdivs = []
            for item in var2:
                singular.set_ring(currentRing)
                singularizedPoly = singular(polynomial)
                partialdivs.append(singularizedPoly.diff(item))
            ideal = singular.ideal(partialdivs)
    return ideal

def evaluate(polynomial,echelon_form):
    print "lambda naught"+" "+str(echelon_form[0][2])
    print "lambda one"+" "+str(echelon_form[1][2])
    return {"lambda naught": echelon_form[0][2],"lambda one": echelon_form[1][2]}
    # if ideal.milnor() != -1:
    #     return {"lambda naught": echelon_form[0][2],"lambda one": echelon_form[1][2]}
    # else:
    #     return 'fail'
    
def master(polynomial):
    global hits
    reduktion = reduction(polynomial)
    if testForICIS(polynomial, reduktion) == True:
        axis = findSingularAxis(polynomial)
        if len(axis) >= 2:
            row_reduced = rowReduceAxis(axis)
            if row_reduced[1][2] != 1:
                #ideal = findSingularVariable(polynomial, findVariables(polynomial))
                result = evaluate(polynomial, row_reduced)
                if result != 'fail':
                    hits += 1
                    return evaluate
hits = 0
currentRing = singular.ring()
currentPolynomial = singular('x')
def start():
    print('Hello! Please enter the number of polynomials you would like to find:')
    goal = int(input())
    print('Please enter the number of terms each polynomial should have:')
    terms = int(input())
    print('Please enter the maximum size of the coefficient on each of the terms:')
    maxcoeff = int(input())
    print('Please enter the maximum size of the exponent any variable can have inside of a single term:')
    maxexp = int(input())
    print('Please enter the number of variables you would like:')
    numvars = int(input())
    print('Please enter the number of processes you would like:')
    procs = int(input())
    random.seed
    currentpolynomialtype = poly(terms, maxcoeff, maxexp, numvars)
    count = 0
    while hits < goal:
        currentRing = singular.ring(0,createRingString(currentpolynomialtype.v),'ds')
        currentPolynomial = createPolynomial(currentpolynomialtype)
        master(currentPolynomial)
        count += 1
        print count

def jumpstart():
    random.seed
    currentpolynomialtype = poly(3, 10, 3, 3)
    count = 0
    while hits < 3:
        global currentRing
        currentRing = singular.ring(0,createRingString(currentpolynomialtype.v),'ds')
        currentPolynomial = createPolynomial(currentpolynomialtype)
        master(currentPolynomial)
        count += 1
        print count

def testOne(polynomial):
    global currentRing
    currentRing = singular.ring(0,createRingString(len(findVariables(polynomial))),'ds')
    currentPolynomial = polynomial
    master(currentPolynomial)

