import sys
from my_queue import Queue


def debug(*args, mode=False):
    if mode:
        print("DEBUG:", *args, flush=True)



def solve(queue: Queue, depth: int = 0) -> int:
    curr = queue.pop()
    debug("    " * depth, "Popped:", curr)

    if curr.isnumeric():
        return int(curr)

    op1 = solve(queue, depth+1)
    op2 = solve(queue, depth+1)

    if curr == '+':
        return op1 + op2
    if curr == '-':
        return op1 - op2
    if curr == '*':
        return op1 * op2
    if curr == '/':
        return op1 // op2
    if curr == '^':
        return op1 ** op2


def main(args: list):
    queue = Queue()
    for item in args:
        queue.push(item)

    debug(queue)

    solution = solve(queue)
    print(solution)


if __name__ == '__main__':
    main(sys.argv[1:])

