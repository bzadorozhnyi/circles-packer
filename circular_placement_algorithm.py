import copy
import math
import random

import numpy as np
from checker import is_valid_answer
from circle import (Circle, is_inside_main_circle, is_overlap,
                    outside_main_circle_value)
from point import Point


def get_rotated_point(y_coord, angle):
    angle = math.radians(angle)
    return Point(y_coord * math.sin(angle),
                 y_coord * math.cos(angle))


def closest_center_to_two_touching_circles(start_point: Point,
                                           c1: Circle, c2: Circle, c3: Circle):
    if (c1.center.x - c2.center.x) ** 2 + (c1.center.y - c2.center.y) ** 2 > \
            (2 * c3.radius + c1.radius + c2.radius) ** 2:
        return None

    delta = 1e-6
    A = np.array([start_point.x, start_point.y], dtype=np.float64)

    while True:
        J = np.array([[-2 * c1.center.x + 2 * A[0],
                       -2 * c1.center.y + 2 * A[1]],

                      [-2 * c2.center.x + 2 * A[0],
                       -2 * c2.center.y + 2 * A[1]]])

        R = np.array([
            (c1.center.x - A[0]) ** 2 +
            (c1.center.y - A[1]) ** 2 - (c1.radius + c3.radius + 0.01) ** 2,

            (c2.center.x - A[0]) ** 2 +
            (c2.center.y - A[1]) ** 2 - (c2.radius + c3.radius + 0.01) ** 2
        ])

        prevA = A

        if abs(np.linalg.det(J)) < 1e-18:
            return None

        A = A - np.dot(np.linalg.inv(J), R)

        if (abs(A - prevA) < delta).all():
            break

    return Point(A[0], A[1])


def center_of_small_circle_touch_main(prev_circle: Circle,
                                      small_circle: Circle,
                                      main_circle_radius: float) -> bool:

    E = prev_circle.center.x ** 2 + prev_circle.center.y ** 2 + \
        (main_circle_radius - small_circle.radius) ** 2 - \
        (small_circle.radius + prev_circle.radius + 0.1) ** 2

    a = 4 * (prev_circle.center.x ** 2 + prev_circle.center.y ** 2)

    b = -4 * prev_circle.center.x * E

    c = E ** 2 - ((2 * prev_circle.center.y) ** 2) * \
        ((main_circle_radius - small_circle.radius) ** 2)

    D = b ** 2 - 4 * a * c

    if D <= 0 or a == 0:
        return None

    x1 = (-b + math.sqrt(D)) / (2 * a)
    y1 = (E - 2 * prev_circle.center.x * x1) / (2 * prev_circle.center.y)

    x2 = (-b - math.sqrt(D)) / (2 * a)
    y2 = (E - 2 * prev_circle.center.x * x2) / (2 * prev_circle.center.y)

    return Point(x1, y1), Point(x2, y2)


def bad_angle(c1: Circle, c2: Circle, main_circle_radius: float) -> float:
    return math.atan(c1.radius / (main_circle_radius - c1.radius)) + \
        math.atan(c2.radius / (main_circle_radius - c2.radius))


