import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("red")

    brad = turtle.Turtle()
    brad.shape("circle")
    brad.color("purple")
    brad.speed()
    brad.forward(1000)
    brad.right(90)
    brad.forward(100)
    brad.right(90)
    brad.forward(10)
    brad.right(90)
    brad.forward(1)
    brad.right(90)

draw_square()
