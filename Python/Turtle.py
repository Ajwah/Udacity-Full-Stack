import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("red")

    brad = turtle.Turtle()
    brad.shape("circle")
    brad.color("purple")
    brad.speed()
    brad.forward(100)
    brad.right(90)
    brad.forward(50)
    brad.right(90)
    brad.forward(25)
    brad.right(90)
    brad.forward(12)
    brad.right(90)

draw_square()
