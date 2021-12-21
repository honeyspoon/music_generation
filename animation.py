import numpy as np
import matplotlib.animation as animation

TWOPI = 2*np.pi

import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt

low, high = (100, 20_000)
delta_f = (high - low) / (args.columns - 1)
gain = 10
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)

fig, ax = plt.subplots()

t = np.arange(0.0, TWOPI, 0.001)
s = np.sin(t)
l = plt.plot(t, s)

ax = plt.axis([0,TWOPI,-1,1])

redDot, = plt.plot([0], [np.sin(0)], 'ro')
def animate(i):
    redDot.set_data(i, np.sin(i))
    return redDot,

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0.0, TWOPI, 0.1), \
                                      interval=10, blit=True, repeat=True)

plt.show()
