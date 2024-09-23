from src.endpoints import fibonacci, factorial, mean


ROUTER = {
    ("fibonacci", "GET"): fibonacci,
    ("factorial", "GET"): factorial,
    ("mean", "GET"): mean,
}
