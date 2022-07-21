import pandas as pd
from ortools.linear_solver import pywraplp

# 数据
distance = pd.read_table('distance.txt', header=None, index_col=None)
distance = distance.values.tolist()
city_num = len(distance)

# 求解器
solver = pywraplp.Solver.CreateSolver('SCIP')

# 决策变量
x = [[solver.IntVar(0, 1, 'x[{}][{}]'.format(i, j)) for j in range(city_num)] for i in range(city_num)]
y = [solver.IntVar(0, solver.infinity(), 'y[{}]'.format(i)) for i in range(city_num)]

# 目标函数
expression_obj = 0
for i in range(city_num):
    for j in range(city_num):
        expression_obj += distance[i][j] * x[i][j]
solver.Minimize(expression_obj)

# 约束
solver.Add(y[0] == 0, 'c0')
for i in range(city_num):
    solver.Add(sum([x[i][j] for j in range(city_num) if i != j]) == 1, 'c1[{}]'.format(i))  # 每个城市只能进一次
    solver.Add(sum([x[j][i] for j in range(city_num) if i != j]) == 1, 'c2[{}]'.format(i))  # 每个城市只能出一次
    solver.Add(y[i] <= city_num - 1, 'c3[{}]'.format(i))
    for j in range(1, city_num):
        if i == j:
            continue
        solver.Add(y[j] >= y[i] + 1 - (1 - x[i][j]) * city_num, 'c4[{}][{}]'.format(i, j))  # 防止多个圈

# 求解
# print(solver.ExportModelAsLpFormat(False))
print('number of variables = ', solver.NumVariables())
print('number of constraints = ', solver.NumConstraints())
status = solver.Solve()
# 结果
if status == solver.OPTIMAL:
    print('total length = ', solver.Objective().Value())
    print('the travel order is:')
    for i in range(city_num):
        for j in range(city_num):
            if y[j].solution_value() == i:
                print(j)
    print(0)
else:
    print('no optimal solution found')

