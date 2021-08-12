import uno

run_num = 1000

points = [0,0,0,0]

for simulation in range(run_num):
    results = uno.run({1:0})
    points[results-1]+=1

print(points)