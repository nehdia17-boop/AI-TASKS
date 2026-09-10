import turtle
import math

# ---- Extended palette: navy -> deep blue -> teal -> sea green -> powder blue -> lavender -> pinks ----
NAVY_BLUE    = "#16215C"
DARK_BLUE    = "#0A1B4D"
NAVY_TEAL    = "#0E3B4D"
SEA_GREEN    = "#2E8B67"
MINT         = "#7FC9A6"
POWDER_BLUE  = "#AEE3F0"
SKY_BLUE     = "#D6F0F7"
LAVENDER     = "#C6A8E0"
BABY_PINK    = "#F7C6D9"
BLUSH_PINK   = "#F0A0C0"
BARBIE_PINK  = "#E0218A"
DEEP_ROSE    = "#8E1856"

PALETTE = [NAVY_BLUE, DARK_BLUE, NAVY_TEAL, SEA_GREEN, MINT, POWDER_BLUE,
           SKY_BLUE, LAVENDER, BABY_PINK, BLUSH_PINK, BARBIE_PINK, DEEP_ROSE]
OUTLINE = "#0A1B4D"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def interpolate_color(palette_hex, t):
    """t in [0, 1] -> smooth blended RGB tuple across the whole palette."""
    rgbs = [hex_to_rgb(c) for c in palette_hex]
    n = len(rgbs) - 1
    pos = t * n
    i = min(int(pos), n - 1)
    frac = pos - i
    r = tuple(rgbs[i][k] + (rgbs[i + 1][k] - rgbs[i][k]) * frac for k in range(3))
    return tuple(round(v) for v in r)


def rotate_point(x, y, angle_deg):
    a = math.radians(angle_deg)
    return (x * math.cos(a) - y * math.sin(a),
            x * math.sin(a) + y * math.cos(a))


def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in (60, -120, 60, 0):
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_snowflake(t, order, size, fill_rgb, pensize, rotation_deg):
    height = size * math.sqrt(3) / 2
    # same centroid-centering as the matplotlib version
    start = (-size / 2, -height / 3)
    start = rotate_point(*start, rotation_deg)

    t.penup()
    t.goto(start)
    t.setheading(rotation_deg)
    t.pendown()

    t.pensize(pensize)
    t.pencolor(OUTLINE)
    t.fillcolor(fill_rgb)

    t.begin_fill()
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)
    t.end_fill()


def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=900)
    screen.bgcolor("white")
    screen.colormode(255)
    screen.title("Koch Snowflake Pinwheel")
    screen.tracer(0, 0)  # turn off animation for instant drawing

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    order = 3
    n_layers = 14
    scale = 340  # overall size in pixels

    for i in range(n_layers):
        frac = i / (n_layers - 1)
        size = scale * (1.0 - frac * 0.86)       # shrink toward center
        color = interpolate_color(PALETTE, frac)
        pensize = 1 + (1 - frac) * 2.5
        rotation = i * 3.0                        # gentle pinwheel twist
        draw_snowflake(t, order, size, color, pensize, rotation)

    # small center accent dot
    t.penup()
    t.goto(0, 0)
    t.dot(14, BARBIE_PINK)

    screen.update()
    screen.exitonclick()


if __name__ == "__main__":
    main()