import random as r
from tkinter import Tk, ttk
import tkinter as tk
import time, os, platform, string, subprocess, threading, wave, socket
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

class general_gui_functions:
    def increase_Z_order(object):
        try:
            object.lift()
        except:
            try:
                canvas.tag_raise(object)
            except:
                return

    def decrease_Z_order(object):
        try:
            object.lower()
        except:
            try:
                canvas.tag_lower(object)
            except:
                return

    def set_X(object, newX):
        object.place(x=newX)
    
    def set_Y(object, newY):
        object.place(y=newY)

    def Set_Pos(widget, newX, newY):
        try:
            widget.place_configure(x=newX, y=newY)
            widget.update_idletasks()  # forces a redraw to prevent ghosting
        except Exception as e:
            print("Error:", e)
            print("could not place the widget")

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
        elif theme == "dark":
            button = tk.Button(Window, text=text, command=function, anchor="center", fg="darkgray", bg="black")

        button.place(x=x, y=y)
        return button
     
    def pack(asset):
        asset.pack()
     
    def SetButtonSize(Button, height, width):
        Button.config(height=height, width=width)
    
    def ButtonStyle(button, fg=None, bg=None):
        if fg != None:
            button.config(fg=fg)
        if bg != None:
            button.config(bg=bg)

    def SetLabelText(Label, new_text):
        Label.config(text=new_text)
     
    def SetButtonFunction(Button, function):
        Button.config(state="disabled")
        Button.config(command=function)
        Button.config(state="normal")

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

    def disableButton(button, boolean=True):
        if boolean:
            button['state'] = 'disabled'
        else:
            button['state'] = 'normal'

    def setSlider(slider, value):
        variable2 = tk.IntVar(value = value)
        slider.config(variable=variable2)

    def sliderStyle(slider, bg, fg, is_slider_vertical=False):
        try:
            slider.configure(
                bg=bg,                 # widget background
                fg=fg,                 # text/ticks color (if shown)
                troughcolor=bg,        # the track color
                activebackground=fg,   # color when interacting (handle highlight)
                highlightthickness=0,
                orient=tk.VERTICAL if is_slider_vertical else tk.HORIZONTAL
            )
            return slider
        except:
            return


    def createTextInput(window, x, y, width, height, multi_line=False):
        if multi_line:
            text_box = tk.Text(window, height=height, width=width, )
            text_box.pack(pady=10)
            text_box.place(x=x, y=y)
            return text_box
        else:
            entry = tk.Entry(window, width=width)
            entry.pack(pady=10)
            entry.place(x=x, y=y)
            return entry

    def getTextInput(entity, has_multiple_lines):
        if has_multiple_lines == True:
            return entity.get("1.0", tk.END)
        if has_multiple_lines == False:
            return entity.get()

class device:
    def cpu_cores():
        return os.cpu_count()

    def plattform():
        return platform.system()

    def current_location():
        return os.path.abspath(__file__)

class Input:
    keys_held = set()
    callbacks = {}

    @staticmethod
    def bindKey(window, key, function, repeat_ms=16):
        """
        key: key name like "Escape", "space", "Left", "Control_L", "a", "Return"...
        function: function to run while key is held
        """

        # save callback
        Input.callbacks[key] = (function, repeat_ms)

        # global event bindings (press + release)
        window.bind("<KeyPress>", Input._on_press)
        window.bind("<KeyRelease>", Input._on_release)

        # Start loop once
        if not hasattr(Input, "_loop_started"):
            Input._loop_started = True
            Input._loop(window)

    @staticmethod
    def _on_press(event):
        Input.keys_held.add(event.keysym)

    @staticmethod
    def _on_release(event):
        if event.keysym in Input.keys_held:
            Input.keys_held.remove(event.keysym)

    @staticmethod
    def _loop(window):
        for key in list(Input.keys_held):
            if key in Input.callbacks:
                func, _ = Input.callbacks[key]
                func()

        window.after(16, lambda: Input._loop(window))

