from pyomo.environ import ConcreteModel, Var, Objective, Constraint, maximize, Binary, SolverFactory

# Example data
items = ['item1', 'item2', 'item3', 'item4']
values = {'item1': 8, 'item2': 10, 'item3': 15, 'item4': 4}
weights = {'item1': 2, 'item2': 3, 'item3': 5, 'item4': 1}
capacity = 6

# Create a ConcreteModel
model = ConcreteModel()

# Define variables
# x[i] = 1 if we take item i, 0 otherwise
model.x = Var(items, domain=Binary)

# Objective: Maximize sum of value of chosen items
model.obj = Objective(expr=sum(values[i]*model.x[i] for i in items), sense=maximize)

# Constraint: Total weight cannot exceed capacity
model.weight_constraint = Constraint(expr=sum(weights[i]*model.x[i] for i in items) <= capacity)

# Solve the model
solver = SolverFactory('cbc')  # or 'glpk', 'gurobi', etc.
result = solver.solve(model, tee=True)

# Print results
print("Solver Status:", result.solver.status)
print("Solver Termination Condition:", result.solver.termination_condition)
print("Optimal Objective Value:", model.obj())
print("Selected Items:")
for i in items:
    if model.x[i].value == 1:
        print(" ", i)