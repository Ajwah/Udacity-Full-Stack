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

    
def draw_fractal(ln):
    ben = init_turtle("triangle","black",10)
    def draw_koch(d,ln):
        if d > 0:
            draw_koch(d-1,ln/2)            
            ben.left(60)

            draw_koch(d-1,ln/2)
            ben.right(120)

            draw_koch(d-1,ln/2)
            ben.left(60)

            draw_koch(d-1,ln/2)
            
        else: ben.forward(ln)
    draw_koch(6,ln)
    
#draw_square(50)
#draw_triangle(100)
#draw_circle(150)
draw_fractal(100)
