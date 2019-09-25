def findjacob(polynomial):
    jacobian = list(polynomial.jacob())
    for y in range(len(jacobian)):
        varsinnomial=[]
        for x in createVarNames(Numvars):
            print(x)
            jacobian[y]=str(jacobian[y])
            if jacobian[y].find(x) != -1:
                print('hi')
                varsinnomial.append(x)
        if len(varsinnomial) == 1:
            jacobian[y]=jacobian[y][0:jacobian[y].find(varsinnomial[0])]+varsinnomial[0]
    return jacobian

jacobian(createVarNames

def findJacobian(polynomial, numvars):
    listvars = createVarNames(numvars)
    for x in listvars:
        x = var(str(x))
    fixedString = createRingString(numvars).replace(","," ")[1:-1]
    fixedString = SR.var(fixedString)
    return jacobian(str(polynomial),fixedString)

listvars = createVarNames(Numvars)
for x in listvars:
    x = var(str(x))
fixedString = createRingString(Numvars).replace(","," ")[1:-1]
fixedString = SR.var(fixedString)
print(fixedString)