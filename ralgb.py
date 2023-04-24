import numpy as np


def calcfg(x: np.ndarray, radiuses: np.ndarray) -> tuple[float, np.ndarray]:
    cx = x[:len(radiuses)]
    cy = x[len(radiuses):2*len(radiuses)]
    main_circle_radius = x[-1]

    gx = np.zeros(len(radiuses))
    gy = np.zeros(len(radiuses))

    f, gr = x[-1], 1

    P1, P2 = 2000, 1000

    eps = 0.05

    temp = cx**2 + cy**2 - (main_circle_radius - radiuses)**2 + eps
    temp[temp <= 0] = 0
    f += P1 * np.sum(temp)
    gx += P1 * cx * (temp > 0)
    gy += P1 * cy * (temp > 0)
    gr -= P1 * np.sum((main_circle_radius - radiuses) * (temp > 0))

    i, j = np.triu_indices(len(radiuses), k=1)

    diff_cx = cx[i] - cx[j]
    diff_cy = cy[i] - cy[j]

    sq_diff_cx = np.square(diff_cx)
    sq_diff_cy = np.square(diff_cy)

    sq_sum_radiuses = np.square(radiuses[i] + radiuses[j])

    temp = -sq_diff_cx - sq_diff_cy + sq_sum_radiuses + eps

    positive_temp_mask = temp > 0
    positive_temp = temp[positive_temp_mask]

    f += np.sum(P1 * positive_temp)
    gx[i[positive_temp_mask]] -= P1 * diff_cx[positive_temp_mask]
    gy[i[positive_temp_mask]] -= P1 * diff_cy[positive_temp_mask]
    gx[j[positive_temp_mask]] += P1 * diff_cx[positive_temp_mask]
    gy[j[positive_temp_mask]] += P1 * diff_cy[positive_temp_mask]

    temp = -main_circle_radius + np.amax(radiuses)
    if temp > 0:
        f += P2 * temp
        gr -= P2

    g = np.concatenate([gx, gy, [gr]])

    return f, g


def ralgb5(x: np.ndarray, alpha: float, h: float,
           q1: float, epsx: float, epsg: float, max_iterations: int,
           radiuses: np.ndarray) -> np.ndarray:
    B = np.identity(len(x))

    result_x = np.copy(x)

    result_f, g0 = calcfg(result_x, radiuses)

    if np.linalg.norm(g0) < epsg:
        return result_x

    for _ in range(max_iterations):
        g1 = np.dot(B.T, g0)

        dx = np.dot(B, g1) / np.linalg.norm(g1)
        dx_norm = np.linalg.norm(dx)

        d, ls, ddx = 1, 0, 0
        while d > 0:
            x -= h * dx
            ddx += h * dx_norm

            f, g1 = calcfg(x, radiuses)
            if f < result_f:
                result_f, result_x = f, np.copy(x)

            if np.linalg.norm(g1) < epsg:
                return result_x

            ls += 1
            if ls % 3 == 0:
                h *= 1.1

            if ls > 500:
                return result_x

            d = np.dot(dx, g1)

        if ls == 1:
            h *= q1

        if ddx < epsx:
            return result_x

        r = np.dot(B.T, g1 - g0)
        r /= np.linalg.norm(r)

        B += (1 / alpha - 1) * np.dot(B, np.outer(r, r.T))
        g0 = g1


    return result_x
