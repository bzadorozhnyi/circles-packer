import random

import numpy as np
from circle import Circle
from circular_placement_algorithm import heuristic_packing
from plots import draw_plot
from point import Point
from ralgb import ralgb5


random.seed(2023)

def dichotomy_step_ralgo(main_circle_radius: float, circles: list[Circle]) -> tuple[float, list[Circle]]:
    x = np.array([c.center.x for c in circles] +
                [c.center.y for c in circles] + [main_circle_radius])

    circles_radiuses = np.array([c.radius for c in circles])

    step_size = 40.96
    while step_size >= 0.01:
        while True:
            y = ralgb5(np.copy(x), 3, step_size, 1, 1e-6, 1e-7, 3000, circles_radiuses)
            if y[-1] >= x[-1]:
                break
            x = np.copy(y)

        step_size /= 2

    main_circle_radius = x[-1]
    for i in range(len(x) // 2):
        circles[i].center = Point(x[i], x[i + len(x) // 2])

    return main_circle_radius, circles

def main(radiuses: list[float], r_algo_optimization=True) -> tuple[float, list[Circle]]:
    main_circle_radius, circles = heuristic_packing(
        radiuses, number_of_iterations=50,
        number_of_flips=10, radius_difference=1000
    )

    if r_algo_optimization:
        main_circle_radius, circles = dichotomy_step_ralgo(main_circle_radius, circles)

    print(main_circle_radius)
    for c in circles:
        print(c.radius, c.center.x, c.center.y)

    draw_plot(main_circle_radius, circles, 'packed_circles', f'R={main_circle_radius}')



number_of_circles = int(input())
radiuses = []
for i in range(number_of_circles):
    radiuses.append(float(input()))

main(radiuses)