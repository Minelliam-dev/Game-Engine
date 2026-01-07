#import the window, gui and canvas classes from the library.py file
from library.Engine import window, gui, Canvas

#color converting function from r, g, b to hex
def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

#initialize the window
window_name = window.new_window(200, 200, "color selector")
window_name.config(bg="white")

#initialize the status color text and live color preview
color_text = gui.label("#000000", window_name, "white", "black", 0, 80)
canvas = Canvas.create_canvas(75, 75, "white", window_name, 0, 100)

#sliders
r_slider = gui.slider(window_name, 0, 0, 255, 0, "horizontal")
g_slider = gui.slider(window_name, 0, 25, 255, 0, "horizontal")
b_slider = gui.slider(window_name, 0, 50, 255, 0, "horizontal")

#status texts
r_text = gui.label("red", window_name, "white", "black", 100, 0)
g_text = gui.label("green", window_name, "white", "black", 100, 25)
b_text = gui.label("blue", window_name, "white", "black", 100, 50)

def mainloop():
    #save the slider values so they don't have to be referenced each time
    red = gui.sliderValue(r_slider)
    green = gui.sliderValue(g_slider)
    blue = gui.sliderValue(b_slider)
    
    #update the hex color status text
    gui.SetLabelText(color_text, rgb_to_hex(red, green, blue))

    #draw the color selected by the user
    Canvas.draw_pixel(0, 0, rgb_to_hex(red, green, blue), canvas, 75)
    window.after(window_name, mainloop)

mainloop()
window.mainloop(window_name)
