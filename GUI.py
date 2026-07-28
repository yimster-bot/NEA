import tkinter as tk

def on_canvas_click(event):
    x, y = event.x, event.y
    canvas.create_oval(x-5, y-5, x+5, y+5, fill='red', outline='red')
    print(f'Clicked at: {x}, {y}')

# def show_screen1():
#     screen2_frame.pack_forget()
#     screen1_frame.pack(fill='both', expand=True)
#
# def show_screen2():
#     screen1_frame.pack_forget()
#     screen2_frame.pack(fill = 'both', expand=True)

root = tk.Tk()
root.title('TRIAL')
root.configure(background='yellow')
root.minsize(200,200)
root.maxsize(1500,1500)
root.geometry('1200x1200+50+50')

container = tk.Frame(root, bg='yellow')
container.pack(fill='both', expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

screen1 = tk.Frame(container, bg='yellow')
screen1.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
img1 = tk.PhotoImage(file='Screenshot 2026-07-27 at 19.22.29.png')
img_label = tk.Label(screen1, image=img1)
img_label.grid(row=1, column=0, sticky='nw', padx=10, pady=10)

text = tk.Label(screen1, text='wsg homie', fg='black', bg='yellow')
text.grid(row=0, column=0, stick='nw', padx=10, pady=10)

entry = tk.Entry(screen1, bg='white', fg='red')
entry.grid(row=2, column=0, stick='w', padx=10, pady=5)

btn = tk.Button(screen1, text='Change screen', command = lambda: screen2.tkraise())
btn.grid(row=3, column=0, sticky='w', pady=10, padx=5)

canvas = tk.Canvas(screen1, width=400, height=400, bg='green')
canvas.grid(row=1, column=1, sticky='w', padx=10, pady=10)
canvas.create_oval(185, 185, 215, 215, outline='white', width=2)
canvas.create_rectangle(50, 50, 350, 350, outline='white', width=3)
canvas.bind('<Button-1>', on_canvas_click)

screen2 = tk.Frame(container, bg='yellow')
screen2.grid(row=0, column=0, sticky='nsew')

img2 = tk.PhotoImage(file='Screenshot 2026-07-28 at 16.30.43.png')
img2_label = tk.Label(screen2, image=img2, bg='yellow')
img2_label.pack(padx=20, pady=20)

back_btn = tk.Button(screen2, text='Back', command = lambda: screen1.tkraise())
back_btn.pack(padx=20, pady=10)

screen1.tkraise()
root.mainloop()
