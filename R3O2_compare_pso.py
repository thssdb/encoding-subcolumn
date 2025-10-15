from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

subcolumn_df = pd.read_csv('result/subcolumn_long.csv')
subcolumn_pso_df = pd.read_csv('result/subcolumn_pso.csv')

compression_ratio_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left',
    suffixes=('', '_pso')
)
compression_ratio_df.rename(
    columns={
        'Compression Ratio': 'Sub-column (Exact)',
        'Compression Ratio_pso': 'Sub-column (PSO)',
    },
    inplace=True
)

subcolumn_df['Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Encoding Time']
subcolumn_pso_df['Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Encoding Time']

throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_pso')
)

throughput_df.rename(
    columns={
        'Throughput': 'Sub-column (Exact)',
        'Throughput_pso': 'Sub-column (PSO)',
    },
    inplace=True
)

subcolumn_df['Decoding Throughput'] = subcolumn_df['Points'] / \
    subcolumn_df['Decoding Time']
subcolumn_pso_df['Decoding Throughput'] = subcolumn_pso_df['Points'] / \
    subcolumn_pso_df['Decoding Time']

decompression_throughput_df = subcolumn_df.merge(
    subcolumn_pso_df[['Dataset', 'Decoding Throughput']],
    on='Dataset',
    how='left',
    suffixes=('', '_pso')
)
decompression_throughput_df.rename(
    columns={
        'Decoding Throughput': 'Sub-column (Exact)',
        'Decoding Throughput_pso': 'Sub-column (PSO)',
    },
    inplace=True
)

compression_ratio_df['Sub-column (Exact)'] = 1 / \
    compression_ratio_df['Sub-column (Exact)']
compression_ratio_df['Sub-column (PSO)'] = 1 / \
    compression_ratio_df['Sub-column (PSO)']

fontsize = 18
labelsize = 18
colors = ['#FF0000', '#008000']

hatches = ['/', '\\']

methods = ['Sub-column (Exact)', 'Sub-column (PSO)']
labels = ['Sub-column (Exact)', 'Sub-column (PSO)']


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


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

line_x_position = (x[0] + x[1]) / 2
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

legend_elements = [Patch(facecolor=colors[i], label=labels[i],
                         hatch=hatches[i]) for i in range(n_methods)]
fig.legend(
    handles=legend_elements,
    loc='upper center',
    ncol=1,
    bbox_to_anchor=(0.48, 1.15),
    columnspacing=0.1,
    labelspacing=0.1,
    handletextpad=0.1,
    fontsize=labelsize
)

plt.savefig('fig/R3O2_compare_pso.png', dpi=300, bbox_inches='tight')
plt.savefig('fig/R3O2_compare_pso.eps', format='eps',
            dpi=300, bbox_inches='tight')
