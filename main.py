import random as r
from tkinter import Tk, ttk
import tkinter as tk
import time, os, platform, string, subprocess, threading, wave
from PIL import Image, ImageTk, ImageFilter

class console:
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
    
    def slider(Window, x, y, max_value, min_value, orientation="horizontal"):
        cale2 = ttk.Scale(Window, from_=min_value, to=max_value, orient=orientation, style="")
        cale2.place(x=x, y=y)
        return cale2

    def sliderValue(slider):
        return int(slider.get())
    
    def disableSlider(slider, boolean=True):
        if boolean:
            slider['state'] = 'disabled'
        else:
            slider['state'] = 'normal'

    def setSlider(slider, value):
        variable2 = tk.IntVar(value = value)
        slider.config(variable=variable2)

    def sliderStyle(slider, bg, fg, is_slider_vertical=False):
        style = ttk.Style()
        style.configure("TScale", background=bg, fg=fg, handle="#ffffff")
        slider.config(style="TScale")
        slider.pack()

class window:
    def changeIcon(Window, ico_File):
        try:
            Window.iconbitmap(ico_File)
        except:
            print("could not load icon, maybe check its name and location ?")
    
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

    def Title(Window, title):
        Window.title(title)

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

    def get_pixel(x, y, canvas, grid_size):
        x *= grid_size
        y *= grid_size
        return canvas.get(x, y)

    def LoadImage(path, x, y, width, height, window):
        try:
            img = Image.open(path)

            scale_factor = 4
            img = img.resize(
                (img.width * scale_factor, img.height * scale_factor),
                Image.NEAREST
            )

            img = img.resize(
                (width, height),
                Image.BOX
            )

            img_tk = ImageTk.PhotoImage(img, master=window)

            panel = tk.Label(window, image=img_tk, bd=0, highlightthickness=0)
            panel.image = img_tk
            panel.place(x=x, y=y)
            return panel

        except Exception as e:
            print("Error:", e)
            print("Please confirm the file is a .png or .jpg and the path is correct.")

    def ChangeIMGPos(object, newX, newY):
        object.place(x=newX, y=newY)
    
    def getImgPosX(img):
        return img.winfo_x()
    
    def getImgPosY(img):
        return img.winfo_y()

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
    _active_processes = []
    _converted_cache = {}

    @staticmethod
    def _is_pcm_wav(filepath):
        try:
            with wave.open(filepath, "rb") as w:
                return w.getsampwidth() == 2 and w.getcomptype() == "NONE"
        except:
            return False
        
    @staticmethod
    def _convert_to_pcm(input_file):

        if input_file in sound._converted_cache:
            return sound._converted_cache[input_file]

        base, ext = os.path.splitext(input_file)
        output_file = base + "_pcm.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            output_file
        ]

        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            sound._converted_cache[input_file] = output_file
            return output_file
        except FileNotFoundError:
            print("[ERROR] FFmpeg is not installed. Cannot convert WAV.")
            return None
        except subprocess.CalledProcessError as e:
            print("[FFmpeg Conversion Error]")
            print(e.stderr.decode())
            return None

    @staticmethod
    def _prepare_file(file):
        if platform.system() == "Windows":
            if not sound._is_pcm_wav(file):
                print("[INFO] Converting WAV to PCM for Windows...")
                converted = sound._convert_to_pcm(file)
                if converted:
                    return converted
        return file

    @staticmethod
    def _play_once(file):
        system = platform.system()
        file = sound._prepare_file(file)

        if system == "Darwin":
            return subprocess.Popen(["afplay", file])

        elif system == "Linux":
            try:
                return subprocess.Popen(["aplay", file])
            except FileNotFoundError:
                return subprocess.Popen(["paplay", file])

        elif system == "Windows":
            import winsound
            winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return None

    @staticmethod
    def play(file, loop=False):
        def loop_play():
            while True:
                sound._play_once(file)

        if loop:
            t = threading.Thread(target=loop_play, daemon=True)
            t.start()
        else:
            p = sound._play_once(file)
            if p:
                sound._active_processes.append(p)

    @staticmethod
    def StopAll():
        for p in sound._active_processes:
            try:
                p.terminate()
            except:
                pass
        sound._active_processes.clear()

        if platform.system() == "Windows":
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)

