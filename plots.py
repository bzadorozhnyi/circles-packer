from matplotlib import pyplot as plt
from circle import Circle

def draw_plot(main_circle_radius: float, circles: list[Circle],
              image_name, title):
    fig, ax = plt.subplots(1, 1)
    ax.add_patch(plt.Circle(
        (0, 0), main_circle_radius, linewidth=1, fill=False))
    
    for c in circles:
        ax.add_patch(plt.Circle((c.center.x, c.center.y),
                     c.radius, linewidth=1, fill=False))

    ax.set_aspect('equal')
    ax.plot()

    plt.title(title)

    fig.savefig(f'./{image_name}')
