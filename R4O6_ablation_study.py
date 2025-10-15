from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

query_df = pd.read_csv('result/point_query/subcolumn_point_query.csv')
rle_df = pd.read_csv('result/point_query_rle/subcolumn_point_query.csv')
bp_df = pd.read_csv('result/point_query_bp/subcolumn_point_query.csv')

query_df["Sub-column"] = query_df["Decoding Time"] / 100000
rle_df["Sub-column-only-RLE"] = rle_df["Decoding Time"] / 100000
bp_df["Sub-column-only-BPE"] = bp_df["Decoding Time"] / 100000

query_df = query_df.merge(
    rle_df[['Dataset', 'Sub-column-only-RLE']],
    on='Dataset',
    how='left'
).merge(
    bp_df[['Dataset', 'Sub-column-only-BPE']],
    on='Dataset',
    how='left'
)

query_df = query_df[['Dataset', 'Sub-column-only-BPE',
                     'Sub-column-only-RLE', 'Sub-column']]

colors = ["#AD62EE", '#008000', '#FF0000', "#2A90EA"]

hatches = ['/' if i %
           2 == 0 else '\\' for i in range(3)]

methods = ['Sub-column-only-BPE', 'Sub-column-only-RLE', 'Sub-column']
labels = ['Sub-column-only-BPE', 'Sub-column-only-RLE', 'Sub-column']


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


means1, stds1 = calculate_stats(
    compression_ratio_df, methods)
means2, stds2 = calculate_stats(
    throughput_df, methods)
means3, stds3 = calculate_stats(
    decompression_throughput_df, methods)
means4, stds4 = calculate_stats(
    query_df, methods)

plt.figure(figsize=(10, 4))
fontsize = 17
x = np.arange(4)
n_methods = len(methods)
width = 0.25
offsets = (np.arange(n_methods) - (n_methods - 1) / 2.0) * width

ax = plt.gca()
ax_right = ax.twinx()

for i in range(n_methods):
    bars = ax.bar(x[0] + offsets[i], means1[i], width=width,
                  color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)
    ax.text(x[0] + offsets[i], means1[i] + 0.0025, f'{means1[i]:.2f}',
            ha='center', va='bottom', fontsize=fontsize)

for i in range(n_methods):
    bars = ax_right.bar(x[1] + offsets[i], means2[i], width=width,
                        color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)
    ax_right.text(x[1] + offsets[i], means2[i] + 0.0025, f'{means2[i]:.2f}',
                  ha='center', va='bottom', fontsize=fontsize)

for i in range(n_methods):
    bars = ax_right.bar(x[2] + offsets[i], means3[i], width=width,
                        color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)
    ax_right.text(x[2] + offsets[i], means3[i] + 0.0025, f'{means3[i]:.2f}',
                  ha='center', va='bottom', fontsize=fontsize)

for i in range(n_methods):
    bars = ax_right.bar(x[3] + offsets[i], means4[i], width=width,
                        color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)
    ax_right.text(x[3] + offsets[i], means4[i] + 0.0025, f'{means4[i]:.2f}',
                  ha='center', va='bottom', fontsize=fontsize)
line_x_position = (x[0] + x[1]) / 2  #
ax.axvline(x=line_x_position, color='black', linewidth=2, linestyle='-')

ax.set_xticks(x)
ax.set_xticklabels(['Compression\nRatio', 'Compression\nThroughput\n(points/ns)',
                    'Decompression\nThroughput\n(points/ns)', 'Point Query\nTime (ns/point)'],
                   fontsize=fontsize, ha='center')
ax.set_yticklabels(ax.get_yticklabels(), fontsize=fontsize)

ax.set_ylabel('Compression Ratio', fontsize=fontsize)
ax_right.set_ylabel(
    'Throughput (points/ns) /\nQuery Time (ns/point)', fontsize=fontsize)
ax_right.set_yticklabels(ax_right.get_yticklabels(), fontsize=fontsize)

legend_elements = [
    Patch(facecolor=colors[0], label=labels[0], hatch=hatches[0]),
    Patch(facecolor=colors[1], label=labels[1], hatch=hatches[1]),
    Patch(facecolor=colors[2], label=labels[2], hatch=hatches[2]),
]

ax.legend(handles=legend_elements, loc='upper center',
          bbox_to_anchor=(0.54, 1.2), ncol=3, fontsize=fontsize)
ax.set_ylim(0, 1.1*ax.get_ylim()[1])
ax_right.set_ylim(0, 1.1*ax_right.get_ylim()[1])

plt.savefig('fig/R1D5_R4O6_ablation_study.png', dpi=300, bbox_inches='tight')
plt.savefig('fig/R1D5_R4O6_ablation_study.eps',
            format='eps', dpi=300, bbox_inches='tight')
