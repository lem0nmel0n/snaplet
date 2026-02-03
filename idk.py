from tkinter import *


def mouse_click(event):
    global mouse_x, mouse_y, rect_id
    if not mouse_x:
        mouse_x, mouse_y = event.x, event.y

        rect_id = canvas.create_rectangle(
        mouse_x, mouse_y,
        event.x, event.y,
        outline="white", 
        width=2,
        dash=(5, 2))
        

def mouse_drag(event):
    global mouse_x, mouse_y, rect_id
    if rect_id:
        canvas.coords(rect_id,
            mouse_x, mouse_y,
            event.x, event.y,
            )

def cancel(event):
    global result
    root.destroy()
    result = None

def mouse_release(event):
    global mouse_x, mouse_y, result
    if not rect_id:
        result = None
    else:
        result = mouse_x, mouse_y, event.x, event.y
    root.destroy()
    

def main():
    global mouse_x, mouse_y, canvas, root, result, rect_id
    rect_id = None
    result = None
    root = Tk()
    canvas = Canvas(
        master=root,
        relief=SUNKEN)
    canvas.configure(bg="black")
    root.configure(cursor="plus")

    mouse_x = mouse_y = None

    root.bind("<Escape>", cancel)
    canvas.bind("<B1-Motion>", mouse_drag)
    canvas.bind("<Button-1>", mouse_click)
    thing = canvas.bind("<ButtonRelease-1>", mouse_release)

    root.attributes("-alpha", 0.5)
    root.attributes("-fullscreen", True)


    canvas.pack(fill="both", expand=True)
    canvas.focus_set()
    mainloop()

    return result
