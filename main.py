import sys
import solver

target = int(sys.argv[1])
nums = [int(a) for a in sys.argv[2:]]

solver.solve(target, nums)

results = solver.solve(target, nums)
result_dict: dict[int, list[tuple[str, int, int]]] = dict()

min_diff = None
for r in results:
    diff = r[2]
    result_dict.setdefault(diff, [])
    result_dict[diff].append(r)

    if min_diff is None or diff < min_diff:
        min_diff = diff

for r in result_dict[min_diff]:
    for expr, result, diff in result_dict[min_diff]:
        print(expr, '=', result, '(', diff, ')')