class window:
    # --- Path helper for window-related file paths (like icons) ---
    @staticmethod
    def _resolve_path(relative_path: str) -> str:
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, relative_path)

    def changeIcon(Window, ico_File):
        try:
            full_path = window._resolve_path(ico_File)
            Window.iconbitmap(full_path)
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
        window_obj = Window
        window_obj.config(cursor=new_cursor)

    def close(Window):
        Window.destroy()

    def update(Window):
        Window.update()

    def mainloop(Window):
        Window.mainloop()

    def after(Window, function):
        Window.after(1, function)
    
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

    def SetPosition(Window, x, y):
        Window.geometry(("+" + str(x) + "+" + str(y)))

    def getX(Window):
        return Window.winfo_x()
    
    def getY(Window):
        return Window.winfo_y()
    
    def setPosY(Window, y):
        Window.geometry(("+", str(window.getX(Window)), str(y)))
    
    def setPosX(Window, x):
        Window.geometry(("+", str(x)))

class Mouse:
    def __init__(self, window):
        self.x = 0
        self.y = 0
        window.bind("<Motion>", self.mouse_move)

    def mouse_move(self, event):
        root = event.widget.winfo_toplevel()
        self.x = event.x_root - root.winfo_rootx()
        self.y = event.y_root - root.winfo_rooty()

    def get_X(self):
        return self.x

    def get_Y(self):
        return self.y

    def bindMotion(window, function):
        window.bind("<Motion>", function)

    def bindClick(window, button, function, event_type="down"):
        # Map button names to Tkinter button numbers
        button_map = {
            "left": 1,
            "middle": 2,
            "right": 3,
            "side-1": 4,
            "side-2": 5
        }

        if button not in button_map:
            raise ValueError(f"Unknown button: {button}")

        if event_type == "down":
            event = f"<ButtonPress-{button_map[button]}>"
        elif event_type == "up":
            event = f"<ButtonRelease-{button_map[button]}>"
        else:
            raise ValueError("event_type must be 'down' or 'up'")

        window.bind(event, function)

    def getGlobalX(Window):
        mouse = Mouse(Window)

        globalMouseX = window.getX(Window) + Mouse.get_X(mouse)
        return globalMouseX
    
    def getGlobalY(Window):
        mouse = Mouse(Window)

        globalMouseY = window.getY(Window) + Mouse.get_Y(mouse)
        return globalMouseY

    def bindMouseWheel(widget, function_up=None, function_down=None):
        system = platform.system()
        def on_scroll(event):
            # Windows and macOS (Darwin)
            if system in ("Windows", "Darwin"):
                direction_up = event.delta > 0

            # Linux uses button 4 (up) and 5 (down)
            else:
                if event.num == 4:
                    direction_up = True
                elif event.num == 5:
                    direction_up = False
                else:
                    return  # Ignore other events

            # Call appropriate function
            if direction_up:
                if function_up:
                    function_up()
            else:
                if function_down:
                    function_down()

        # FIXED: must check explicitly using `in`
        if system in ("Windows", "Darwin"):
            widget.bind("<MouseWheel>", on_scroll)
        else:
            widget.bind("<Button-4>", on_scroll)  # Scroll up
            widget.bind("<Button-5>", on_scroll)  # Scroll down

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

    def Screen(GRID_SIZE, PIXEL_SIZE, canvas, Window):
        rand = random.Randomint # Local reference (faster)

        # Precompute coordinates to avoid repeated multiplication
        coords = [
            (x * PIXEL_SIZE, y * PIXEL_SIZE)
            for y in range(GRID_SIZE)
            for x in range(GRID_SIZE)
        ]

        for (x2, y2) in coords:
            r = rand(0, 255)
            g = rand(0, 255)
            b = rand(0, 255)

            # Fast hex color
            color = f"#{r:02x}{g:02x}{b:02x}"

            # Put pixel block
            canvas.put(color, to=(x2, y2, x2 + PIXEL_SIZE, y2 + PIXEL_SIZE))

    def Letter(amount):
        result = ""
        for i in range(amount):
            result = (result + r.choice(string.ascii_letters))
        return result

