from pyomo.environ import *

##chose abstract model because the variables in the optimization formula are unknown until data is imported
model = AbstractModel()

model.n = Param(within=PositiveIntegers, initialize = 9)
model.o = Param(within=PositiveIntegers, initialize = 9)
model.b = Param(within=PositiveIntegers, initialize = 9)
model.I = RangeSet(1,model.b)
model.J = RangeSet(1,model.n)
model.K = RangeSet(1,model.o)

#establish the variables (xj, yijk, zk)
model.x = Var(model.J, within=Binary)
model.y = Var(model.I, model.J, model.K, within=Binary)
model.z = Var(model.K, within=Binary)

#establish the parameters(given variables): dijk, hik, U, P, Vhatk, qk, alpha, mk
model.d = Param(model.I, model.J) # snr
model.h = Param(model.I, model.K) # demand
model.U = Param(initialize = 0.8) # upper bound
model.P = Param(initialize = 2) # number of antennas
model.Vhat = Param(model.K) # best p-median value
model.q = Param(model.K) # probabilities
model.a = Param() # significance
model.m = Param(model.K) # largest possible regret
model.R = Var(model.K, within=Any)



#define the objective function
##unsure if i can do just minimizing W without establishing W as a summation of something

#def obj_rule(model):
#    return model.W
#model.obj = Objective(sense=minimize, expr = obj_rule)

model.W = Objective(expr=1)
model.W_var = Var(within=Any)
model.W = Objective(sense=minimize, expr = model.W_var)
#Constraints

## Constaint 1 sum(xj) <= P
def allocated_antenna_rule(model):
    return sum(model.x[j] for j in model.J) <= model.P
model.allocated_antenna = Constraint(rule = allocated_antenna_rule)

## Constraint 2 sum(yijk) = 1 for all i and k
def demand_met_rule(model, i, k):
    return sum(model.y[i,j,k] for j in model.J) <= 1
model.demand_met = Constraint(model.I, model.K, rule = demand_met_rule)

## Constraint 3 sum(yijk)/i >= U
def demand_met_perc_rule(model, k):
   return sum(model.y[i,j,k] for i in model.I for j in model.J)/model.b >= model.U
model.demand_met_perc = Constraint(model.K, rule = demand_met_perc_rule)

## Constraint 4 yijk - xj <= 0
def antenna_is_there_rule(model, i, j, k):
    return model.y[i,j,k] - model.x[j] <= 0
model.antenna_is_there = Constraint(model.I, model.J, model.K, rule = antenna_is_there_rule)

## Constraint 5 do not need b/c of objective function
def regret_function_rule(model, k):
    return (model.Vhat[k] - sum(h[i,k]*d[i,j]*model.y[i,j,k] for i in model.I for j in model.J)) == R[k]
model.regret_function = Constraint(model.K, rule = regret_function_rule)


## Constraint 6 sum(qkzk) >= a
def reliability_rule(model):
    return sum(model.q[k]*model.z[k] for k in model.K) <= model.a
model.reliability_rule = Constraint(rule = reliability_rule)

## Constraint 7 do not need b/c it is defined in the objective function
def W_rule(model, k):
    return model.W - model.R[k] + model.m[k]*(1-model.z[k]) >= 0
model.W_rule = Constraint(model.K, rule = W_rule)


## Constraint 8 xj-Fj<=0 (new)
#def feasible_placement_rule(model, j):
#    return model.x[j] - model.F[j] <= 0
#model.feasible_placement_rule = Constraint(model.J, rule = feasible_placement_rule)

## Constraint 9 Fj-Cj >= 0 (new)
#def antenna_necessity_rule(model, j):
#    return model.F[j] - model.C[j] >= 0
#model.antenna_necessity_rule = Constraint(model.J, rule = antenna_necessity_rule)


instance = model.create_instance()
opt = SolverFactory('glpk')
opt.solve(instance)
results = opt.solve(model, tee=True)

print(results.solver.status)

