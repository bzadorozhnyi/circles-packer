import numpy as np

# f = -6x1 - 4x2 -> min
# -x1 + 2x2 <= 12
# 2x1 - x2 <= 14
# 3x1 + 4x2 <= 48
# x1, x2 >= 0
def calcfgA(x: np.ndarray) -> tuple[float, np.ndarray]:
    f = -6 * x[0] - 4 * x[1]
    g = np.array([-6, -4])

    P1, P2, P3, P4, P5 = 100, 100, 100, 100, 100

    penalty = 0

    temp = -x[0] + 2 * x[1] - 12
    if temp > 0:
        penalty += P1 * temp
        g[0] += -P1
        g[1] += 2 * P1

    temp = 2 * x[0] - x[1] - 14
    if temp > 0:
        penalty += P2 * temp
        g[0] += 2 * P2
        g[1] += -P2

    temp = 3 * x[0] + 4 * x[1] - 48
    if temp > 0:
        penalty += P3 * temp
        g[0] += 3 * P3
        g[1] += 4 * P3

    temp = -x[0]
    if temp > 0:
        penalty += P4 * temp
        g[0] += -P4

    temp = -x[1]
    if temp > 0:
        penalty += P5 * temp
        g[1] += -P5

    f = f + penalty
    # print(f, f1)

    return f, g


def calcfgB(x: np.ndarray) -> tuple[float, np.ndarray]:
    y = abs(x)
    f = -6 * y[0] - 4 * y[1]
    g = np.array([-6, -4])
    P1, P2, P3 = 100, 100, 100

    penalty = 0

    temp = -y[0] + 2 * y[1] - 12
    if temp > 0:
        penalty += P1 * temp
        g[0] += -P1
        g[1] += 2 * P1

    temp = 2 * y[0] - y[1] - 14
    if temp > 0:
        penalty += P2 * temp
        g[0] += 2 * P2
        g[1] += -P2

    temp = 3 * y[0] + 4 * y[1] - 48
    if temp > 0:
        penalty += P3 * temp
        g[0] += 3 * P3
        g[1] += 4 * P3

    f = f + penalty
    g = g * np.sign(x)

    return f, g


def ralgb5(x: np.ndarray, alpha: float, h0: float,
           q1: float, epsx: float, epsg: float, max_iteration: int, calcfg) -> np.ndarray:
    B = np.identity(len(x))
    hs = h0

    xr = np.copy(x)
    fr, g0 = calcfg(xr)

    if np.linalg.norm(g0) < epsg:
        # print('norm(g0) < epsg')
        return xr

    for i in range(max_iteration):
        g1 = np.dot(B.T, g0)
        dx = np.dot(B, g1) / np.linalg.norm(g1)

        d, ls, ddx = 1, 0, 0
        while d > 0:
            x -= hs * dx
            ddx += hs * np.linalg.norm(dx)

            f, g1 = calcfg(x)
            if f < fr:
                fr, xr = f, np.copy(x)

            if np.linalg.norm(g1) < epsg:
                # print('norm(g1) < epsg')
                return xr

            ls += 1
            if ls % 3 == 0:
                hs *= 1.1

            if ls > 500:
                # print('ls > 500')
                return xr

            d = np.dot(dx, g1)

        if ls == 1:
            hs *= q1

        if ddx < epsx:
            # print('ddx < epsx')
            return xr

        dg = np.dot(B.T, g1 - g0)
        xi = dg / np.linalg.norm(dg)

        B += (1 / alpha - 1) * np.dot(B, np.outer(xi, xi.T))
        g0 = g1

    # print('normal return')

    return xr


number_of_iterations = 1000
np.random.seed(2023)

EPS = 7 * 1e-8

result_1, result_2 = 1000000000, 1000000000
result_point_1, result_point_2 = [0, 0], [0, 0]

for _ in range(1, 1001):
    x = np.random.uniform(low=-100, high=100, size=(1, 2))[0]

    x1 = ralgb5(np.copy(x), 2, 1, 1, 1e-6, 1e-7, 3000, calcfgA)
    x2 = abs(ralgb5(np.copy(x), 2, 1, 1, 1e-6, 1e-7, 3000, calcfgB))

    if np.all(x1 >= -EPS) and (-x1[0] + 2 * x1[1] <= 12) and (2 * x1[0] - x1[1] <= 14) and (3 * x1[0] + 4 * x1[1] <= 48):
        result_1 = min(-6 * x1[0] - 4 * x1[1], result_1)
        result_point_1 = np.copy(x1)

    if np.all(x2 >= -EPS) and (-x2[0] + 2 * x2[1] <= 12) and (2 * x2[0] - x2[1] <= 14) and (3 * x2[0] + 4 * x2[1] <= 48):
        result_2 = min(-6 * x2[0] - 4 * x2[1], result_2)
        result_point_2 = np.copy(x2)

print(result_1)
print(result_point_1)

print(result_2)
print(result_point_2)
