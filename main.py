import tkinter as tk
import math
import string
from turtle import TurtleScreen, RawTurtle

# Create the main tkinter window
root = tk.Tk()
root.title("Computational & Graphing tool for General Sinus")
root.geometry("960x700")

# Disable window resizing
root.resizable(False, False)

# Create a canvas to draw the turtle graphics
canvas = tk.Canvas(root, width=700, height=700)
canvas.place(x=260, y=0)

# Create a frame for the GUI elements
frame = tk.Frame(root, width=260, height=700)
frame.place(x=0, y=0)

# Create another frame within the main frame
frame2 = tk.Frame(frame, width=250, height=370)
frame2.place(x=5, y=50)

# Create the turtle screen and turtle objects
screen = TurtleScreen(canvas)
screen.setworldcoordinates(-2, -2, 2, 2)  # around the unit circle
screen.tracer(0)

turtle = RawTurtle(screen)
turtle.hideturtle()

# Define a Point class to store the x and y coordinates of a point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Create lists to store the GUI elements and points
checkboxes = []
checkbox_vars = []
labels = []
labels2 = []
entries1 = []
entries2 = []
points = []
checkbox_point_map = {}
select_all_var = tk.IntVar()
color_labels = []
letter_labels = []

# Function to select/deselect all checkboxes
def select_all():
    for checkbox_var in checkbox_vars:
        checkbox_var.set(select_all_var.get())

# Create a "Select All" checkbox
select_all_checkbox = tk.Checkbutton(frame, text="Select All", variable=select_all_var, command=select_all)
select_all_checkbox.place(x=10, y=40)

# Function to draw the grid lines along the x-axis
def grid_x():
    screen.tracer(0) # disable updating
    turtle.speed("fastest")
    turtle.penup()
    turtle.width(0.05)

    # Draw horizontal lines
    turtle.color("#F2F2F2")
    for n in range(1, 50):
        turtle.penup()
        turtle.goto(-2.5, -0.04 * n)
        turtle.pendown()
        turtle.forward(5)
        turtle.penup()
        turtle.goto(-2.5, 0.04 * n)
        turtle.pendown()
        turtle.forward(5)

    turtle.color("#D3D3D3")
    for i in range(1, 50):
        turtle.penup()
        turtle.goto(-2.5, 0.2 * i)
        turtle.pendown()
        turtle.forward(5)
        turtle.penup()
        turtle.goto(-2.5, -0.2 * i)
        turtle.pendown()
        turtle.forward(5)

    screen.update()

# Function to draw the x-axis line
def x_axis():
    turtle.penup()
    turtle.width(1.5)
    turtle.color('black')
    # X Axis Real
    turtle.penup()
    turtle.goto(-2.5, 0)
    turtle.pendown()
    turtle.forward(4.49)
    turtle.penup()
    turtle.stamp()

# Function to draw the unit circle
def draw_circle():
    screen.tracer(0)
    # Circle
    turtle.width(0.5)
    turtle.penup()
    turtle.goto(0, -1)
    turtle.color('#808080')
    turtle.setheading(0)
    turtle.speed("fastest")
    turtle.pendown()

    for _ in range(72):
        turtle.pendown()
        turtle.circle(1, 360 / 144)
        turtle.penup()
        turtle.circle(1, 360 / 144)

    turtle.penup()
    screen.update()

# Function to delete selected points
def delete_selected_fields():
    indices_to_delete = []
    for i, checkbox_var in enumerate(checkbox_vars):
        if checkbox_var.get() == 1:
            indices_to_delete.append(i)

    for index in reversed(indices_to_delete):
        checkbox = checkboxes[index]
        checkbox.destroy()
        labels[index].destroy()
        labels2[index].destroy()
        entries1[index].destroy()
        entries2[index].destroy()
        color_labels[index].destroy()
        letter_labels[index].destroy()

        checkboxes.pop(index)
        labels.pop(index)
        labels2.pop(index)
        entries1.pop(index)
        entries2.pop(index)
        checkbox_vars.pop(index)
        point = points.pop(index)
        color_labels.pop(index)
        letter_labels.pop(index)

        # Remove the checkbox from checkbox_point_map
        for cb, pt in checkbox_point_map.items():
            if pt == point:
                checkbox_point_map.pop(cb)
                break

    # Reset the state of the select_all_var based on the remaining checkboxes
    select_all_var.set(1 if all(var.get() == 1 for var in checkbox_vars) else 0)

