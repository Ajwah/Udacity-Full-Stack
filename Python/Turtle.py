import turtle

window = turtle.Screen()
window.bgcolor("red")

def init_turtle(shape,color,speed):
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.speed(speed)
    return t

def draw_square(ln):    
    brad = init_turtle("circle","purple",2)
    for i in range(0,4):
        brad.forward(ln)
        brad.right(90)

def draw_triangle(ln):
    genie = init_turtle("classic","green",4)
    for i in range(1,4):
        genie.forward(ln)
        genie.right(120)


def draw_circle(r):
    jamie = init_turtle("square","blue",6)
    jamie.circle(r)
    
draw_square(50)
draw_triangle(100)
draw_circle(150)
