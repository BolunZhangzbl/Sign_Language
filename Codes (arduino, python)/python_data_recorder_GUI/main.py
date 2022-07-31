# 升级到2.0了！！！！

import tkinter as tk
import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from timeit import default_timer
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# User Defined Parameters ##############################################################

demo = False                       # Change to False for arduino
demo_samp_freq = 60.0                # Only for demo use (arduino will setup it's own frequency)
disp_len = 100                      # Number of history data to plot
data_save_addr = "D:/ML_LAB/Git/data_collection/init.txt"  # Place to save data
colors = ["blue", "#d1c000", "green", "orange"]  # EMG color

# Other Parameters ####################################################################

serial_port = "com5"                # Serial port to Arduino
baud_rate = 115200                  # Serial port baud rate
ani_period = 1                      # Figure refresh period
N = 11                              # Number of data transmitted to comp

########################################################################################


# --- functions ---

t_start = default_timer()
t_count = 0


def read_from_serial():
    """
    msg shape: [discret_time(int), [4 emg], [6 imu]]
    """
    error_flag = False
    try:
        msg = SerialReciver.readline().decode('UTF-8')[:-2]
        msg = msg.split()
        if len(msg) < (N-1):
            error_flag = True
        data_to_return = [int(msg[0])] + list(map(int, msg[1:5])) + list(map(float, msg[5:]))
    except UnicodeDecodeError:
        error_flag = True

    finally:
        if error_flag is True:
            return [-1] * N
        else:
            return data_to_return


def read_from_pseudo_serial():
    t = default_timer() - t_start

    n = int(t * demo_samp_freq)

    emgs = []
    for i in range(4):
        emgs.append(512*(np.sin((t+i*3)/10)+1))

    imus = np.asarray(datas[-1][-6:]) + (np.random.random(size=6) - 0.5) * 0.3
    for i in range(6):
        imus[i] = min([max([imus[i], -1]), 1])

    t += 1
    return [n] + emgs + imus.tolist()


def animation(i):
    global t_count, datas

    data = read_data()
    # print(data, end="\t")
    n = data[0]
    if n < t_count:
        t_count = n
        datas = [[-1] * N]

    elif n > t_count:
        t_count = n
        datas.append(data)

    y = np.asarray(datas[-min([disp_len, len(datas)]):])[:,1:].T
    x = np.asarray([i for i in range(max([0, disp_len - len(datas)]), disp_len)])

    for i in range(len(lines)):
        line = lines[i]
        line.set_data(x, y[i])
    # print()
    return lines


def on_close(save_file):
    if save_file is True:
        file_p = open(data_save_addr, "w")
        for i in range(len(datas)):
            s = datas[i]
            s = " ".join(map(str, s))
            file_p.write(s+"\n")
        file_p.close()
        print("Data saved! Exiting.")
    else:
        print("Exiting without saving.")
    exit(True)


counter = 0
doing = False
def start_pause_record(tk_label):
    global counter, doing
    if doing is False:
        doing = True
        counter += 1
        tk_label.config(text="ACTIVE\n"+str(counter), fg="#eeeeee", bg="#ff0000")
        print(counter, end="\t")
        datas.append([-200] * len(datas[-1]))
    else:
        doing = False
        tk_label.config(text="READY\n"+str(counter), fg="#000000", bg="#e0e0e0")
        print("End")
        datas.append([-100] * len(datas[-1]))


def tk_key_pressed(event, root, tk_label):
    if event.char == " ":
        start_pause_record(tk_label)
    elif event.char == "s":
        on_close(True)
        root.destroy()
    elif event.char == "x":
        on_close(False)
        root.destroy()


# --- main ---

if __name__ == "__main__":

    datas = [[-1] * N]
    times = []

    # create button
    root = tk.Tk()
    # root.geometry("200x120")

    # button = tk.Button(root, text="start/pause", command=lambda:start_pause_record())
    # button.pack()

    button_3 = tk.Button(root, text="exit (no save)", command=partial(on_close, False))
    button_3.pack()

    button_4 = tk.Button(root, text="save and exit", command=partial(on_close, True))
    button_4.pack()

    tk_label = tk.Label(root, text="READY\n"+str(counter), fg="#000000", bg="#e0e0e0", width=20, font=("Times", "24", "bold"))
    tk_label.pack()

    tk_label_info = tk.Label(root, text="space - to toggle acting\nS - exit and save\nX - exit WITHOUT saving")
    tk_label_info.pack()

    tk_label_info2 = tk.Label(root, text="Data will be saved to: "+data_save_addr, fg="#555555", bg="#e0ffff")
    tk_label_info2.pack()

    if demo is True:
        read_data = read_from_pseudo_serial
    else:
        read_data = read_from_serial
        SerialReciver = serial.Serial(serial_port, baud_rate)

    fig, (ax1, ax2) = plt.subplots(2,1)
    lines = []
    for n in range(4):
        line, = ax1.plot([], [], color=colors[n])
        lines.append(line)
    for n in range(6):
        line, = ax2.plot([], [])
        lines.append(line)

    ax1.set_xlim(0, disp_len - 1)
    ax1.set_ylim(0, 1024)
    ax1.legend(["EMG "+str(i+1) for i in range(4)])
    ax2.set_xlim(0, disp_len - 1)
    ax2.set_ylim(-20, 20)
    ax2.legend(["angX", "angY", "angZ", "linX", "linY", "linZ"])

    fn_ani = FuncAnimation(fig, animation, frames=None, interval=ani_period, blit=True)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.bind("<Key>", lambda event: tk_key_pressed(event, root, tk_label))

    root.focus_force()
    root.resizable(False, False)
    def dummy_func():
        pass
    root.protocol("WM_DELETE_WINDOW", dummy_func)
    root.title("Demo reader" if demo is True else "Arduino data reader")
    root.mainloop()  # start program
