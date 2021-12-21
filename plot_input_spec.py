#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import math

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-d', '--device', type=int,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')

args = parser.parse_args()
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

if args.samplerate is None:
    device_info = sd.query_devices(args.device, 'input')
    args.samplerate = device_info['default_samplerate']

print(args)

low, high = (100, 20_000)
bins = 1000
delta_f = (high - low) / (bins - 1)
gain = 10
fftsize = math.ceil(args.samplerate / delta_f)
low_bin = math.floor(low / delta_f)

length = int(args.window * args.samplerate / (1000 * args.downsample))
mag = np.zeros((int(fftsize/2 + 1),))

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)

    fft = np.fft.rfft(indata[::args.downsample, mapping], n=fftsize)
    magnitude = np.abs(fft)
    magnitude *= gain / fftsize
    global mag
    mag = magnitude

def update_plot(frame):
    global mag
    for _, line in enumerate(lines):
        line.set_ydata(mag)
    print("new data", len(mag))
    ax.relim()
    ax.autoscale_view()
    return lines

fig, ax = plt.subplots()
lines = ax.plot(mag)
ax.set_xscale('log')

ax.yaxis.grid(True)

fig.tight_layout(pad=0)

stream = sd.InputStream(
    device=args.device,
    channels=max(args.channels),
    samplerate=args.samplerate,
    callback=audio_callback
)

ani = FuncAnimation(
    fig,
    update_plot,
    interval=args.interval,
    blit=True
)

with stream:
    plt.show()
