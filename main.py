import sys
import solver

target = int(sys.argv[1])
nums = [int(a) for a in sys.argv[2:]]

solver.solve(target, nums)

results = solver.solve(target, nums)
result_dict: dict[int, list[solver.Result]] = dict()

min_diff = None
for r in results:
    result_dict.setdefault(r.delta, [])
    result_dict[r.delta].append(r)

    if min_diff is None or r.delta < min_diff:
        min_diff = r.delta

for r in result_dict[min_diff]:
    print(" ".join(map(str, r.operations)), '=', r.result, '(', r.delta, ')')
