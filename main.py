import pyaudio
import time

from p5 import *

import scipy.signal as signal

import sounddevice as sd
import queue
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import collections
built_in_mic = 2
built_in_output = 1

device=(built_in_mic, built_in_output)

device_info = sd.query_devices(device, 'input')
samplerate = device_info['default_samplerate']

blocksize = 1024
channels = 1
latency = 0

d = collections.deque(maxlen=3)

low, high = (100, 20_000)
bins = 10
delta_f = (high - low) / (bins - 1)
gain = 10
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)

b = None
n = None

def callback(indata, outdata, frames, time, status):
    global d
    if status:
        print(status) 
    volume = np.mean(np.absolute(indata))
    d.append(volume)

    magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
    magnitude *= gain / fftsize
    global b, n
    b, n = np.histogram(np.log10(magnitude + 1), bins='auto')

def setup():
    size(600, 600)
    no_stroke()
    background(204)

def draw():
    global d
    center_x = width / 2
    center_y = height /2
    center = (center_x, center_y)

    background(204, 204, 204, 1)

    c = sum(d)/len(d)
    fill(c, 0, c, 80)
    circle_size = 500 * c
    circle_pos = center
    offset = 50
    circle(circle_pos, circle_size)
    circle((center_x - offset, center_y - offset), circle_size / 2)
    circle((center_x + offset, center_y + offset), circle_size / 2)

    global b, n

    if b is not None and n is not None:
        l = bins
        w = width / l
        h = 40
        for i, v in enumerate(b):
            fill(i * 20, 20, i * 20)
            rect(i * w, 0, i * w + w, h * v)

stream = sd.Stream(
    device=device,
    samplerate=samplerate,
    blocksize=blocksize,
    latency=latency,
    channels=channels,
    callback=callback
)

with stream:
    run()
    
