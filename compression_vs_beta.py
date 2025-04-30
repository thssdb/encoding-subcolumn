import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

dataset_abbreviations = {
    'Air-pressure': 'AP',
    'Bird-migration': 'BM',
    'Bitcoin-price': 'BP',
    'Blockchain-tr': 'BTR',
    'City-temp': 'CT',
    'Dewpoint-temp': 'DT',
    'IR-bio-temp': 'IR',
    'PM10-dust': 'PM10',
    'Stocks-DE': 'SDE',
    'Stocks-UK': 'SUK',
    'Stocks-USA': 'SUSA',
    'Wind-Speed': 'WS'
}

ax1: Axes
ax2: Axes
ax3: Axes
fig, (ax1, ax2, ax3) = plt.subplots(
    1,
    3,
    figsize=(24, 6)
)

beta_list = list(range(1, 32))

fontsize = 20
labelsize = 20

file_names = [
    f'./result/compression_vs_beta/subcolumn_beta_{beta}.csv' for beta in beta_list]

colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffc107',
          '#a65628', '#f781bf', '#999999', '#66c2a5', '#fc8d62', '#8da0cb']
markers = ['o', 's', 'D', '^', 'v', '>', '<', 'p', 'h', 'H', 'd', '*']

# ax1
compression_ratios = {}
for file_name, beta in zip(file_names, beta_list):
    df = pd.read_csv(file_name)
    df['Dataset'] = df['Dataset'].map(dataset_abbreviations)
    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']
        if dataset not in compression_ratios:
            compression_ratios[dataset] = []
        compression_ratios[dataset].append((beta, compression_ratio))

for i, (dataset, ratios) in enumerate(compression_ratios.items()):
    ratios = sorted(ratios, key=lambda x: x[0])
    beta = [x[0] for x in ratios]
    compression_values = [x[1] for x in ratios]
    max_ratio_index = compression_values.index(max(compression_values))

    color = colors[i]
    marker = markers[i]

    ax1.plot(
        beta,
        compression_values,
        marker=marker,
        label=dataset,
        color=color
    )
    ax1.plot(
        beta[max_ratio_index],
        compression_values[max_ratio_index],
        marker=marker,
        color=color,
        markerfacecolor='white'
    )

ax1.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax1.set_xlabel('Bit Width β', fontsize=fontsize)
ax1.set_ylabel('Compression Ratio', fontsize=fontsize)
ax1.set_title('(a) Compression ratio', fontsize=fontsize)
ax1.set_xticks(beta[::3])

# ax2
compression_times = {}
for file_name, beta in zip(file_names, beta_list):
    df = pd.read_csv(file_name)
    df['Dataset'] = df['Dataset'].map(dataset_abbreviations)
    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_time = row['Encoding Time'] / row['Points']
        if dataset not in compression_times:
            compression_times[dataset] = []
        compression_times[dataset].append((beta, compression_time))

for i, (dataset, ratios) in enumerate(compression_times.items()):
    ratios = sorted(ratios, key=lambda x: x[0])
    beta = [x[0] for x in ratios]
    compression_values = [x[1] for x in ratios]

    color = colors[i]
    marker = markers[i]

    ax2.plot(
        beta,
        compression_values,
        marker=marker,
        label=dataset,
        color=color
    )

ax2.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax2.set_xlabel('Bit Width β', fontsize=fontsize)
ax2.set_ylabel('Compression Time (ns/point)', fontsize=fontsize)
ax2.set_title('(b) Compression time', fontsize=fontsize)
ax2.set_xticks(beta[::3])

# ax3
decompression_times = {}
for file_name, beta in zip(file_names, beta_list):
    df = pd.read_csv(file_name)
    df['Dataset'] = df['Dataset'].map(dataset_abbreviations)
    for index, row in df.iterrows():
        dataset = row['Dataset']
        decompression_time = row['Decoding Time'] / row['Points']
        if dataset not in decompression_times:
            decompression_times[dataset] = []
        decompression_times[dataset].append((beta, decompression_time))

for i, (dataset, ratios) in enumerate(decompression_times.items()):
    ratios = sorted(ratios, key=lambda x: x[0])
    beta = [x[0] for x in ratios]
    compression_values = [x[1] for x in ratios]

    color = colors[i]
    marker = markers[i]

    ax3.plot(
        beta,
        compression_values,
        marker=marker,
        label=dataset,
        color=color
    )

ax3.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax3.set_xlabel('Bit Width β', fontsize=fontsize)
ax3.set_ylabel('Decompression Time (ns/point)', fontsize=fontsize)
ax3.set_title('(c) Decompression time', fontsize=fontsize)
ax3.set_xticks(beta[::3])

handles, labels = ax1.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='upper center',
    ncol=12,
    bbox_to_anchor=(0.5, 1.07),
    columnspacing=0.68,
    fontsize=fontsize
)

plt.savefig(
    './fig/beta_comparison.png',
    dpi=1000,
    bbox_inches='tight'
)
plt.savefig(
    './fig/beta_comparison.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
# plt.show()
