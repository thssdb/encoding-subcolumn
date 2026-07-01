from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

subcolumn_df = pd.read_csv('result/subcolumn_full.csv')
subcolumn_without_bp_df = pd.read_csv('result/subcolumn_without_bp.csv')
subcolumn_without_rle_df = pd.read_csv('result/subcolumn_without_rle.csv')
subcolumn_without_de_df = pd.read_csv('result/subcolumn_without_de.csv')

subcolumn_full_ratio_df = pd.read_csv('result/subcolumn_full2.csv')
subcolumn_without_bp_ratio_df = pd.read_csv('result/subcolumn_without_bp2.csv')
subcolumn_without_rle_ratio_df = pd.read_csv('result/subcolumn_without_rle2.csv')
subcolumn_without_de_ratio_df = pd.read_csv('result/subcolumn_without_de2.csv')

compression_ratio_df = subcolumn_full_ratio_df.merge(
    subcolumn_without_bp_ratio_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_bp')
).merge(
    subcolumn_without_rle_ratio_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_rle')
).merge(
    subcolumn_without_de_ratio_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_de')
)

compression_ratio_df.rename(
    columns={
        'Compression Ratio': 'Sub-column',
        'Compression Ratio_without_bp': 'Sub-column without BPE',
        'Compression Ratio_without_rle': 'Sub-column without RLE',
        'Compression Ratio_without_de': 'Sub-column without DE',
    },
    inplace=True
)

subcolumn_df['Compression Time'] = subcolumn_df['Encoding Time'] / \
    subcolumn_df['Points']
subcolumn_without_bp_df['Compression Time'] = subcolumn_without_bp_df['Encoding Time'] / \
    subcolumn_without_bp_df['Points']
subcolumn_without_rle_df['Compression Time'] = subcolumn_without_rle_df['Encoding Time'] / \
    subcolumn_without_rle_df['Points']
subcolumn_without_de_df['Compression Time'] = subcolumn_without_de_df['Encoding Time'] / \
    subcolumn_without_de_df['Points']

throughput_df = subcolumn_df.merge(
    subcolumn_without_bp_df[['Dataset', 'Compression Time']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_bp')
).merge(
    subcolumn_without_rle_df[['Dataset', 'Compression Time']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_rle')
).merge(
    subcolumn_without_de_df[['Dataset', 'Compression Time']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_de')
)

throughput_df.rename(
    columns={
        'Compression Time': 'Sub-column',
        'Compression Time_without_bp': 'Sub-column without BPE',
        'Compression Time_without_rle': 'Sub-column without RLE',
        'Compression Time_without_de': 'Sub-column without DE',
    },
    inplace=True
)

subcolumn_df['Decoding Time (ns/point)'] = subcolumn_df['Decoding Time'] / \
    subcolumn_df['Points']
subcolumn_without_bp_df['Decoding Time (ns/point)'] = subcolumn_without_bp_df['Decoding Time'] / \
    subcolumn_without_bp_df['Points']
subcolumn_without_rle_df['Decoding Time (ns/point)'] = subcolumn_without_rle_df['Decoding Time'] / \
    subcolumn_without_rle_df['Points']
subcolumn_without_de_df['Decoding Time (ns/point)'] = subcolumn_without_de_df['Decoding Time'] / \
    subcolumn_without_de_df['Points']

decompression_throughput_df = subcolumn_df.merge(
    subcolumn_without_bp_df[['Dataset', 'Decoding Time (ns/point)']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_bp')
).merge(
    subcolumn_without_rle_df[['Dataset', 'Decoding Time (ns/point)']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_rle')
).merge(
    subcolumn_without_de_df[['Dataset', 'Decoding Time (ns/point)']],
    on='Dataset',
    how='left',
    suffixes=('', '_without_de')
)

decompression_throughput_df.rename(
    columns={
        'Decoding Time (ns/point)': 'Sub-column',
        'Decoding Time (ns/point)_without_bp': 'Sub-column without BPE',
        'Decoding Time (ns/point)_without_rle': 'Sub-column without RLE',
        'Decoding Time (ns/point)_without_de': 'Sub-column without DE',
    },
    inplace=True
)

compression_ratio_df['Sub-column'] = 1 / compression_ratio_df['Sub-column']
compression_ratio_df['Sub-column without BPE'] = 1 / \
    compression_ratio_df['Sub-column without BPE']
compression_ratio_df['Sub-column without RLE'] = 1 / \
    compression_ratio_df['Sub-column without RLE']
compression_ratio_df['Sub-column without DE'] = 1 / \
    compression_ratio_df['Sub-column without DE']

colors = ["#FF0000", "#AD62EE", '#008000', '#FFA500']
hatches = ['/' if i % 2 == 0 else '\\' for i in range(len(colors))]

methods = ['Sub-column', 'Sub-column without DE',
           'Sub-column without RLE', 'Sub-column without BPE']
labels = ['Sub-column', 'Sub-column without DE',
          'Sub-column without RLE', 'Sub-column without BPE']


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


means1, stds1 = calculate_stats(compression_ratio_df, methods)
means2, stds2 = calculate_stats(throughput_df, methods)
means3, stds3 = calculate_stats(decompression_throughput_df, methods)

plt.figure(figsize=(12, 4.0))
fontsize = 18
x = np.arange(3)
n_methods = len(methods)
width = 0.2
offsets = (np.arange(n_methods) - (n_methods - 1) / 2.0) * width

ax = plt.gca()
ax_right = ax.twinx()

for i in range(n_methods):
    bars = ax.bar(x[0] + offsets[i], means1[i], width=width,
                  color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

for i in range(n_methods):
    bars = ax_right.bar(x[1] + offsets[i], means2[i], width=width,
                        color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

for i in range(n_methods):
    bars = ax_right.bar(x[2] + offsets[i], means3[i], width=width,
                        color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

line_x_position = (x[0] + x[1]) / 2
ax.axvline(x=line_x_position, color='black', linewidth=2, linestyle='-')

ax.set_xticks(x)
ax.set_xticklabels(['Compression\nRatio', 'Compression\nTime',
                    'Decompression\nTime'],
                   fontsize=fontsize, ha='center')
ax.set_yticklabels(ax.get_yticklabels(), fontsize=fontsize)

ax.set_ylabel('Compression Ratio', fontsize=fontsize)
ax_right.set_ylabel('Time (ns/point)', fontsize=fontsize)
ax_right.set_yticklabels(ax_right.get_yticklabels(), fontsize=fontsize)

legend_elements = [
    Patch(facecolor=colors[0], label=labels[0],
          hatch=hatches[0], edgecolor='black'),
    Patch(facecolor=colors[1], label=labels[1],
          hatch=hatches[1], edgecolor='black'),
    Patch(facecolor=colors[2], label=labels[2],
          hatch=hatches[2], edgecolor='black'),
    Patch(facecolor=colors[3], label=labels[3],
          hatch=hatches[3], edgecolor='black'),
]

ax.legend(handles=legend_elements, loc='upper center',
          columnspacing=0.2,
          bbox_to_anchor=(0.54, 1.3), ncol=2, fontsize=fontsize-2)

ax.set_ylim(0, 1.1*ax.get_ylim()[1])
ax_right.set_ylim(0, 1.1*ax_right.get_ylim()[1])

plt.savefig('fig/ablation_study.png', dpi=300, bbox_inches='tight')
plt.savefig('fig/ablation_study.eps', format='eps',
            dpi=300, bbox_inches='tight')
