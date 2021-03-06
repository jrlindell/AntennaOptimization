from pyomo.environ import *

model = AbstractModel()


##i,j,k:
# Set of demand nodes
#model.I = Set()
# Set of antenna locations
#model.J = Set()

model.m = Param(within=PositiveIntegers)
model.n = Param(within=PositiveIntegers)
model.I = RangeSet(1,model.m)
model.J = RangeSet(1,model.n)

#establish the variables (xj, yijk, zk)
model.x = Var(model.J, within=Binary)
model.y = Var(model.I, model.J, within=Binary)
#model.z = Var(model.K, within=Binary)

#establish the parameters(given variables): dijk, hik, U, P, Vhatk, qk, alpha, mk
model.d = Param(model.I, model.J) # snr
model.h = Param(model.I) # demand
#model.U = Param() # upper bound
model.P = Param() # number of antennas
model.Vhat = Param() # best p-median value
#model.q = Param(model.K) # probabilities
#model.a = Param(initialize=0.8) # significance
#model.m = Param(model.K) # largest possible regret


#define the objective function
##unsure if i can do just minimizing W without establishing W as a summation of something
def obj_rule(model):
    return sum(model.h[i]*model.d[i,j]*model.y[i,j] for i in model.I for j in \
              model.J) 
model.obj = Objective(rule = obj_rule, sense=minimize)


#Constraints

## Constaint 1 sum(xj) = P HAD TO CHANGE TO = P CAUSE OTHERWISE IT WOULD JUST HAVE XJ BE 0
def allocated_antenna_rule(model):
    return sum(model.x[j] for j in model.J) == model.P
model.allocated_antenna = Constraint(rule = allocated_antenna_rule)

## Constraint 2 sum(yijk) = 1 for all i and k
def demand_met_rule(model, i):
    return sum(model.y[i,j] for j in model.J) == 1
model.demand_met = Constraint(model.I, rule = demand_met_rule)

## Constraint 4 yijk - xj <= 0
def antenna_is_there_rule(model, i, j):
    return model.y[i,j] - model.x[j] <= 0
model.antenna_is_there = Constraint(model.I, model.J, rule = antenna_is_there_rule)

