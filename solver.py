import functools
from multiprocessing import Pool
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


def resolve_form(queue: Queue[Union[str, int]], depth: int = 0) -> int:
    curr = queue.pop()

    if isinstance(curr, int):
        return curr

    op1 = resolve_form(queue, depth+1)
    op2 = resolve_form(queue, depth+1)

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


def find_form_results(nums: list[int], form_str: str) -> list[tuple[str, int]]:
    results: list[tuple[str, int]] = []

    seen = set()
    form = form_str.split()
    for filled_form in fill_form(form, nums, '+-*/'):
        key = ' '.join([str(t) for t in filled_form])
        if key in seen:
            continue
        seen.add(key)

        term_queue = Queue(filled_form)
        result = resolve_form(term_queue)

        if result is None:
            continue

        expr_str = ' '.join([str(t) for t in filled_form])
        results.append((expr_str, result))

    return results


def solve(target: int, nums: list[int]) -> list[tuple[str, int, int]]:
    partial_find_results = functools.partial(find_form_results, nums)

    with Pool() as pool:
        results: list[list[tuple[str, int]]] = pool.map(partial_find_results, find_forms(len(nums)))

    flat_results: list[tuple[str, int, int]] = list()
    for r_list in results:
        for r in r_list:
            diff = abs(target - r[1])
            flat_results.append((r[0], r[1], diff))

    return flat_results