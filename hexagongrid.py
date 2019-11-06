from turtle import Screen, Turtle

OUTER_RADIUS = 75
INNER_RADIUS = 3**0.5 * OUTER_RADIUS / 2
SIDES = 6
EXTENT = 360 / SIDES


def tessellation(depth):
    turtle.right(EXTENT/2)

    for _ in range(SIDES):
        turtle.circle(OUTER_RADIUS, EXTENT, 1)

        if depth:
            heading = turtle.heading()

            turtle.right(90)
            tessellation(depth - 1)

            turtle.setheading(heading)

screen = Screen()
turtle = Turtle(visible=False)

screen.tracer(False)

turtle.penup()
turtle.goto(-OUTER_RADIUS / 2, -INNER_RADIUS)
turtle.pendown()
tessellation(2)

screen.tracer(True)

screen.exitonclick()
