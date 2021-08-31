import matplotlib.pyplot
import numpy as np
import sycomore
from sycomore.units import ms, deg, s

species = sycomore.Species(1000*ms, 1000*ms)
idle = sycomore.bloch.time_interval(species, 10*ms)
flip_angles = np.array([a for a in range(0,91,30)]) * deg

print(flip_angles/deg)

t = 0 * s
df = 1 * ms
total_iters = 200
n_180 = 10
echo_wait = 20

M = {
    fa : np.array([0,0,1,1])
    for fa in flip_angles
}

record = {
    fa : [[t, M[fa][:3]/M[fa][3]]]
    for fa in flip_angles
}


def relax(M, iter, cur_t):
    for _ in range(iter):
        cur_t = cur_t + df
        M = idle @ M
        temp_record.append([cur_t, M[:3] / M[3]])

    return M, cur_t

for fa in flip_angles:
    t = 0 * s
    pulse = sycomore.bloch.pulse(fa)
    pulse_180 = sycomore.bloch.pulse(180*deg)
    temp_record = [[t, M[fa][:3]/M[fa][3]]]

    # initial saturation
    M[fa], t = relax(M[fa], 5, t)

    # apply initial RF excitation
    M[fa] = pulse @ M[fa]

    # wait for longitudinal de-phasing
    M[fa], t = relax(M[fa],20, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # apply 180 pulse, wait for signal to be recovered, then wait for long de-phasing again
    M[fa] = pulse_180 @ M[fa]
    M[fa], t = relax(M[fa], echo_wait, t)
    M[fa], t = relax(M[fa], echo_wait, t)

    # wait for longitudinal de-phasing
    M[fa], t = relax(M[fa], 500, t)

    record[fa] = temp_record

print("Done.")

for fa in flip_angles:
    time, magnetization = list(zip(*record[fa]))
    magnetization = np.array(magnetization)

    x_axis = [x.convert_to(ms) for x in time]
    matplotlib.pyplot.scatter(
        x_axis, np.linalg.norm(magnetization[:, :2], axis=-1), label="$M_\perp$")
    matplotlib.pyplot.scatter(x_axis, magnetization[:, 2], label="$M_z$")
    # matplotlib.pyplot.xlim(0)
    matplotlib.pyplot.ylim(-1)
    matplotlib.pyplot.xlabel("Time (ms)")
    matplotlib.pyplot.ylabel("$M/M_0$")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.title(f"Flip angle: {fa}")
    matplotlib.pyplot.show()
