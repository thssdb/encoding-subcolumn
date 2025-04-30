import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

axes: np.ndarray
fig, axes = plt.subplots(
    2,
    3,
    figsize=(24, 13.5)
)

axes_flat = axes.flatten()

plt.subplots_adjust(
    hspace=0.25,
    wspace=0.2
)

beta_list = list(range(1, 32))

fontsize = 21
labelsize = 21

buff_value = 11.57

query_types = [
    ('greater', '(a) X > v'),
    ('less', '(b) X < v'),
    ('equal', '(c) X = v'),
    ('max', '(d) MAX(X)'),
    ('sum', '(e) SUM(X)'),
    ('count', '(f) COUNT(v)')
]

for i, (query_type, title) in enumerate(query_types):
    ax: Axes = axes_flat[i]

    file_names = [
        f'./result/query_vs_beta/subcolumn_query_{query_type}_beta_{beta}.csv' for beta in beta_list
    ]

    decoding_times = {}

    for file_name, beta in zip(file_names, beta_list):
        df = pd.read_csv(file_name)

        for index, row in df.iterrows():
            dataset = row['Dataset']
            time_per_point = row['Decoding Time'] / row['Points']

            if dataset not in decoding_times:
                decoding_times[dataset] = []

            decoding_times[dataset].append((beta, time_per_point))

    boxplot_data = {}
    for dataset, ratios in decoding_times.items():
        for beta, time in ratios:
            if beta not in boxplot_data:
                boxplot_data[beta] = []
            boxplot_data[beta].append(time)

    ax.boxplot(
        boxplot_data.values(),
        positions=boxplot_data.keys(),
        widths=0.4
    )

    medians = [np.median(data) for data in boxplot_data.values()]

    ax.plot(
        list(boxplot_data.keys()),
        medians,
        color='orange',
        linestyle='-',
        marker='o',
        linewidth=2,
        markersize=6
    )

    ax.axhline(
        y=buff_value,
        color='black',
        linestyle='--',
        label='BUFF'
    )
    ax.text(
        beta_list[-1],
        buff_value,
        'BUFF',
        color='black',
        fontsize=fontsize,
        verticalalignment='bottom',
        horizontalalignment='right'
    )

    if i == 5:
        current_ylim = ax.get_ylim()
        ax.set_ylim(top=current_ylim[1] * 1.05)

    ax.tick_params(
        axis='both',
        which='major',
        labelsize=labelsize
    )
    ax.set_xticks(list(boxplot_data.keys())[::3])
    ax.set_xticklabels([str(size) for size in boxplot_data.keys()][::3])
    ax.set_xlabel('Bit Width β', fontsize=fontsize)
    ax.set_ylabel('Query Time (ns/point)', fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)

plt.savefig(
    './fig/query_vs_beta.png',
    dpi=1000,
    bbox_inches='tight'
)
plt.savefig(
    './fig/query_vs_beta.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
# plt.show()
