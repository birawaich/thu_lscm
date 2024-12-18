import pyomo.environ as pyo

### DATA ###
n = 5  # Number of warehouses
m = 7  # Number of markets

# Revenue on markets
revenue_data = [315.0, 326.0, 348.0, 292.0, 307.0, 289.0, 277.0]
assert len(revenue_data) == m, "Dimension error in revenue data."

# Fixed cost of warehouse
fixed_cost_data = [30000.0, 40000.0, 35000.0, 20000.0, 35000.0]
assert len(fixed_cost_data) == n, "Dimension error in fixed cost data."

# Warehose Capacity
warehouse_capacity = [350.0,350.0,350.0,350.0,350.0]
assert len(warehouse_capacity) == n, "dim error fixed cost"

# Market Demand
demand_market = [150.0,150.0,100.0,100.0,100.0,150.0,100.0]
assert len(demand_market) == m, "dim error demand"

# Transportation Cost
trans_cost = [
    [4.5, 5.0, 4.6, 5.5, 4.8, 4.1, 4.9],
    [4.8, 4.6, 4.9, 5.7, 5.7, 5.9, 4.0],
    [5.2, 5.1, 5.1, 4.2, 4.7, 4.0, 5.0],
    [5.2, 5.9, 4.3, 5.9, 5.7, 4.1, 4.7],
    [4.9, 5.3, 4.1, 4.5, 4.7, 5.6, 4.0]
]
assert len(trans_cost) == n\
    and len(trans_cost[0]) == m\
    , "dim error transportation costs" #note: does not check all rows

### MODEL ###
model = pyo.ConcreteModel()

# Sets
model.N = pyo.RangeSet(n)
model.M = pyo.RangeSet(m)

# Parameters
model.r = pyo.Param(model.M, initialize={i: revenue_data[i-1] for i in model.M})
model.f = pyo.Param(model.N, initialize={j: fixed_cost_data[j-1] for j in model.N})
model.K = pyo.Param(model.N, initialize={i: warehouse_capacity[i-1] for i in model.N})
model.D = pyo.Param(model.M, initialize={j: demand_market[j-1] for j in model.M})
model.c = pyo.Param(model.N, model.M,
                    initialize={(i,j): trans_cost[i-1][j-1] for i in model.N for j in model.M})

# Variables
model.y = pyo.Var(model.N, domain=pyo.Binary)
model.x = pyo.Var(model.N, model.M, domain=pyo.NonNegativeReals) #directly ensures that non-negative

# Objective function.
model.obj = pyo.Objective(
    expr=sum(model.r[j] * sum(model.x[i, j] for i in model.N) for j in model.M) #revenue
        - sum(model.f[i] * model.y[i] for i in model.N) #fixed cost
        - sum(model.c[i,j] * model.x[i,j] for j in model.M for i in model.N), #cost of transportation
    sense=pyo.maximize
)

# Constraints
model.constraints = pyo.ConstraintList()
for j in model.M:
    model.constraints.add(
        expr=sum(model.x[i,j] for i in model.N) <= model.D[j] #cannot sell more than demand in a region
    )
for i in model.N:
    model.constraints.add(
        expr=sum(model.x[i,j] for j in model.M) <= model.K[i]*model.y[i] #have to respect capacity
    )

### SOLVE ###
solver = pyo.SolverFactory('cbc')
result = solver.solve(model, tee=True)


### RESULTS ###
print("Solver Status:", result.solver.status)
print("Solver Termination Condition:", result.solver.termination_condition)
print("Optimal Objective Value:", pyo.value(model.obj))
print("===")
for j in model.N:
    print(f"y[{j}]: {pyo.value(model.y[j])}")
print("x[warehouse][market]")
for j in model.N:
    row_vals = []
    for i in model.M:
        row_vals.append(str(pyo.value(model.x[j,i])))
    print("\t".join(row_vals))
