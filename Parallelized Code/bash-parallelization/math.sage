import random
from random import uniform
import re
_=singular.lib('random.lib')
_=singular.lib('sing.lib')
_=singular.lib('poly.lib')
_=singular.lib('absfact.lib')
_=singular.lib('ring.lib')
_=singular.lib('nctools.lib')

class Poly():
    def __init__(self, numterms, maxcoeff, maxexp, numvars):
        self.t = numterms
        self.c = maxcoeff
        self.e = maxexp
        self.v = numvars

class Term():
    def __init__(self, variables, constant, exponent):
        self.v = variables
        self.c = constant
        self.e = exponent
        self.f = int(random.uniform(1,variables))

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
    lst = str(list(sageGarbage)[0])[1:-1].split(",")
    list2 = []
    for x in lst:
        list2.append(singular(x))
    return list2

def createPolynomial(newpoly):
    polynomial = []
    for Y in range(newpoly.t):
        polynomial.append(Term(newpoly.v, int(random.uniform(1,newpoly.c)), newpoly.e))
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

def rowReduceAxis(singularaxis):
    B = MatrixSpace(QQ,2,3)
    M = B([[1,99,singularaxis[0]],[1,100,singularaxis[1]]])
    return M.echelon_form()
    
def generalMilnor(polynomial, variables):
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
    return ideal.milnor()

def evaluate(polynomial,echelon_form, gMilnor):
    print(polynomial)
    print("lambda naught"+" "+str(echelon_form[0][2]))
    print("lambda one"+" "+str(echelon_form[1][2]))
    return {"polynomial": polynomial, "lambda naught": echelon_form[0][2],"lambda one": echelon_form[1][2], "general milnor": gMilnor, "beta invariant": echelon_form[1][2]-echelon_form[0][2]+gMilnor}

def master(polynomial):
    reduktion = reduction(polynomial)
    if testForICIS(polynomial, reduktion) == True:
        print(polynomial)
        axis = findSingularAxis(polynomial)
        if len(axis) >= 2:
            row_reduced = rowReduceAxis(axis)
            if row_reduced[1][2] != 1:
                gMilnor = generalMilnor(polynomial, findVariables(polynomial))
                result = evaluate(polynomial, row_reduced, gMilnor)
                if result != 'fail':
                    hits += 1
                    return evaluate

currentpolynomialtype = Poly(5, 10, 5, 5)
currentRing = singular.ring(0,createRingString(currentpolynomialtype.v),'ds')
currentPolynomial = createPolynomial(currentpolynomialtype)

random.seed
currentRing = singular.ring(0,createRingString(currentpolynomialtype.v),'ds')
currentPolynomial = createPolynomial(currentpolynomialtype)
master(currentPolynomial)