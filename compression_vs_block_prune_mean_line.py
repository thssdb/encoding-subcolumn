import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

FONT_SIZE = 24
XTICK_FONT_SIZE = 22

plt.rcParams.update(
    {
        "font.size": FONT_SIZE,
        "axes.titlesize": FONT_SIZE,
        "axes.labelsize": FONT_SIZE,
        "xtick.labelsize": FONT_SIZE,
        "ytick.labelsize": FONT_SIZE,
        "legend.fontsize": FONT_SIZE,
        "legend.title_fontsize": FONT_SIZE,
        "figure.titlesize": FONT_SIZE,
    }
)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 4))
plt.subplots_adjust(wspace=0.35, top=0.88)

block_sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

file_names_1 = [
    f'result/compression_vs_block_noprune/subcolumn_block_{size}.csv' for size in block_sizes
]

compression_ratios_1 = {}
encoding_times_1 = {}
decoding_times_1 = {}

for file_name, block_size in zip(file_names_1, block_sizes):
    df = pd.read_csv(file_name)
    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']
        encoding_time = row['Encoding Time'] / row['Points']
        decoding_time = row['Decoding Time'] / row['Points']

        if dataset not in compression_ratios_1:
            compression_ratios_1[dataset] = []
            encoding_times_1[dataset] = []
            decoding_times_1[dataset] = []

        compression_ratios_1[dataset].append((block_size, compression_ratio))
        encoding_times_1[dataset].append((block_size, encoding_time))
        decoding_times_1[dataset].append((block_size, decoding_time))

file_names_2 = [
    f'result/compression_vs_block_prune_fast/subcolumn_block_{size}.csv' for size in block_sizes
]

compression_ratios_2 = {}
encoding_times_2 = {}
decoding_times_2 = {}

for file_name, block_size in zip(file_names_2, block_sizes):
    df = pd.read_csv(file_name)
    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']
        encoding_time = row['Encoding Time'] / row['Points']
        decoding_time = row['Decoding Time'] / row['Points']

        if dataset not in compression_ratios_2:
            compression_ratios_2[dataset] = []
            encoding_times_2[dataset] = []
            decoding_times_2[dataset] = []

        compression_ratios_2[dataset].append((block_size, compression_ratio))
        encoding_times_2[dataset].append((block_size, encoding_time))
        decoding_times_2[dataset].append((block_size, decoding_time))

data_compression = []
data_encoding = []
data_decoding = []

for dataset, ratios in compression_ratios_1.items():
    for block_size, ratio in ratios:
        data_compression.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Compression Ratio': ratio,
            'Type': 'Without Pruning'
        })

for dataset, ratios in compression_ratios_2.items():
    for block_size, ratio in ratios:
        data_compression.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Compression Ratio': ratio,
            'Type': 'With Pruning'
        })

for dataset, times in encoding_times_1.items():
    for block_size, time in times:
        data_encoding.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Time (ns/point)': time,
            'Type': 'Without Pruning'
        })

for dataset, times in encoding_times_2.items():
    for block_size, time in times:
        data_encoding.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Time (ns/point)': time,
            'Type': 'With Pruning'
        })

for dataset, times in decoding_times_1.items():
    for block_size, time in times:
        data_decoding.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Time (ns/point)': time,
            'Type': 'Without Pruning'
        })

for dataset, times in decoding_times_2.items():
    for block_size, time in times:
        data_decoding.append({
            'Block Size': f'2^{int(np.log2(block_size))}',
            'Time (ns/point)': time,
            'Type': 'With Pruning'
        })

df_compression = pd.DataFrame(data_compression)
df_encoding = pd.DataFrame(data_encoding)
df_decoding = pd.DataFrame(data_decoding)
shared_decoding_by_block = {
    lbl: df_decoding[df_decoding['Block Size'] == lbl]['Time (ns/point)'].mean()
    for lbl in [f'2^{int(np.log2(size))}' for size in block_sizes]
}
shared_decoding_overall = df_decoding['Time (ns/point)'].mean()

block_size_labels = [f'2^{int(np.log2(size))}' for size in block_sizes]
color_mapping = {
    'Without Pruning': '#0A94EA',
    'With Pruning': '#FF0000'
}

x = np.arange(len(block_sizes))
MARKER_SIZE = 8


def _mean_line(ax, df, ycol):

    series_zorder = {'With Pruning': (1, 2), 'Without Pruning': (3, 4)}
    for type_name in ('With Pruning', 'Without Pruning'):
        color = color_mapping[type_name]
        line_z, marker_z = series_zorder[type_name]
        if ycol == 'Shared Decoding Time':
            yvals = [shared_decoding_overall for _ in block_size_labels]
        else:
            yvals = [
                df[(df['Block Size'] == lbl) & (df['Type'] == type_name)][ycol].mean()
                for lbl in block_size_labels
            ]
        ax.plot(x, yvals, color=color, linewidth=2, zorder=line_z)
        if type_name == 'Without Pruning':
            ax.plot(
                x, yvals, color=color, linestyle='None', marker='x',
                markersize=MARKER_SIZE, zorder=marker_z,
            )
        else:
            ax.plot(
                x, yvals, color=color, linestyle='None', marker='o',
                markersize=MARKER_SIZE, markerfacecolor='white',
                markeredgecolor=color, markeredgewidth=2, zorder=marker_z,
            )


_mean_line(ax1, df_compression, 'Compression Ratio')

ax1.set_xticks(x)
ax1.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in block_sizes],
    fontsize=XTICK_FONT_SIZE
)

ax1.set_xlabel('Number of values $n$')
ax1.set_ylabel('Compression Ratio')
ax1.set_title('(a) Compression ratio')
ax1.set_ylim(bottom=0)


_mean_line(ax2, df_encoding, 'Time (ns/point)')

ax2.set_xticks(x)
ax2.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in block_sizes],
    fontsize=XTICK_FONT_SIZE
)
ax2.set_xlabel('Number of values $n$')
ax2.set_ylabel('Time (ns/point)')
ax2.set_title('(b) Compression time')
ax2.set_ylim(bottom=0)


_mean_line(ax3, df_decoding, 'Shared Decoding Time')

ax3.set_xticks(x)
ax3.set_xticklabels(
    [r'2$^{' + f'{int(np.log2(size))}' + '}$' for size in block_sizes],
    fontsize=XTICK_FONT_SIZE
)
ax3.set_xlabel('Number of values $n$')
ax3.set_ylabel('Time (ns/point)')
ax3.set_title('(c) Decompression time',x=0.4)
ax3.set_ylim(bottom=0)


legend_elements = [
    Line2D(
        [0], [0], color=color_mapping['Without Pruning'], marker='x', linestyle='-',
        linewidth=2, markersize=8, label='Sub-column (Without pruning)',
    ),
    Line2D(
        [0], [0], color=color_mapping['With Pruning'], marker='o', linestyle='-',
        linewidth=2, markersize=MARKER_SIZE, markerfacecolor='white',
        markeredgewidth=2, label='Sub-column (With pruning)',
    ),
]

fig.legend(
    handles=legend_elements,
    loc='upper center',
    ncol=2,
    bbox_to_anchor=(0.5, 1.2),
    frameon=True,
)


plt.savefig(
    'fig/block_size_comparison_pruning_mean_line.png',
    dpi=300, bbox_inches='tight'
)
plt.savefig(
    'fig/block_size_comparison_pruning_mean_line.eps',
    format='eps', dpi=300, bbox_inches='tight'
)
