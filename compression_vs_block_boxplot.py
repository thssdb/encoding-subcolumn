import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

ax1: Axes
ax2: Axes
ax3: Axes
fig, (ax1, ax2, ax3) = plt.subplots(
    1,
    3,
    figsize=(24, 6.5)
)

block_sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

fontsize = 20
labelsize = 20

file_names = [
    f'./result/compression_vs_block/subcolumn_block_{size}.csv' for size in block_sizes]

# ax1
compression_ratios = {}

for file_name, block_size in zip(file_names, block_sizes):
    df = pd.read_csv(file_name)

    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']

        if dataset not in compression_ratios:
            compression_ratios[dataset] = []

        compression_ratios[dataset].append((block_size, compression_ratio))

boxplot_data1 = {}
for dataset, ratios in compression_ratios.items():
    for block_size, ratio in ratios:
        if block_size not in boxplot_data1:
            boxplot_data1[block_size] = []
        boxplot_data1[block_size].append(ratio)

widths1 = np.array(list(boxplot_data1.keys())) / 8
box_plot1 = ax1.boxplot(
    boxplot_data1.values(),
    positions=boxplot_data1.keys(),
    widths=widths1
)
medians1 = [np.median(data) for data in boxplot_data1.values()]
ax1.plot(
    list(boxplot_data1.keys()),
    medians1,
    color='orange',
    linestyle='-',
    marker='o',
    linewidth=2,
    markersize=6
)

ax1.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax1.set_xscale(
    'log',
    base=2
)
ax1.set_xticks(list(boxplot_data1.keys()))
ax1.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in boxplot_data1.keys()]
)
ax1.set_xlabel('Block Size n', fontsize=fontsize)
ax1.set_ylabel('Compression Ratio', fontsize=fontsize)
ax1.set_title('(a) Compression ratio', fontsize=fontsize)

# ax2
encoding_times = {}

for file_name, block_size in zip(file_names, block_sizes):
    df = pd.read_csv(file_name)

    for index, row in df.iterrows():
        dataset = row['Dataset']
        time_per_point = row['Encoding Time'] / row['Points']

        if dataset not in encoding_times:
            encoding_times[dataset] = []

        encoding_times[dataset].append((block_size, time_per_point))

boxplot_data2 = {}
for dataset, ratios in encoding_times.items():
    for block_size, time in ratios:
        if block_size not in boxplot_data2:
            boxplot_data2[block_size] = []
        boxplot_data2[block_size].append(time)

widths2 = np.array(list(boxplot_data2.keys())) / 8
box_plot2 = ax2.boxplot(
    boxplot_data2.values(),
    positions=boxplot_data2.keys(),
    widths=widths2
)

medians2 = [np.median(data) for data in boxplot_data2.values()]
ax2.plot(
    list(boxplot_data2.keys()),
    medians2,
    color='orange',
    linestyle='-',
    marker='o',
    linewidth=2,
    markersize=6
)

ax2.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax2.set_xscale(
    'log',
    base=2
)
ax2.set_xticks(list(boxplot_data2.keys()))
ax2.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in boxplot_data2.keys()]
)
ax2.set_xlabel('Block Size n', fontsize=fontsize)
ax2.set_ylabel('Compression Time (ns/point)', fontsize=fontsize)
ax2.set_title('(b) Compression time', fontsize=fontsize)

# ax3
decoding_times = {}

for file_name, block_size in zip(file_names, block_sizes):
    df = pd.read_csv(file_name)

    for index, row in df.iterrows():
        dataset = row['Dataset']
        time_per_point = row['Decoding Time'] / row['Points']

        if dataset not in decoding_times:
            decoding_times[dataset] = []

        decoding_times[dataset].append((block_size, time_per_point))

boxplot_data3 = {}
for dataset, ratios in decoding_times.items():
    for block_size, time in ratios:
        if block_size not in boxplot_data3:
            boxplot_data3[block_size] = []
        boxplot_data3[block_size].append(time)

widths3 = np.array(list(boxplot_data3.keys())) / 8
box_plot3 = ax3.boxplot(
    boxplot_data3.values(),
    positions=boxplot_data3.keys(),
    widths=widths3
)

medians3 = [np.median(data) for data in boxplot_data3.values()]
ax3.plot(
    list(boxplot_data3.keys()),
    medians3,
    color='orange',
    linestyle='-',
    marker='o',
    linewidth=2,
    markersize=6
)

ax3.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax3.set_xscale(
    'log',
    base=2
)
ax3.set_xticks(list(boxplot_data3.keys()))
ax3.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in boxplot_data3.keys()]
)
ax3.set_xlabel('Block Size n', fontsize=fontsize)
ax3.set_ylabel('Decompression Time (ns/point)', fontsize=fontsize)
ax3.set_title('(c) Decompression time', fontsize=fontsize)

plt.savefig(
    './fig/block_size_comparison.png',
    dpi=1000,
    bbox_inches='tight'
)
plt.savefig(
    './fig/block_size_comparison.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
# plt.show()
