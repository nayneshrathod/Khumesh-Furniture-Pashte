'''
from django.contrib.auth.models import User
from blogs.models import post
from extapp.models import extenduser

s = User.objects.get(username='Nano')
d = post.objects.create(post_writer=s, post_title='This is a Post Title', post_description='this is a post Discription',
                        post_publish_status=True)
d.save

d1 = post.objects.create(post_writer=s, post_title='This is a Post Title',
                         post_description='this is a post Discription by Naynesh', post_publish_status=True)
d1.save

s1 = User.objects.get(username='Koli')
b = post.objects.create(post_writer=s1, post_title='This is a Post Title by Koli',
                        post_description='this is a post Discription by Koli', post_publish_status=True)
b.save

b1 = post.objects.create(post_writer=s1, post_title='This is a Post Title by Koli',
                         post_description='this is a post Discription by Koli', post_publish_status=False)
b1.save

data = extenduser.objects.all()
dataa = data[0:3]

data1 = extenduser.objects.get(user=2)
print(data1.profile_pic)

# dataa = User.objects.filter(id=request.user.id)
# data = extenduser.objects.all()
# dataa = data[0:3]

# print(dataa)
# print(dataa.get(id=request.user.id))
#
# datac = extenduser.objects.get(user__username=dataa.get(id=request.user.id))
# print(str(datac))
'''

'''

import turtle
x = turtle.Turtle()
for i in range(5):
    x.fd(100)
    x.rt(144)
'''
'''
import turtle
colors = ['orange','orange','orange','white','white','white','green','green','green']
# colors = ['red','yellow','pink','purple','green','blue','orange']
t = turtle.Pen()
turtle.bgcolor('black')
for x in range(200):
    t.pencolor(colors[x%9])
    # t.pencolor(colors[x%6])
    t.width(x/100+1)
    t.forward(x)
    t.left(39)
    # t.left(59)
'''
''' 
import turtle
# wn = turtle.Screen()
turtle.bgcolor('black')
# turtle.shape('turtle')
# colors = ['orange', 'white','green','green','white','orange']
# colors = ['orange','orange', 'white', 'white','green','green','green','green','white','white','orange','orange']
colors = ['blue','orange', 'white', 'green','green','black','black','green','green','white','orange','Blue']
tr = turtle.Turtle()
# move = 1
# tr.speed("fastest")
# for j in range(1):
for i in range(30):
    tr.pu()
    print(i)
    tr.goto(0,0)
    tr.pd()
    tr.pensize(2)
    # tr.color('Red')
    # tr.circle(90,steps=7)
    # tr.color('Orange')
    # tr.circle(75,steps=6)
    # tr.color('Yellow')
    # tr.circle(60,steps=5)
    # tr.color('Green')
    # tr.circle(45,steps=4)
    # tr.color('Blue')
    # tr.circle(30,steps=3)
    # tr.color('Indigo')
    # tr.circle(15,steps=2)
    # tr.color(colors[i % 6])
    # tr.pencolor(colors[i % 6])
    my_num_sides = 12
    my_side_length = 60
    my_angle = 360.0 / my_num_sides
    for i in range(my_num_sides):
        tr.color(colors[i % 12])
        # tr.color(colors[i % 9])
        tr.forward(my_side_length)
        tr.right(my_angle)
    # tr.circle(60,steps=11)
    tr.right(12)

turtle.done()




import turtle
turtle.bgcolor("green")
draw = turtle.Turtle()
draw.speed(1000000)
draw.hideturtle()
draw.pensize(3)
draw.color("white")

def Board (a, x, y, size):
    draw.pu()
    draw.goto(x, y)
    draw.pd()
    for i in range (0, 4):
        draw.forward(size)
        draw.right(90)

x =-40
y = -40
size = 40
for i in range (0, 10):
    for j in range (0, 10):
         Board (draw, x + j*size, y + i*size, size)

turtle.done()
'''

'''
import turtle
turtle.bgcolor('black')
colors = ['orange', 'white','green','green','white','orange']
tr = turtle.Turtle()
for i in range(30):
    tr.pu()
    print(tr.pd())
    tr.goto(0,0)
    tr.pd()
    tr.pensize(1)
    my_num_sides = 6
    my_side_length = 120
    my_angle = 360.0 / my_num_sides
    for i in range(my_num_sides):
        tr.color(colors[i % 6])
        tr.forward(my_side_length)
        tr.right(my_angle)
    tr.right(12)

turtle.done()
'''

import turtle as t

co = ['orange', 'green', 'red', 'blue']
S = t.Screen()
# t.shape("circle")
for i in range(75):
    t.pensize(len(co[i % 4]))
    t.pencolor(co[i % 4])
    t.speed(3)
    t.forward(i * 5 + 1)
    t.speed(5)
    t.back(i * 3 - 10)
    t.left(90)
    t.speed(8)
    # t.forward(i * 9 + 1)
    # t.left(90)
    # if i == 60:
    #     t.goto(i + 10, i + 10)
    #     t.pencolor(co[i % 3])
    #     t.forward(i * 7 + 1)
    #     t.left(120)

t.done()
