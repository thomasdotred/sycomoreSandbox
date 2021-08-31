import matplotlib.pyplot
import numpy
import sycomore
from sycomore.units import ms,deg,s

species = sycomore.Species(100*ms, 10*ms)
flip_angle = 40*deg
flip_180 = 80*deg

idle = sycomore.bloch.time_interval(species, 10*ms)
pulse = sycomore.bloch.pulse(flip_angle)
pulse_180 = sycomore.bloch.pulse(flip_180)
t = 0*s
M = numpy.array([0,0,1,1])

record = [[t, M[:3]/M[3]]]

# Initial saturation period
for _ in range(10):
    t = t+10*ms
    M = idle @ M
    record.append([t, M[:3]/M[3]])

# Apply pulse
M = pulse @ M
record.append([t, M[:3]/M[3]])

# analyse recovery
for _ in range(10):
    t = t+10*ms
    M = idle @ M
    record.append([t, M[:3]/M[3]])

# apply 180 flip pulse
M = pulse_180 @ M
record.append([t, M[:3]/M[3]])

# analyse recovery
for _ in range(10):
    t = t+10*ms
    M = idle @ M
    record.append([t, M[:3]/M[3]])

# apply 180 flip pulse
M = pulse_180 @ M
record.append([t, M[:3]/M[3]])

# analyse recovery
for _ in range(10):
    t = t+10*ms
    M = idle @ M
    record.append([t, M[:3]/M[3]])

# apply 180 flip pulse
M = pulse_180 @ M
record.append([t, M[:3]/M[3]])

# analyse recovery
for _ in range(10):
    t = t+10*ms
    M = idle @ M
    record.append([t, M[:3]/M[3]])


time, magnetization = list(zip(*record))
magnetization = numpy.array(magnetization)

x_axis = [x.convert_to(ms) for x in time]
matplotlib.pyplot.plot(
    x_axis, numpy.linalg.norm(magnetization[:, :2], axis=-1), label="$M_\perp$")
matplotlib.pyplot.plot(x_axis, magnetization[:, 2], label="$M_z$")
matplotlib.pyplot.xlim(0)
matplotlib.pyplot.ylim(-0.02)
matplotlib.pyplot.xlabel("Time (ms)")
matplotlib.pyplot.ylabel("$M/M_0$")
matplotlib.pyplot.legend()
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()