import functools
import sys
import itertools
from typing import Union
from my_queue import Queue


@functools.cache
def find_forms(n: int) -> list[str]:
    if n == 1:
        return ['x']

    forms = set()
    for m in range(1, n):
        for sub_form1 in find_forms(m):
            for sub_form2 in find_forms(n - m):
                forms.add(f'? {sub_form1} {sub_form2}')
                forms.add(f'? {sub_form2} {sub_form1}')

    return forms


def fill_form(form: list[str], nums: list[int], ops: list[str]) -> list[list[Union[int, str]]]:
    filled_forms = []

    for op_ordering in itertools.product(ops, repeat=len(nums) - 1):
        # If all ops are + or all ops are *, order of nums does not matter
        num_permuations = [nums]
        if not (all([op == '+' for op in op_ordering]) or all([op == '*' for op in op_ordering])):
            num_permuations = itertools.permutations(nums, len(nums))

        for num_ordering in num_permuations:
            op_itr = iter(op_ordering)
            num_itr = iter(num_ordering)

            new_form = []
            for term in form:
                if term == '?':
                    new_form.append(next(op_itr))
                else:
                    new_form.append(next(num_itr))

            filled_forms.append(new_form)

    return filled_forms


def solve(queue: Queue[Union[str, int]], depth: int = 0) -> int:
    curr = queue.pop()

    if isinstance(curr, int):
        return curr

    op1 = solve(queue, depth+1)
    op2 = solve(queue, depth+1)

    if op1 is None or op2 is None:
        return None

    if curr == '+':
        return op1 + op2
    if curr == '-':
        return op1 - op2
    if curr == '*':
        return op1 * op2
    if curr == '/':
        if op2 == 0:
            return None
        if op1 == 0 or op2 % op1 != 0:
            return None
        return op1 // op2

    if curr == '^':
        assert False, "Power operation is not supported"
        return op1 ** op2


def main():
    target = int(sys.argv[1])
    nums = [int(a) for a in sys.argv[2:]]

    results: list[tuple[str, int]] = []

    for form_str in find_forms(len(nums)):
        print(form_str)
        form = form_str.split()
        for filled_form in fill_form(form, nums, '+-*/'):
            term_queue = Queue(filled_form)
            result = solve(term_queue)

            if result is None:
                continue

            expr_str = ' '.join([str(t) for t in filled_form])
            results.append((expr_str, result))

    for expr, result in sorted(results, key=lambda r: abs(target - r[1])):
        print(expr, '=', result, '(', abs(target-result), ')')


if __name__ == '__main__':
    main()
