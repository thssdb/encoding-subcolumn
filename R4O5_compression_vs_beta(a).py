import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.path as mpath

heart_vertices = [
    (0, 0), (0.5, 0.5), (1, 0), (0.5, -0.5), (0, 0),
    (-0.5, -0.5), (-1, 0), (-0.5, 0.5), (0, 0)
]

heart = mpath.Path(heart_vertices)

dataset_abbreviations = {
    'Arade4': 'Arade',
    'Bird-migration': 'BM',
    'Bitcoin-price': 'BP',
    'City-temp': 'CT',
    'Dewpoint-temp': 'DT',
    'EPM-Education': 'EE',
    'Gov10': 'Gov',
    'POI-lat': 'PLAT',
    'IR-bio-temp': 'IR',
    'PM10-dust': 'PM10',
    'Stocks-DE': 'SDE',
    'Stocks-UK': 'SUK',
    'Stocks-USA': 'SUSA',
    'Wind-Speed': 'WS',
    'Wine-Tasting': 'WT',
}
t = np.linspace(0, 2*np.pi, 100)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
x = x / np.max(np.abs(x))
y = y / np.max(np.abs(y))

heart_parametric = mpath.Path(np.column_stack([x, y]))
trapezoid_vertices = [
    (-0.8, -1),
    (0.8, -1),
    (0.4, 1),
    (-0.4, 1),
    (-0.8, -1)
]

trapezoid = mpath.Path(trapezoid_vertices)
parallelogram_vertices = [
    (-1, -0.6),
    (0.5, -0.6),
    (1, 0.6),
    (-0.5, 0.6),
    (-1, -0.6)
]

parallelogram = mpath.Path(parallelogram_vertices)

colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffc107',
          '#a65628', '#f781bf', '#999999', '#66c2a5', '#fc8d62', '#8da0cb',
          '#ff69b4', '#8b0000', '#00ced1']
markers = ['o', 's', 'D', '^', 'v', '>', '<', 'p', 'h', 'H', 'd', '*',
           'X', 'P', '8']
markers = [heart_parametric, 'o', 's', '^', 'v', '>', '<',  'D', 'p', '*', 'X', 'P', 'd',
           trapezoid,  parallelogram_vertices, '1', '2', '3', '4', '|', '_']

dataset_marker_color_map = {dataset: (markers[i % len(markers)], colors[i % len(colors)])
                            for i, dataset in enumerate(dataset_abbreviations.values())}

ax1: Axes
fig, (ax1) = plt.subplots(
    1,
    1,
    figsize=(8, 5)
)

beta_list = list(range(1, 32))

fontsize = 20
labelsize = 20

file_names = [
    f'result/compression_vs_beta/subcolumn_beta_{beta}.csv' for beta in beta_list]

compression_ratios = {}

for file_name, beta in zip(file_names, beta_list):
    df = pd.read_csv(file_name)
    df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

    df['Dataset'] = pd.Categorical(
        df['Dataset'],
        categories=dataset_abbreviations.values(),
        ordered=True
    )
    df = df.sort_values('Dataset')

    for index, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']
        if dataset not in compression_ratios:
            compression_ratios[dataset] = []
        compression_ratios[dataset].append((beta, compression_ratio))

beta_31_ratios = {dataset: ratios[-1][1] for dataset,
                  ratios in compression_ratios.items() if len(ratios) == 31}
sorted_datasets = sorted(beta_31_ratios, key=beta_31_ratios.get, reverse=True)
marker_size = 12
for dataset in sorted_datasets:
    ratios = compression_ratios[dataset]
    ratios = sorted(ratios, key=lambda x: x[0])
    beta = [x[0] for x in ratios]
    compression_values = [x[1] for x in ratios]
    max_ratio_index = compression_values.index(max(compression_values))

    marker, color = dataset_marker_color_map[dataset]
    ax1.plot(
        beta,
        compression_values,
        marker=marker,
        markersize=marker_size,
        label=dataset,
        color=color,
        markerfacecolor='none',
        markeredgecolor=color,
    )
    ax1.plot(
        beta[max_ratio_index],
        compression_values[max_ratio_index],
        marker=marker,
        color=color,
        markersize=marker_size,
        markerfacecolor=color,
        markeredgecolor=color
    )


ax1.tick_params(
    axis='both',
    which='major',
    labelsize=labelsize
)
ax1.set_xlabel(r'Bit Width $\beta$', fontsize=fontsize)
ax1.set_ylabel('Compression Ratio', fontsize=fontsize)
ax1.set_xticks(beta[::3])

handles, labels = ax1.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='center left',
    ncol=1,
    bbox_to_anchor=(0.9, 0.43),
    labelspacing=0.1,
    handletextpad=0.3,
    fontsize=fontsize
)

plt.savefig('fig/R4O5_beta_comparison.png', dpi=1000, bbox_inches='tight')
plt.savefig('fig/R4O5_beta_comparison.eps',
            format='eps', dpi=1000, bbox_inches='tight')
