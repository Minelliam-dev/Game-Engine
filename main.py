import random as r
from tkinter import Tk
import tkinter as tk
import time, os, platform, string, pygame, numpy

class terminal:
    def clear():
        if platform.system() == "Windows":
            os.system("cls")
        else:
           os.system("clear")

    def color_print(color, text):
        if (color == "red"): print('\033[31m' + str(text) + '\033[0m')
        if (color == "green"): print('\033[32m' + str(text) + '\033[0m')
        if (color == "blue"): print('\033[34m' + str(text) + '\033[0m')
        if (color == "normal"): print('\033[0m' + str(text) + '\033[0m')
        if (color == "yellow"): print('\033[33m' + str(text) + '\033[0m')
        if (color == "purple"): print('\033[35m' + str(text) + '\033[0m')
        if (color == "cyan"): print('\033[36m' + str(text) + '\033[0m')
        if (color == "gray"): print('\033[30m' + str(text) + '\033[0m')

class gui:
    def label(text, Window, backgroundColor=None, foregroundColor="black", x=0, y=0):
        kwargs = {"text": text, "foreground": foregroundColor}
        if backgroundColor is not None:
            kwargs["background"] = backgroundColor
    
        label = tk.Label(Window, **kwargs, anchor="nw")
        label.place(x=x, y=y)
    
        return label

    def button(text, x, y, function, Window, theme):
        if theme == "light":
            button = tk.Button(Window, text=text, command=function, anchor="center")
        if theme == "dark":
            button = tk.Button(Window, text=text, command=function, anchor="center", fg="darkgray", bg="black")

        button.place(x=x, y=y)
        return button

    def pack(asset):
        asset.pack()

    def SetButtonSize(Button, height, width):
        Button.config(height=height, width=width)
    
    def SetLabelText(Label, new_text):
        Label.config(text=new_text)
    
    def SetButtonFunction(Button, function):
        Button.config(command=function)

class window:
    def changeIcon(Window, ico_File):
        Window.iconbitmap(ico_File)
    
    def getFPS(prev=[None]):
        now = time.perf_counter()
        if prev[0] is None:
            prev[0] = now
            return 0
        delta = now - prev[0]
        prev[0] = now
        if delta == 0:
            return 0
        return 1 / delta
    
    def new_window(height, width, name):
        window_size = str(width) + "x" + str(height)
        window = Tk()
        window.title(name)
        window.geometry(window_size)
        return window

    def set_cursor(new_cursor, Window):
        window = Window
        window.config(cursor=new_cursor)

    def close(Window):
        Window.destroy()

    def update(Window):
        Window.update()

    def mainloop(Window):
        Window.mainloop()
    
    def HideTitleBar(Window, boolean):
        Window.overrideredirect(boolean)
    
    def AllowResize(Window, boolean):
        Window.resizable(width=boolean, height=boolean)
    
    def CursorVisible(Window, boolean):
        if boolean:
            Window.config(cursor="")
        else:
            Window.config(cursor="none")

    def Fullscreen(Window, boolean):
        Window.overrideredirect(False)
        Window.attributes('-fullscreen', boolean)
        Window.overrideredirect(True)

class device:
    def cpu_cores():
        return os.cpu_count()
    def plattform():
        return platform.system()

class Mouse:
    def __init__(self, window):
        self.x = 0
        self.y = 0
        window.bind("<Motion>", self.mouse_move)

    def mouse_move(self, event):
        self.x = event.x
        self.y = event.y

    def get_X(self):
        return self.x

    def get_Y(self):
        return self.y

class input:
    def key(window, key, function):
        window.bind(f"<KeyPress-{key}>", function)

class Canvas:
    def create_canvas(width, height, Background, window, x, y):
        canvas = tk.Canvas(window, width=width, height=height, bg=Background)
        gui.pack(canvas)
        img = tk.PhotoImage(width=width, height=height)
        canvas.create_image((width / 2, height / 2), image=img, state="normal")
        canvas.place(x=x, y=y)
        return img
    
    def draw_pixel(x, y, hex_color, canvas, pixel_size):
        x = x * pixel_size
        y = y * pixel_size
        if pixel_size == 1:
            canvas.put(hex_color, (x, y))
        else:
            canvas.put(hex_color, to=(x, y, (x + pixel_size), (y + pixel_size)))

    def line(a_x, a_y, b_x, b_y, canvas, hex_color, pixel_size, grid_size):
        pass

    def get_pixel(x, y, canvas, grid_size):
        x *= grid_size
        y *= grid_size
        return canvas.get(x, y)