class sound:
    _active_processes = []
    _converted_cache = {}

    # --- Path helper (same style as image & window) ---
    @staticmethod
     
    def _resolve_path(relative_path: str) -> str:
        """Return absolute path relative to this file."""
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, relative_path)

    # --- WAV validation ---
    @staticmethod
     
    def _is_pcm_wav(filepath):
        try:
            with wave.open(filepath, "rb") as w:
                return w.getsampwidth() == 2 and w.getcomptype() == "NONE"
        except:
            return False

    # --- Convert WAV to PCM for Windows ---
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

    # --- Ensure correct format (Windows) ---
    @staticmethod
     
    def _prepare_file(filepath):
        filepath = sound._resolve_path(filepath)

        if platform.system() == "Windows":
            if not sound._is_pcm_wav(filepath):
                print("[INFO] Converting WAV to PCM for Windows...")
                converted = sound._convert_to_pcm(filepath)
                if converted:
                    return converted

        return filepath

    # --- Play one instance ---
    @staticmethod
     
    def _play_once(filepath):
        system = platform.system()
        filepath = sound._prepare_file(filepath)

        if system == "Darwin":
            return subprocess.Popen(["afplay", filepath])

        elif system == "Linux":
            try:
                return subprocess.Popen(["aplay", filepath])
            except FileNotFoundError:
                return subprocess.Popen(["paplay", filepath])

        elif system == "Windows":
            import winsound
            winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return None

    # --- Play normally or loop ---
    @staticmethod
     
    def play(filepath, loop=False):

        if loop:
            def loop_play():
                while True:
                    sound._play_once(filepath)

            t = threading.Thread(target=loop_play, daemon=True)
            t.start()
            return

        # non-loop playback
        p = sound._play_once(filepath)
        if p:
            sound._active_processes.append(p)

    # --- Stop all sounds ---
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

class data:
     
    def create(path, extension):
        def _resolve_path(relative_path: str) -> str:
            base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, relative_path)
        path2 = _resolve_path(path) + extension
        
        
        with open(path2, "w") as f:
            f.write("Hello, world!")

     
    def write(file_path, content):
        def _resolve_path(relative_path: str) -> str:
            base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, relative_path)
        path2 = _resolve_path(file_path)
        
        
        with open(path2, "w") as f:
            f.write(content)

     
    def read(file_path, amount_of_chars):
        def _resolve_path(relative_path: str) -> str:
            base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, relative_path)
        path2 = _resolve_path(file_path)
        
        
        with open(path2, "r") as f:
            content = f.read()
        return content
    
     
    def createFolder(name):
        try:
            def _resolve_path(relative_path: str) -> str:
                base = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(base, relative_path)

            path2 = _resolve_path(name)
            

            os.mkdir(path2)
        except Exception as e:
            print(e)

     
    def getFolderExists(path):
        try:
            def _resolve_path(relative_path: str) -> str:
                base = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(base, relative_path)

            path2 = _resolve_path(path)
            

            if os.path.exists(path2):
                return True
            else:
                return False
        except Exception as e:
            print(e)

     
    def getFileExists(path):
        try:
            def _resolve_path(relative_path: str) -> str:
                base = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(base, relative_path)

            path2 = _resolve_path(path)
            

            if os.path.exists(path2):
                return True
            else:
                return False
        except:
            return
    
     
    def readLine(file_path, line):
        def _resolve_path(relative_path: str) -> str:
            base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, relative_path)
        path2 = _resolve_path(file_path)
        
        
        with open(path2, "r") as f:
            content = f.read()
        return content
    
    def delete_file(file_path):
        if data.getFileExists(file_path):
            file_path.unlink()
        else:
            print("Cannot delete file. File not found")
            return