# Function to add input fields for points
def add_fields():
    index = len(labels) + 1
    colors = ["deepskyblue", "tomato", "limegreen", "hotpink", "salmon",
              "dodgerblue", "slategray", "steelblue", "goldenrod", "mediumseagreen",
              "coral", "skyblue", "plum", "wheat", "lightyellow"]

    names = string.ascii_uppercase
    checkbox_var = tk.IntVar()
    new_checkbox = tk.Checkbutton(frame2, variable=checkbox_var)
    new_checkbox.place(x=5, y=index * 30)
    checkboxes.append(new_checkbox)
    checkbox_vars.append(checkbox_var)

    new_label1 = tk.Label(frame2, text="x" + str(index) + "=", width=10)
    new_label1.place(x=25, y=index * 30)
    labels.append(new_label1)

    new_entry1 = tk.Entry(frame2, width=10)
    new_entry1.place(x=75, y=index * 30)
    entries1.append(new_entry1)

    new_label2 = tk.Label(frame2, text="y" + str(index) + "=", width=10)
    new_label2.place(x=115, y=index * 30)
    labels2.append(new_label2)

    new_entry2 = tk.Entry(frame2, width=8)
    new_entry2.place(x=165, y=index * 30)
    entries2.append(new_entry2)

    color_index = (index - 1) % len(colors)
    color = colors[color_index]

    name_index = (index - 1) % len(names)
    name = names[name_index]

    color_label = tk.Label(frame2, text="•", foreground=color, font=("roboto", 20))
    color_label.place(x=215, y=index * 29)

    letter_label = tk.Label(frame2, text=name, foreground=color, font=("roboto", 9))
    letter_label.place(x=229, y=index * 29)
    letter_labels.append(letter_label)

    point = Point(0, 0)  # Create a placeholder point
    points.append(point)
    color_labels.append(color_label)