class random:
    def Randomint(a, b):
        return r.randint(a, b)

    def Randomfloat(a, b):
        number = r.randint(a * 1000, b * 1000)
        number /= 1000
        return number

    def HEX_color():
        color = f"#{r.randint(0,255):02x}{r.randint(0,255):02x}{r.randint(0,255):02x}"
        return color
    
    def Screen(GRID_SIZE, PIXEL_SIZE, Window):
        for t in range(GRID_SIZE):
            for i in range(GRID_SIZE):
                color = f"#{r.randint(0,255):02x}{r.randint(0,255):02x}{r.randint(0,255):02x}"
                x = (i)
                y = (t)
                Canvas.draw_pixel(x, y, color, canvas, PIXEL_SIZE)
        window.update(Window)
        
    def Letter(amount):
        result = ""
        for i in range(amount):
            result = (result + r.choice(string.ascii_letters))
        return result

class sound:
    _loaded_sounds = {}


    def play(file, volume=1.0, loop=False):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        if file not in sound._loaded_sounds:
            sound._loaded_sounds[file] = pygame.mixer.Sound(file)

        snd = sound._loaded_sounds[file]

        volume = max(0, min(1, volume))
        snd.set_volume(volume)
        
        loops = -1 if loop else 0
        snd.play(loops=loops)

    def StopAll():
        if pygame.mixer.get_init():
            pygame.mixer.stop()

# Example usage
terminal.clear()
terminal.color_print("red", "red")
terminal.color_print("green", "green")
terminal.color_print("blue", "blue")
terminal.color_print("normal", "white")
terminal.color_print("yellow", "yellow")
terminal.color_print("purple", "purple")
terminal.color_print("cyan", "cyan")
terminal.color_print("gray", random.Letter(50))
terminal.color_print("blue", str(random.Randomfloat(0, 1)))

window_name = window.new_window(500, 500, "test")
label1 = gui.label("test", window_name, None, "green", 1, 1)
gui.pack(label1)

canvas = Canvas.create_canvas(500, 500, "#000000", window_name, -2, 0)
Canvas.draw_pixel(9, 9, "#ff0000", canvas, 50)
Canvas.draw_pixel(0, 0, "#ff0000", canvas, 50)
window.set_cursor("cross", window_name)
window_name.config()

mouse = Mouse(window_name)

print_FPS = True
print_mouseX = False

def test(event): print("test")

def kill(event): window.close(window_name)

def set_text(event): gui.SetLabelText(label1, "testtttttt")

button2 = gui.button("test", 0, 100, lambda: print("test"), window_name, "dark")
button3 = gui.button("close", 0, 0, lambda: window.close(window_name), window_name, "light")
button4 = gui.button("set label", 0, 50, lambda: gui.SetLabelText(label1, "testing the changing of label text"), window_name, "light")
button5 = gui.button("change button defenition", 0, 150, lambda: gui.SetButtonFunction(button4, gui.SetLabelText(label1, "testing the changing of label text for the second time")), window_name, "light")
button6 = gui.button("play sound", 50, 100, lambda: sound.play("sound.wav", 1, False), window_name, "dark")
button7 = gui.button("stop sound", 50, 150, lambda: sound.StopAll(), window_name, "dark")

gui.SetButtonSize(button3, 0, 10)

#window.changeIcon(window_name, "icon.ico")
window.HideTitleBar(window_name, True)
window.CursorVisible(window_name, True)
window.AllowResize(window_name, False)
window.Fullscreen(window_name, False)

print(device.cpu_cores())
print(device.plattform())

while True:
    window.update(window_name)
    #Canvas.draw_pixel(0, 0, random.HEX_color(), canvas, 50)
    random.Screen(10, 50, window_name)
    if print_mouseX == True:
        mouse_X = mouse.get_X()
        print(mouse_X)
    input.key(window_name, "w", kill)
    if print_FPS == True:
        print(window.getFPS())