class image:
    # --- Path helper for image files ---
    @staticmethod
     
    def _resolve_path(relative_path: str) -> str:
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, relative_path)

     
    def Load(path, x, y, width, height, window):
        full_path = image._resolve_path(path)

        print("Loading image from:", full_path)

        try:
            img = Image.open(full_path).convert("RGBA")

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
            panel.image = img_tk          # must keep a reference for Tk
            panel.pil_image = img         # store PIL image, e.g., for rotation later
            panel.img_width = width
            panel.img_height = height
            panel.place(x=x, y=y)

            return panel

        except Exception as e:
            print("Error:", e)
            print("Please confirm the file is a .png or .jpg and that the path is correct.")
     
    def getPosX(img):
        return img.winfo_x()
    
     
    def getPosY(img):
        return img.winfo_y()

     
    def Rotate(panel, angle):
        try:
            pil_img = panel.pil_image.convert("RGBA")

            rotated = pil_img.rotate(angle, expand=True)

            # Resize AFTER rotation kills quality.
            # Better: resize BEFORE rotation.
            rotated = rotated.resize((panel.img_width, panel.img_height), Image.LANCZOS)

            img_tk = ImageTk.PhotoImage(rotated, master=panel.master)

            panel.configure(image=img_tk)
            panel.image = img_tk
            panel.pil_image = pil_img  # keep original for future rotation

        except Exception as e:
            print("RotateImage error:", e)

    def crop(img, texture_start_X, texture_start_Y, texture_width, texture_height):
        try:
            atlas = img.convert("RGBA")

            # sprite rect in pixels: (x, y, w, h) with (0,0) at top-left
            x, y, w, h = texture_start_X, texture_start_Y, texture_width, texture_height

            sprite = atlas.crop((x, y, x + w, y + h))
            return sprite
        except:
            pass

class imageFilter:
    def blur(image, scale):
        return image.filter(ImageFilter.GaussianBlur(radius=scale))

class Networking:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.clients = []
        self.running = False
        self.on_message = None
        self.is_server = False

    def start_server(self, host="0.0.0.0", port=5000, on_message=None):
        """Starts a server that listens for clients."""
        self.is_server = True
        self.on_message = on_message
        self.running = True

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

        threading.Thread(target=self._accept_clients, daemon=True).start()
        print(f"[SERVER] Started on {host}:{port}")

    def _accept_clients(self):
        """Accepts clients in background."""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                print(f"[SERVER] Client connected: {addr}")
                self.clients.append(conn)

                threading.Thread(target=self._handle_client,
                                 args=(conn,), daemon=True).start()
            except:
                break

    def _handle_client(self, conn):
        """Handles receiving messages from one client."""
        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                msg = data.decode()
                if self.on_message:
                    self.on_message(msg, conn)  # Pass who sent it
            except:
                break

        print("[SERVER] Client disconnected")
        self.clients.remove(conn)
        conn.close()

    def send_to_client(self, conn, message):
        """Send a message to one connected client."""
        try:
            conn.send(message.encode())
        except:
            pass

    def broadcast(self, message):
        """Send a message to every connected client."""
        for client in list(self.clients):
            try:
                client.send(message.encode())
            except:
                self.clients.remove(client)

    # =====================================================
    # CLIENT FUNCTIONS
    # =====================================================

    def start_client(self, host="127.0.0.1", port=5000, on_message=None):
        """Connect to a server."""
        self.is_server = False
        self.on_message = on_message
        self.running = True

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        threading.Thread(target=self._listen_to_server, daemon=True).start()
        print(f"[CLIENT] Connected to {host}:{port}")

    def _listen_to_server(self):
        """Listen for messages from server."""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                msg = data.decode()
                if self.on_message:
                    self.on_message(msg)
            except:
                break

        print("[CLIENT] Disconnected from server")

    def send_to_server(self, message):
        """Send message to server."""
        if self.client_socket:
            try:
                self.client_socket.send(message.encode())
            except:
                pass

    # =====================================================
    # CLEANUP
    # =====================================================

    def close(self):
        """Shuts down server or client cleanly."""
        self.running = False

        # Close client
        if self.client_socket:
            try: self.client_socket.close()
            except: pass

        # Close server + all clients
        if self.server_socket:
            try: self.server_socket.close()
            except: pass

        for c in self.clients:
            try: c.close()
            except: pass

        self.clients.clear()
        print("[NETWORK] Closed all connections.")

