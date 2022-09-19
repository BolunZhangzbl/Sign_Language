import tkinter as tk
import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from timeit import default_timer
from functools import partial


# User Defined Parameters ##############################################################

demo = False                        # Change to False for arduino
demo_samp_freq = 5.0                # Only for demo use (arduino will setup it's own frequency)
disp_len = 100                      # Number of history data to plot
data_save_addr = "./data/data.txt"  # Place to save data

# Other Parameters #####################################################################

serial_port = "com3"                # Serial port to Arduino
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
    print(data, end="\t")
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
    print()
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


def start_record():
    datas.append([-200] * len(datas[-1]))


def pause_record():
    datas.append([-100] * len(datas[-1]))


# --- main ---

datas = [[-1] * N]
times = []

# create button
root = tk.Tk()
root.geometry("200x120")

button = tk.Button(root, text="start", command=lambda:start_record())
button.pack()

button_2 = tk.Button(root, text="pause", command=lambda:pause_record())
button_2.pack()

button_3 = tk.Button(root, text="exit (no save)", command=partial(on_close, False))
button_3.pack()

button_4 = tk.Button(root, text="exit", command=partial(on_close, True))
button_4.pack()

if demo is True:
    read_data = read_from_pseudo_serial
else:
    read_data = read_from_serial
    SerialReciver = serial.Serial(serial_port, baud_rate)

fig, (ax1, ax2) = plt.subplots(2,1)
lines = []
for n in range(4):
    line, = ax1.plot([], [])
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

plt.show()
root.mainloop()  # start program
