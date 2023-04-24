from typing import Optional

from point import Point


class Circle:
    def __init__(self, radius: float, center: Optional[Point]=None) -> None:
        self.radius = radius
        self.center = center

    def __str__(self) -> str:
        return f'Circle({self.radius}, {self.center})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, Circle):
            return self.radius == other.radius and self.center == other.center

        return False

    def __ne__(self, other) -> bool:
        return not (self == other)

    def is_inside_main_circle(self, main_circle_radius: float) -> bool:
        return (self.center.x ** 2 + self.center.y ** 2) ** 0.5 <= \
            (main_circle_radius - self.radius)

    def is_overlap(self, other: any) -> bool:
        if not isinstance(other, Circle):
            raise TypeError(f"Expected Circle, but got {type(other)}")
        return is_two_circles_overlap(self, other)


def is_inside_main_circle(main_circle_radius, c: Circle) -> bool:
    return (c.center.x ** 2 + c.center.y ** 2) ** 0.5 <= (main_circle_radius - c.radius)


def outside_main_circle_value(main_circle_radius, c: Circle) -> float:
    return (c.center.x ** 2 + c.center.y ** 2) ** 0.5 - \
        (main_circle_radius - c.radius)


def is_two_circles_overlap(a: Circle, b: Circle) -> bool:
    return ((a.center.x - b.center.x) ** 2 +
            (a.center.y - b.center.y) ** 2) ** 0.5 < (a.radius + b.radius)


def two_circles_overlap_value(a: Circle, b: Circle) -> float:
    return ((a.center.x - b.center.x) ** 2 +
            (a.center.y - b.center.y) ** 2) ** 0.5 - (a.radius + b.radius)


def is_overlap(circles, new_circle):
    for c in circles:
        if c.center is not None and is_two_circles_overlap(c, new_circle):
            return True

    return False
