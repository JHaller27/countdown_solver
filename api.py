from fastapi import FastAPI, Query, HTTPException, status
import solver
import pydantic


class NumbersResponse(pydantic.BaseModel):
    expression: str
    result: int
    delta: int


app = FastAPI(title="Countdown solver")


def filter_best_only(results: list[solver.Result]) -> list[solver.Result]:
    result_dict: dict[int, list[solver.Result]] = dict()

    min_diff = None
    for r in results:
        result_dict.setdefault(r.delta, [])
        result_dict[r.delta].append(r)

        if min_diff is None or r.delta < min_diff:
            min_diff = r.delta

    return result_dict[min_diff]


@app.get("/", response_model=list[NumbersResponse])
def solve(target: int = Query(...), numbers: list[int] = Query(...), best_only: bool = True) -> list[NumbersResponse]:
    if len(numbers) > 6:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="May pass no more than 6 numbers")

    solver.solve(target, numbers)

    results = solver.solve(target, numbers)

    if best_only:
        results = filter_best_only(results)

    results = [NumbersResponse(expression=" ".join(map(str, r.operations)), result=r.result, delta=r.delta) for r in results]

    return results