if __name__ == "__main__":
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

    window_name = window.new_window(1000, 1000, "test")
    label1 = gui.label("test", window_name, None, "green", 1, 1)
    label2 = gui.label("mouse", window_name, None, "black", 1, 1)
    gui.pack(label1)

    canvas = Canvas.create_canvas(1000, 1000, "#000000", window_name, -2, 0)

    window.set_cursor("cross", window_name)

    mouse = Mouse(window_name)

    print_FPS = True
    print_mouseX = True

    def test(event): print("test")
    def test2(): print("test")
    def test3(): print("test2")

    def kill(): window.close(window_name)

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

    img2 = image.Load("image.png", 0, 0, 200, 200, window_name)
    img3 = image.Load("image.png", 0, 0, 200, 200, window_name)

    img5 = image.Load("image.png", 0, 0, 200, 200, window_name)

    img4 = image.crop(img5, 0, 0, 20, 20)

    #general_gui_functions.set_X(img4, 100)

    speed = 8

    def move(): general_gui_functions.Set_Pos(img3, image.getPosX(img3), image.getPosY(img3) + speed)
    Input.bindKey(window_name, "s", move)

    def move2(): general_gui_functions.Set_Pos(img3, image.getPosX(img3) + speed, image.getPosY(img3))
    Input.bindKey(window_name, "d", move2)

    def move3(): general_gui_functions.Set_Pos(img3, image.getPosX(img3), image.getPosY(img3) - speed)
    Input.bindKey(window_name, "w", move3)

    def move4(): general_gui_functions.Set_Pos(img3, image.getPosX(img3) - speed, image.getPosY(img3))
    Input.bindKey(window_name, "a", move4)

    Input.bindKey(window_name, "e", kill)

    image.Rotate(img2, 0)

    mouseX = mouse.get_X()
    mouseY = mouse.get_Y()

    text_input = gui.createTextInput(window_name, 300, 0, 30, 10, True)

    #Mouse.bindMotion(window_name, test)
    #Mouse.bindClick(window_name, "right", test2)

    Mouse.bindMouseWheel(window_name, test2, test3)

    image.Rotate(img2, 0)

    data.create("test", ".txt")
    data.write("test.txt", str(data.read("test.txt", 10)) + "test")
    print(data.read("test.txt", 7))
    if data.getFolderExists("test2") == False:
        data.createFolder("test2")

    general_gui_functions.increase_Z_order(label1)
    general_gui_functions.decrease_Z_order(canvas)

    print(window.getY(window_name))
    print(window.getX(window_name))

    print(Mouse.getGlobalX(window_name))
    print(Mouse.getGlobalY(window_name))

    print(Mouse.getGlobalX(window_name))
    print(Mouse.getGlobalY(window_name))

    def mainloop():
        mouseX = mouse.get_X()
        mouseY = mouse.get_Y()
        window.Title(window_name, str(window.getFPS()))
        Mouse.bindMotion(window_name, general_gui_functions.Set_Pos(img2, (mouseX + 1), (mouseY + 1)))
        random.Screen(10, 50, canvas, window_name)
        window.SetPosition(window_name, 1, 1)
        window.after(window_name, mainloop)

    mainloop()
    window.mainloop(window_name)
