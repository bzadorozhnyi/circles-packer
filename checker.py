from circle import Circle


def is_valid_answer(main_circle_radius: float, circles: list[Circle]) -> bool:
    for i in range(len(circles)):
        if not circles[i].is_inside_main_circle(main_circle_radius):
            return False

        for j in range(i + 1, len(circles)):
            if circles[i].is_overlap(circles[j]):
                return False

    return True
