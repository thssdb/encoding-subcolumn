from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

subcolumn_df = pd.read_csv('result/subcolumn_long.csv')
subcolumn_pso_df = pd.read_csv('result/subcolumn_dictionary.csv')
subcolumn_rle_df = pd.read_csv('result/subcolumn_rle.csv')
subcolumn_bp_df = pd.read_csv('result/subcolumn_bp.csv')

compression_ratio_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(
    subcolumn_rle_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_rle')
).merge(
    subcolumn_bp_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

compression_ratio_df.rename(
    columns={
        'Compression Ratio_bp': 'Sub-column-only-BPE',
        'Compression Ratio_rle': 'Sub-column-only-RLE',
        'Compression Ratio': 'Sub-column',
        'Compression Ratio_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

subcolumn_df['Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Encoding Time']
subcolumn_pso_df['Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Encoding Time']
subcolumn_rle_df['Throughput'] = subcolumn_rle_df['Points'] / \
    subcolumn_rle_df['Encoding Time']
subcolumn_bp_df['Throughput'] = subcolumn_bp_df['Points'] / \
    subcolumn_bp_df['Encoding Time']


throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(subcolumn_rle_df[[
        'Dataset', 'Throughput']], on='Dataset', how='left', suffixes=('', '_rle')
        ).merge(
    subcolumn_bp_df[['Dataset', 'Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

throughput_df.rename(
    columns={
        'Throughput_rle': 'Sub-column-only-BPE',
        'Throughput_bp': 'Sub-column-only-RLE',
        'Throughput': 'Sub-column',
        'Throughput_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

subcolumn_df['Decoding Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Decoding Time']
subcolumn_pso_df['Decoding Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Decoding Time']
subcolumn_rle_df['Decoding Throughput'] = subcolumn_rle_df['Points'] / \
    subcolumn_rle_df['Decoding Time']
subcolumn_bp_df['Decoding Throughput'] = subcolumn_bp_df['Points'] / \
    subcolumn_bp_df['Decoding Time']

decompression_throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(subcolumn_rle_df[[
    'Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_rle')
).merge(
    subcolumn_bp_df[['Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

decompression_throughput_df.rename(
    columns={
        'Decoding Throughput_rle': 'Sub-column-only-RLE',
        'Decoding Throughput_bp': 'Sub-column-only-BPE',
        'Decoding Throughput': 'Sub-column',
        'Decoding Throughput_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

fontsize = 18
labelsize = 18

ax1: Axes
ax2: Axes
ax3: Axes

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
plt.subplots_adjust(wspace=0.6)

colors = ['#FF0000', '#008000']

compression_ratio_df['Sub-column-only-RLE'] = 1 / \
    compression_ratio_df['Sub-column-only-RLE']
compression_ratio_df['Sub-column-only-BPE'] = 1 / \
    compression_ratio_df['Sub-column-only-BPE']
compression_ratio_df['Sub-column'] = 1 / compression_ratio_df['Sub-column']
compression_ratio_df['Sub-column (+DE)'] = 1 / \
    compression_ratio_df['Sub-column (+DE)']

labels = ['Sub-column without DE', 'Sub-column with DE']

data_to_plot1 = [
    compression_ratio_df['Sub-column'], compression_ratio_df['Sub-column (+DE)']
]

box1 = ax1.boxplot(data_to_plot1, tick_labels=labels,
                   patch_artist=True, widths=0.8)

for patch, color in zip(box1['boxes'], colors):
    patch.set_facecolor(color)
ax1.set_title('(a) Compression ratio', fontsize=fontsize, x=0.3)
ax1.set_ylabel('Compression Ratio', fontsize=fontsize)
ax1.tick_params(axis='both', which='major', labelsize=labelsize)

data_to_plot2 = [
    throughput_df['Sub-column'],
    throughput_df['Sub-column (+DE)']
]

box2 = ax2.boxplot(data_to_plot2, tick_labels=labels,
                   patch_artist=True, widths=0.8)
for patch, color in zip(box2['boxes'], colors):
    patch.set_facecolor(color)
ax2.set_title('(b) Compression throughput', fontsize=fontsize, x=0.1)
ax2.set_ylabel('Throughput (point/ns)', fontsize=fontsize)
ax2.tick_params(axis='both', which='major', labelsize=labelsize)
ax2.set_ylim(0, 0.21)

data_to_plot3 = [
    decompression_throughput_df['Sub-column'],
    decompression_throughput_df['Sub-column (+DE)']
]

box3 = ax3.boxplot(data_to_plot3, tick_labels=labels,
                   patch_artist=True, widths=0.8)
for patch, color in zip(box3['boxes'], colors):
    patch.set_facecolor(color)
ax3.set_title('(c) Decompression throughput', fontsize=fontsize, x=0.15)
ax3.set_ylabel('Throughput (point/ns)', fontsize=fontsize)
ax3.tick_params(axis='both', which='major', labelsize=labelsize)
ax3.set_ylim(0, 0.21)
for ax in (ax1, ax2, ax3):
    ax.set_xticks([])

legend_elements = [
    Patch(facecolor=colors[0], label='Sub-column without DE'),
    Patch(facecolor=colors[1], label='Sub-column with DE')
]

fig.legend(
    handles=legend_elements,
    loc='upper center',
    ncol=4,
    bbox_to_anchor=(0.48, 1.1),
    columnspacing=0.1,
    labelspacing=0.1,
    handletextpad=0.1,
    fontsize=fontsize-0.5
)

plt.savefig('fig/R2O2_compare_add_dictionary_boxplot.png',
            dpi=300, bbox_inches='tight')
plt.savefig('fig/R2O2_compare_add_dictionary_boxplot.eps',
            format='eps', dpi=300, bbox_inches='tight')


subcolumn_df = pd.read_csv('result/subcolumn_long.csv')
subcolumn_pso_df = pd.read_csv('result/subcolumn_dictionary.csv')
subcolumn_rle_df = pd.read_csv('result/subcolumn_rle.csv')
subcolumn_bp_df = pd.read_csv('result/subcolumn_bp.csv')

compression_ratio_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(
    subcolumn_rle_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_rle')
).merge(
    subcolumn_bp_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

compression_ratio_df.rename(
    columns={
        'Compression Ratio_bp': 'Sub-column-only-BPE',
        'Compression Ratio_rle': 'Sub-column-only-RLE',
        'Compression Ratio': 'Sub-column',
        'Compression Ratio_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

subcolumn_df['Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Encoding Time']
subcolumn_pso_df['Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Encoding Time']
subcolumn_rle_df['Throughput'] = subcolumn_rle_df['Points'] / \
    subcolumn_rle_df['Encoding Time']
subcolumn_bp_df['Throughput'] = subcolumn_bp_df['Points'] / \
    subcolumn_bp_df['Encoding Time']

throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(subcolumn_rle_df[['Dataset', 'Throughput']],
        on='Dataset',
        how='left',
        suffixes=('', '_rle')
        ).merge(
    subcolumn_bp_df[['Dataset', 'Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

throughput_df.rename(
    columns={
        'Throughput_rle': 'Sub-column-only-RLE',
        'Throughput_bp': 'Sub-column-only-BPE',
        'Throughput': 'Sub-column',
        'Throughput_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

subcolumn_df['Decoding Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Decoding Time']
subcolumn_pso_df['Decoding Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Decoding Time']
subcolumn_rle_df['Decoding Throughput'] = subcolumn_rle_df['Points'] / \
    subcolumn_rle_df['Decoding Time']
subcolumn_bp_df['Decoding Throughput'] = subcolumn_bp_df['Points'] / \
    subcolumn_bp_df['Decoding Time']

decompression_throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_dictionary')
).merge(subcolumn_rle_df[['Dataset', 'Decoding Throughput']],
        on='Dataset',
        how='left',
        suffixes=('', '_rle')
        ).merge(
    subcolumn_bp_df[['Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_bp')
)

decompression_throughput_df.rename(
    columns={
        'Decoding Throughput_rle': 'Sub-column-only-RLE',
        'Decoding Throughput_bp': 'Sub-column-only-BPE',
        'Decoding Throughput': 'Sub-column',
        'Decoding Throughput_dictionary': 'Sub-column (+DE)',
    },
    inplace=True
)

compression_ratio_df['Sub-column-only-RLE'] = 1 / \
    compression_ratio_df['Sub-column-only-RLE']
compression_ratio_df['Sub-column-only-BPE'] = 1 / \
    compression_ratio_df['Sub-column-only-BPE']
compression_ratio_df['Sub-column'] = 1 / compression_ratio_df['Sub-column']
compression_ratio_df['Sub-column (+DE)'] = 1 / \
    compression_ratio_df['Sub-column (+DE)']

fontsize = 28
labelsize = 28

colors = ['#FF0000', '#008000']

hatches = ['/', '\\']

methods = ['Sub-column', 'Sub-column (+DE)']
labels = ['Sub-column without DE', 'Sub-column with DE']


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


fontsize = 18
labelsize = 18

means1, stds1 = calculate_stats(compression_ratio_df, methods)
means2, stds2 = calculate_stats(throughput_df, methods)
means3, stds3 = calculate_stats(decompression_throughput_df, methods)

fig, ax = plt.subplots(figsize=(4, 3))
plt.subplots_adjust()

ax_right = ax.twinx()

x = np.arange(3)
n_methods = len(methods)
width = 0.28
offsets = (np.arange(n_methods) - (n_methods - 1) / 2.0) * width
rotation = 30
ha = 'center'
for i in range(n_methods):
    ax.bar(x[0] + offsets[i], means1[i], width=width,
           color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

for i in range(n_methods):
    ax_right.bar(x[1] + offsets[i], means2[i], width=width,
                 color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)
    ax_right.bar(x[2] + offsets[i], means3[i], width=width,
                 color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

line_x_position = (x[0] + x[1]) / 2  #
ax.axvline(x=line_x_position, color='black', linewidth=2, linestyle='-')

ax.set_xticks(x)
ax.set_xticklabels(['Compression\nRatio', 'Compression\nThroughput', 'Decompression\nThroughput'],
                   fontsize=labelsize, ha=ha, rotation=rotation)

ax.set_ylabel('Compression Ratio', fontsize=fontsize)
ax_right.set_ylabel('Throughput (point/ns)', fontsize=fontsize)

max_left = max(means1) if len(means1) > 0 else 1.0
ax.set_ylim(0, max_left * 1.25)

max_right = 0.081
if len(means2) > 0 or len(means3) > 0:
    max_th = max(max(means2) if len(means2) else 0,
                 max(means3) if len(means3) else 0)
    max_right = max(max_right, max_th * 1.25)
ax_right.set_ylim(0, max_right)

ax.tick_params(axis='y', labelsize=labelsize)
ax.tick_params(axis='x', labelsize=labelsize)
ax_right.tick_params(axis='y', labelsize=labelsize)

legend_elements = [Patch(facecolor=colors[i], hatch=hatches[i], label=labels[i])
                   for i in range(n_methods)]
fig.legend(
    handles=legend_elements,
    loc='upper center',
    ncol=1,
    bbox_to_anchor=(0.48, 1.15),
    columnspacing=0.1,
    labelspacing=0.1,
    handletextpad=0.1,
    fontsize=labelsize,
)

plt.savefig('fig/R2O2_compare_add_dictionary.png',
            dpi=300, bbox_inches='tight')
plt.savefig('fig/R2O2_compare_add_dictionary.eps',
            format='eps', dpi=300, bbox_inches='tight')
