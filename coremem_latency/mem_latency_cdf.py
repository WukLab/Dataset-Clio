#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def gen_cdf(filename):
    with open(filename, 'r') as fd:
        lines = fd.read().splitlines()

    cycle_time = 4  # 4ns per cycle
    # skip none integer lines
    data = []
    for line in lines:
        try:
            data.append(int(line) * cycle_time)
        except ValueError:
            pass

    n_bins = max(data) - min(data) + 1
    h, edges = np.histogram(data, density=True, bins=n_bins)
    h = np.cumsum(h)/np.cumsum(h).max()

    x = edges.repeat(2)[:-1]
    y = np.zeros_like(x)
    y[1:] = h.repeat(2)
    return [x, y]


def draw_cdf(pgf_trace, tlb_hit_read_trace, tlb_hit_write_trace, tlb_miss_read_trace, tlb_miss_write_trace, saveto="mem_latency.jpg"):
    pgf_cdf = gen_cdf(pgf_trace)
    tlb_hit_read_cdf = gen_cdf(tlb_hit_read_trace)
    tlb_hit_write_cdf = gen_cdf(tlb_hit_write_trace)
    tlb_miss_read_cdf = gen_cdf(tlb_miss_read_trace)
    tlb_miss_write_cdf = gen_cdf(tlb_miss_write_trace)

    plt.figure(constrained_layout=True)
    plt.rcParams.update({'font.size': 16})
    plt.title("Core Memory Access Latency", pad=7.0)
    plt.xlabel('Latency (ns)')
    plt.ylabel('Percentile')

    plt.plot(*pgf_cdf, lw=3, label="Page Fault (write)")
    plt.plot(*tlb_hit_read_cdf, lw=3, label="TLB Hit (read)")
    plt.plot(*tlb_hit_write_cdf, lw=3, label="TLB Hit (write)")
    plt.plot(*tlb_miss_read_cdf, lw=3, label="TLB Miss (read), \nw/o Page Fault")
    plt.plot(*tlb_miss_write_cdf, lw=3, label="TLB Miss (write), \nw/o Page Fault")
    plt.grid()
    plt.legend()
    plt.savefig(saveto)


if __name__ == "__main__":
    draw_cdf("data_used/lat_pgf_64_w.txt", "data_used/lat_64_r.txt", "data_used/lat_64_w.txt","data_used/lat_64_miss_r.txt", "data_used/lat_64_miss_w.txt")
