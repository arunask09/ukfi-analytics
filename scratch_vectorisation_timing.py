import math
import time

import numpy as np

rng = np.random.default_rng(seed=42)
n = 100_000
big_tenors = rng.uniform(0.5, 30, n)
big_rates = rng.uniform(0.03, 0.06, n)

start = time.perf_counter()
naive_df = [math.exp(-t * r) for t, r in zip(big_tenors, big_rates)]
loop_time = time.perf_counter() - start
print(f"loop: {loop_time:.4f}s")


start = time.perf_counter()
vec_df = np.exp(-big_tenors * big_rates)
vec_time = time.perf_counter() - start
print(f"vectorised: {vec_time:.6f}s")
print(f"speedup: {loop_time / vec_time:.1f}x")