def is_possible_to_place(circles, main_circle_radius, radius_difference):
    circles[0].center = Point(0, main_circle_radius - circles[0].radius)
    order_of_circles_placement = [0]

    for i in range(len(circles)):
        if circles[i].center is not None:
            continue

        left, right, angle_for_new_circle = 0, 360 - \
            bad_angle(circles[0], circles[i], main_circle_radius), -1

        for _ in range(50):
            angle = (left + right) / 2
            new_circle = Circle(circles[i].radius, get_rotated_point(
                main_circle_radius - circles[i].radius, angle))

            if is_overlap(circles, new_circle) is False:
                right = angle
                angle_for_new_circle = angle
            else:
                left = angle

        if angle_for_new_circle >= 0:
            circles[i] = Circle(circles[i].radius, get_rotated_point(
                main_circle_radius - circles[i].radius, angle_for_new_circle))
            order_of_circles_placement.append(i)

    for index in order_of_circles_placement:
        for i in range(len(circles)):
            if circles[i].center is not None:
                continue

            for start_point in center_of_small_circle_touch_main(circles[index], circles[i], main_circle_radius) or ():
                new_circle = Circle(circles[i].radius, start_point)

                if not is_overlap(circles, new_circle) and \
                        is_inside_main_circle(main_circle_radius, new_circle):
                    circles[i] = new_circle
                    break

            if circles[i].center is not None:
                break

    while len(order_of_circles_placement) > 0:
        new_order_of_circles_placement = []
        for index in range(len(order_of_circles_placement)):
            for circle_index, circle in enumerate(circles):
                if circle.center is not None:
                    continue

                for j in range(1, min(2, len(order_of_circles_placement)) + 1):
                    new_circle_center = closest_center_to_two_touching_circles(
                        Point(
                            0, 0), circles[order_of_circles_placement[index]],
                        circles[order_of_circles_placement[(index + j) % len(order_of_circles_placement)]], circle)

                    if new_circle_center is None:
                        continue

                    new_circle = Circle(circle.radius, new_circle_center)
                    if not is_overlap(circles, new_circle) and is_inside_main_circle(main_circle_radius, new_circle):
                        circles[circle_index] = new_circle
                        new_order_of_circles_placement.append(circle_index)
                        break

                if circles[circle_index].center is not None:
                    break

        order_of_circles_placement = new_order_of_circles_placement

    return circles


def is_possible_to_fit(radiuses, circles, main_circle_radius, radius_difference):
    circles = [Circle(radiuses[i]) for i in range(len(radiuses))]

    circles = is_possible_to_place(circles, main_circle_radius, radius_difference)

    for c in circles:
        if c.center is None:
            return False, circles

    return True, circles


def get_index_for_swap(circles, radius_difference):
    index1 = random.randint(0, len(circles) - 1)
    index2 = index1

    for index, c in enumerate(circles):
        if circles[index1].radius != c.radius and \
                abs(circles[index1].radius - c.radius) <= radius_difference:
            index2 = index
            break

    return index1, index2


def get_index_for_swap_slow(circles, radius_difference):
    index1 = random.randint(0, len(circles) - 1)
    index2 = [index1]

    for index, c in enumerate(circles):
        if circles[index1].radius != c.radius and\
                abs(circles[index1].radius - c.radius) <= radius_difference:
            index2.append(index)

    return index1, random.choice(index2)


def heuristic_packing(radiuses, number_of_iterations=50, radius_difference=25,
                number_of_flips=1):
    main_circle_radius = 5000.0

    answer, circles, new_circles = [Circle(r, Point(
        random.randint(-main_circle_radius / 2, main_circle_radius / 2), random.randint(-main_circle_radius / 2, main_circle_radius / 2))) for r in radiuses], [], []

    for iter in range(number_of_iterations):
        # print('iter', iter, main_circle_radius)
        left, right = 0, main_circle_radius

        while abs(right - left) >= 0.0001:
            middle = (left + right) / 2

            isPossible, circles = is_possible_to_fit(
                radiuses, circles, middle, radius_difference)

            if isPossible:
                right = middle
                new_circles = copy.deepcopy(circles)
            else:
                left = middle

        if all(c.center is not None for c in new_circles):
            new_main_circle_radius = right

            max_outside_main_circle_value = max(
                [outside_main_circle_value(new_main_circle_radius, c) for c in new_circles])

            if max_outside_main_circle_value > 0:
                new_main_circle_radius += 1.5 * max_outside_main_circle_value

            if new_main_circle_radius < main_circle_radius and is_valid_answer(new_main_circle_radius, new_circles):
                main_circle_radius = new_main_circle_radius
                answer = copy.deepcopy(new_circles)

        for _ in range(number_of_flips):
            index1, index2 = get_index_for_swap(circles,
                                                radius_difference)
            radiuses[index1], radiuses[index2] = \
                radiuses[index2], radiuses[index1]

    return main_circle_radius, answer