# Function to draw points
def draw_points():
    # calling again the turtle screen and turtle objects for draw x_axis after the grid_y
    screen = TurtleScreen(canvas)
    screen.setworldcoordinates(-2, -2, 2, 2) # around the unit circle
    screen.tracer(0)
    
    turtle = RawTurtle(screen)
    selected_points = []

    select_all_var.set(1 if all(var.get() == 1 for var in checkbox_vars) else 0)

    for checkbox_var, entry1, entry2 in zip(checkbox_vars, entries1, entries2):
        if checkbox_var.get() == 1:
            try:
                x_value = float(entry1.get())
                y_value = float(entry2.get())
                selected_points.append((x_value, y_value))
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    if selected_points:
        grid_x()
        draw_circle()
        print("Selected Points:")
        for index, point in enumerate(selected_points, 1):
            print(f"Point {index}: ({point[0]}, {point[1]})")
            x = point[0]
            y = point[1]
            if radio_var.get() == 1:
                D_x = math.radians(x)
                D_y = math.radians(y)
                D_xy = math.radians(x + y)
            if radio_var.get() == 2:
                D_x = x
                D_y = y
                D_xy = x + y
            sinxy = (float(math.sin(D_x)) / float(math.sin(D_xy)))
            cosxy = (float(math.sin(D_y)) / float(math.sin(D_xy)))

            def grid_y():
                turtle.color("#f2f2f2")
                for n in range(1, 500):
                    turtle.penup()
                    turtle.goto(0.04 * n, 0)
                    turtle.setheading(180 + x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(0.04 * n, 0)
                    turtle.setheading(x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(-0.04 * n, 0)
                    turtle.setheading(180 + x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(-0.04 * n, 0)
                    turtle.setheading(x + y)
                    turtle.pendown()
                    turtle.forward(15)

                turtle.color('#d3d3d3')
                for i in range(1, 100):
                    turtle.penup()
                    turtle.goto(0.2 * i, 0)
                    turtle.setheading(180 + x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(0.2 * i, 0)
                    turtle.setheading(x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(-0.2 * i, 0)
                    turtle.setheading(180 + x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()
                    turtle.goto(-0.2 * i, 0)
                    turtle.setheading(x + y)
                    turtle.pendown()
                    turtle.forward(15)
                    turtle.penup()

            turtle.penup()
            turtle.width(1.5)
            turtle.color('black')
            turtle.goto(0, 0)
            turtle.setheading(180 + x + y)
            turtle.pendown()
            turtle.forward(2.5)
            turtle.penup()
            turtle.goto(0, 0)
            turtle.setheading(x + y)
            turtle.pendown()
            turtle.forward(2.5)
            turtle.penup()
            turtle.width(0.2)

            if len(selected_points) == 1:
                grid_y()
            elif len(selected_points) > 1:
                sums = set()
                is_same_sum = True
                for i in range(len(selected_points) - 1):
                    sum1 = selected_points[i][0] + selected_points[i][1]
                    sum2 = selected_points[i + 1][0] + selected_points[i + 1][1]
                    if sum1 != sum2:
                        is_same_sum = False
                        break
                if is_same_sum:
                    grid_y()

            # Call the drawing functions here
            turtle.goto(0, 0)
            x_axis()
            turtle.penup()
            turtle.width(0.5)
            turtle.color("black")
            # Angle
            turtle.home()
            turtle.setheading(x)
            turtle.penup()
            turtle.forward(1)
            turtle.pendown()
            turtle.home()
            turtle.penup()
            # Draw Sin axis
            turtle.width(2)
            turtle.penup()
            turtle.color('blue')
            turtle.goto(0, 0)
            turtle.setheading(x)
            turtle.forward(1)
            turtle.setheading(180 + x + y)
            turtle.pendown()
            turtle.forward(sinxy)
            turtle.dot(6)
            # Draw Cos axis
            turtle.penup()
            turtle.color('Green')
            turtle.home()
            turtle.goto(0, 0)
            turtle.setheading(x)
            turtle.forward(1)
            turtle.setheading(180)
            turtle.pendown()
            turtle.forward(cosxy)
            turtle.dot(6)
            turtle.penup()
            turtle.goto(0, 0)

            x0, y0 = turtle.position()
            names = string.ascii_uppercase
            colors = ["deepskyblue", "tomato", "limegreen", "hotpink", "salmon",
                      "dodgerblue", "slategray", "steelblue", "goldenrod", "mediumseagreen",
                      "coral", "skyblue", "plum", "wheat", "lightyellow"]

            for entry1, name, color in zip(entries1, names, colors):
                try:
                    p = float(entry1.get())  # Convert the entry value to float
                    if radio_var.get() == 1:
                        angle = math.radians(p)  # Convert angle x to radians                  
                    if radio_var.get() == 2:
                        angle = p
                    distance = 1  # Set the distance from the original point
                    x1 = x0 + distance * math.cos(angle)
                    y1 = y0 + distance * math.sin(angle)
                    turtle.color(color)
                    turtle.goto(0, 0)
                    turtle.penup()
                    turtle.goto(x1, y1)  # Set the coordinates where you want to draw the point
                    turtle.pendown()
                    turtle.dot(5)  # Draw a dot with a size of 5 pixels
                    turtle.write(f"Point {name}", align="left", font=("Arial", 8))
                    turtle.penup()
                except ValueError:
                    print("Invalid input. Please enter numeric values.")

select_all_var.set(0)

# Function to calculate trigonometric values
def calcule():
    entry_sin.delete(0, tk.END)
    entry_cos.delete(0, tk.END)
    entry_tan.delete(0, tk.END)
    selected_points = []

    for checkbox_var, entry1, entry2 in zip(checkbox_vars, entries1, entries2):
        if checkbox_var.get() == 1:
            try:
                x_value = float(entry1.get())
                y_value = float(entry2.get())
                selected_points.append((x_value, y_value))
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    if selected_points:
        print("Selected Points:")
        for index, point in enumerate(selected_points, 1):
            print(f"Point {index}: ({point[0]}, {point[1]})")
            x = point[0]
            y = point[1]
            if radio_var.get() == 1:
                D_x = math.radians(x)
                D_y = math.radians(y)
                D_xy = math.radians(x + y)
            if radio_var.get() == 2:
                D_x = x
                D_y = y
                D_xy = x + y

            sinxy = (float(math.sin(D_x)) / float(math.sin(D_xy)))
            entry_sin.insert(tk.END, sinxy)
            cosxy = (float(math.sin(D_y)) / float(math.sin(D_xy)))
            entry_cos.insert(tk.END, cosxy)
            tanxy = (float(math.sin(D_x)) / float(math.sin(D_y)))
            entry_tan.insert(tk.END, tanxy)

# Function to clear the result fields
def clear():
    entry_sin.delete(0, tk.END)
    entry_cos.delete(0, tk.END)
    entry_tan.delete(0, tk.END)

# Create a button to calculate the trigonometric values
button = tk.Button(master=frame, text="Calculate", width=25, command=calcule)
button.place(x=40, y=490)

# Create labels and entry fields for displaying the trigonometric values
label_sin = tk.Label(master=frame, text="Sin =", font=("Roboto", 11))
label_sin.place(x=40, y=540)

entry_sin = tk.Entry(master=frame, width=20, font=("Roboto", 8))
entry_sin.place(x=90, y=543)

label_cos = tk.Label(master=frame, text="Cos =", font=("Roboto", 11))
label_cos.place(x=40, y=570)

entry_cos = tk.Entry(master=frame, width=20, font=("Roboto", 8))
entry_cos.place(x=90, y=573)

label_tan = tk.Label(master=frame, text="Tan =", font=("Roboto", 11))
label_tan.place(x=40, y=600)

entry_tan = tk.Entry(master=frame, width=20, font=("Roboto", 8))
entry_tan.place(x=90, y=603)

# Create the "Clear" button
clear_button = tk.Button(frame, text="Clear", width=25, command=clear)
clear_button.place(x=40, y=640)

# Create the "Add" button
add_button = tk.Button(frame, text="Add", command=add_fields)
add_button.place(x=10, y=10)

# Create the "Delete Selected" button
delete_button = tk.Button(frame, text="Delete Selected", command=delete_selected_fields)
delete_button.place(x=150, y=10)

radio_var = tk.IntVar()
radio_var.set(1)
radiobutton_1 = tk.Radiobutton(master=frame, text="Degree", variable=radio_var, value=1, font=("Roboto", 10))
radiobutton_2 = tk.Radiobutton(master=frame, text="Radian", variable=radio_var, value=2, font=("Roboto", 10))
radiobutton_1.place(x=50, y=460)
radiobutton_2.place(x=130, y=460)

draw_button = tk.Button(frame, text="Draw Points", command=draw_points)
draw_button.place(x=60, y=10)

screen.update()
root.mainloop()
