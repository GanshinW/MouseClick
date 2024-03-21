import time
import threading
import pynput.mouse 
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
from tkinter import *
import ctypes

LEFT = 0
RIGHT = 1


# Mouse clicking control class
class MouseClick:
    def __init__(self, button, time_interval):
        self.mouse = pynput.mouse.Controller()
        self.running = False  # To check if it's running
        self.time_interval = time_interval
        self.button = button
        self.mouse_pressed = False  # To check if the mouse button is pressed
        # Starting the main listener thread
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def on_key_press(self, key):
        if key == Key.f8:
            if self.running:
                self.running = False
                state.delete('0.0', END)
                state.insert(INSERT, "Current State: Listening\n")
                state.insert(INSERT, "Press ESC to stop listening.\n")
                state.insert(INSERT, "Press F8 to switch clicking.")
                # Need to call this function to stop clicking
                self.perform_click()
            else:
                self.running = True
                state.delete('0.0', END)
                state.insert(INSERT, "Current State: Clicking\n")
                state.insert(INSERT, "Press F8 to stop clicking.\n")
                state.insert(INSERT, "Clicking.\n")
                self.perform_click()
        elif key == Key.esc and not self.running:
            start_button['state'] = NORMAL
            state.delete('0.0', END)
            state.insert(
                INSERT, "Choose which mouse button to click and set the time interval, then click START button to start clicking.")
            # Exiting the main listener thread
            self.listener.stop()

    def perform_click(self):
        # Additional thread for listening to update self.running and avoid infinite loops
        key_listener = Listener(on_press=self.on_key_press)
        key_listener.start()
        while self.running:
            self.mouse.click(self.button)
            self.mouse_pressed = True
            time.sleep(self.time_interval)
        key_listener.stop()

    def on_mouse_click(self, x, y, button, pressed):
        # Updating the mouse pressed status
        if button == self.button:
            self.mouse_pressed = pressed
                
# Function for new thread start
def start_new_thread(button, time_interval):
    MouseClick(button, time_interval)


# START button handling function
def start():
    try:
        # Convert the string from the text box to a floating-point number
        time_interval = float(time_interval_entry.get()) / 1000
        if time_interval < 0.2:
            time_interval = 0.2
        if mouse_button.get() == LEFT:
            button = pynput.mouse.Button.left
        elif mouse_button.get() == RIGHT:
            button = pynput.mouse.Button.right
        start_button['state'] = DISABLED
        state.delete('0.0', END)
        state.insert(INSERT, "Current State: Listening\n")
        state.insert(INSERT, "Press ESC to stop listening.\n")
        state.insert(INSERT, "Press F8 to start clicking.")
        # Starting a new thread to avoid GUI freeze
        thread = threading.Thread(target=start_new_thread, args=(button, time_interval))
        # Setting the thread as daemon so it exits when the GUI is closed unexpectedly
        thread.setDaemon(True)
        thread.start()
    except:
        state.delete('0.0', END)
        state.insert(INSERT, "Time input ERROR!\n")
        state.insert(INSERT, "You should enter an integer or a float number.")

# -------------------------------- UI --------------------------------
root = Tk()
# High dpi
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)

root.title('Mouse Clicker')
root.geometry('300x300')

mouse_button = IntVar()
lab1 = Label(root, text='Mouse Button', font=("Arial", 11), fg="gray")
lab1.place(relx=0.05, y=10, relwidth=0.4, height=30)
r1 = Radiobutton(root,
                 text='LEFT',
                 font=("Arial", 10),
                 value=0,
                 variable=mouse_button)
r1.place(relx=0.45, y=10, relwidth=0.2, height=30)
r2 = Radiobutton(root,
                 text='RIGHT',
                 font=("Arial", 10),
                 value=1,
                 variable=mouse_button)
r2.place(relx=0.7, y=10, relwidth=0.2, height=30)

lab2 = Label(root, text='Time Interval(ms)', font=("Arial", 11), fg="gray")
lab2.place(relx=0.05, y=50, relwidth=0.4, height=30)
defaultValue = StringVar(value='200')
time_interval_entry = Entry(root, relief="flat", font=("Arial", 10), textvariable = defaultValue)
time_interval_entry.place(relx=0.55, y=50, relwidth=0.4, height=30)

state = Text(root, relief="flat", font=("Arial", 10))
state.place(relx=0.1, y=150, relwidth=0.8, height=100)
state.insert(INSERT, "Choose which mouse button you want to click and set the time interval, then click START button to start listening.")

start_button = Button(root,
                   text='START',
                   font=("Arial", 12),
                   fg="white",
                   bg="#000000",
                   relief="flat",
                   command=start)
start_button.place(relx=0.1, y=100, relwidth=0.8, height=30)

root.mainloop()
# -------------------------------- UI --------------------------------