# Example usage
console.clear()
console.color_print("red", "red")
console.color_print("green", "green")
console.color_print("blue", "blue")
console.color_print("normal", "white")
console.color_print("yellow", "yellow")
console.color_print("purple", "purple")
console.color_print("cyan", "cyan")
console.color_print("gray", random.Letter(50))
console.color_print("blue", str(random.Randomfloat(0, 1)))

window_name = window.new_window(500, 500, "test")
label1 = gui.label("test", window_name, None, "green", 1, 1)
label2 = gui.label("mouse", window_name, None, "black", 1, 1)
gui.pack(label1)

canvas = Canvas.create_canvas(500, 500, "#000000", window_name, -2, 0)
Canvas.draw_pixel(9, 9, "#ff0000", canvas, 50)
Canvas.draw_pixel(0, 0, "#ff0000", canvas, 50)
window.set_cursor("cross", window_name)

mouse = Mouse(window_name)

print_FPS = True
print_mouseX = True

def test(event): print("test")

def kill(event): window.close(window_name)

def set_text(event): gui.SetLabelText(label1, "testtttttt")

button2 = gui.button("test", 0, 100, lambda: print("test"), window_name, "dark")
button3 = gui.button("close", 0, 0, lambda: window.close(window_name), window_name, "light")
button4 = gui.button("set label", 0, 50, lambda: gui.SetLabelText(label1, "testing the changing of label text"), window_name, "light")
button5 = gui.button("change button defenition", 0, 150, lambda: gui.SetButtonFunction(button4, gui.SetLabelText(label1, "testing the changing of label text for the second time")), window_name, "light")
button6 = gui.button("play sound", 0, 200, lambda: sound.play("sound.wav", False), window_name, "dark")
button7 = gui.button("stop sound", 70, 200, lambda: sound.StopAll(), window_name, "dark")

gui.SetButtonSize(button3, 0, 10)


window.changeIcon(window_name, "icon.ico")

window.CursorVisible(window_name, True)
window.AllowResize(window_name, True)

button8 = gui.button("Fullscreen off", 100, 50, lambda: window.Fullscreen(window_name, False), window_name, "dark")
button9 = gui.button("Fullscreen on", 100, 100, lambda: window.Fullscreen(window_name, True), window_name, "dark")
button10 = gui.button("Hide Title Bar off", 200, 50, lambda: window.HideTitleBar(window_name, False), window_name, "dark")
button11 = gui.button("Hide Title Bar on", 200, 100, lambda: window.HideTitleBar(window_name, True), window_name, "dark")
button12 = gui.button("randomise screen", 200, 130, lambda: random.Screen(10, 50, window_name), window_name, "dark")

print(device.cpu_cores())
print(device.plattform())

slider = gui.slider(window_name, 0, 0, 100, 0, "horizontal")

gui.disableSlider(slider, False)
gui.setSlider(slider, 50)
gui.sliderStyle(slider, "#000000", "#ffffff", False)
gui.pack(slider)

img2 = Canvas.LoadImage("image.png", 0, 0, 200, 200, window_name)

while True:
    Canvas.ChangeIMGPos(img2, random.Randomint(0, 500), random.Randomint(0, 500))
    #gui.setSlider(slider, 50)
    #print(gui.sliderValue(slider))
    window.update(window_name)
    mouse_X = mouse.get_X()
    gui.SetLabelText(label2, str())
    label2.pack()
    input.key(window_name, "w", kill)
    window.Title(window_name, str(window.getFPS()))
