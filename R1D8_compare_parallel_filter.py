import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

dataset_abbreviations = {
    'Arade4': 'Arade',
    'Bird-migration': 'BM',
    'Bitcoin-price': 'BP',
    'City-temp': 'CT',
    'Dewpoint-temp': 'DT',
    'EPM-Education': 'EE',
    'Gov10': 'Gov',
    'IR-bio-temp': 'IR',
    'PM10-dust': 'PM10',
    'POI-lat': 'PLAT',
    'Stocks-DE': 'SDE',
    'Stocks-UK': 'SUK',
    'Stocks-USA': 'SUSA',
    'Wind-Speed': 'WS',
    'Wine-Tasting': 'WT',
}

df = pd.read_csv('result/subcolumn_filter.csv')


df['Filter in pipeline'] = df['LM-pipelined'] / df['Points']
df['Filter in parallel'] = df['LM-parallel'] / df['Points']
df = df[[
    'Dataset',
    'Filter in pipeline',
    'Filter in parallel',
    'Selectivity',
    'Phi'
]]
df.rename(
    columns={
        'Selectivity': r'Selectivity ($\tau$)',
        'Phi': r'Correlation ($\phi$)',
    },
    inplace=True
)


df = df[df['Dataset'].isin(dataset_abbreviations.keys())
        ].reset_index(drop=True)

df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

df['Dataset'] = pd.Categorical(
    df['Dataset'], categories=dataset_abbreviations.values(), ordered=True)

df.sort_values('Dataset', inplace=True)

df = df.reset_index(drop=True)

df.sort_values('Dataset', inplace=True)
df = df.reset_index(drop=True)

color_palette = ['#FF0000', '#008000', "#AD62EE", "#2A90EA"]

fontsize = 18

ax1: Axes
ax2: Axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

x = np.arange(len(df['Dataset'])) * \
    len(df.columns[1:3]) * 0.12
width = 0.1
hatches = ['/' if i %
           2 == 0 else '\\' for i in range(len(df.columns[1:]))]

for i, column in enumerate(df.columns[1:3]):
    ax1.bar(
        x + i * width,
        df[column],
        width,
        label=column,
        color=color_palette[i],
        hatch=hatches[i]
    )

ax1.set_ylabel('Time (ns/point)', fontsize=fontsize)
ax1.tick_params(axis='y', labelsize=fontsize)
ax1.set_title("(a) Query Time", fontsize=fontsize)

x2 = np.arange(len(df['Dataset'])) * \
    len(df.columns[3:]) * 0.12
width2 = 0.1

for i, column in enumerate(df.columns[3:]):
    ax2.bar(
        x2 + i * width2,
        df[column],
        width2,
        label=column,
        color=color_palette[i+2],
        hatch=hatches[i]
    )
ax2.axhline(y=1, color='black', linestyle='--')
ax2.axhline(y=0, color='black', linestyle='--')
ax2.set_title("(b) Coefficients", fontsize=fontsize)
ax2.tick_params(axis='y', labelsize=fontsize)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

fig.legend(handles, labels, loc='upper center',
           ncol=4, bbox_to_anchor=(0.47, 1.04),
           columnspacing=0.1,
           labelspacing=0.1,
           handletextpad=0.1, fontsize=fontsize-2)


plt.setp(ax1.get_xticklabels(), visible=False)

plt.xticks(
    x + (len(df.columns[1:3]) - 1) * width / 2,
    df['Dataset'],
    fontsize=fontsize
)
plt.xticks(fontsize=fontsize-3,  ha="center")

x_min = x[0] - width
x_max = x[-1] + (len(df.columns[1:3]) * width)
plt.xlim(x_min, x_max)

plt.subplots_adjust(hspace=0.2)

plt.savefig('fig/R1D8_parallel_filter.png', dpi=1000, bbox_inches='tight')

plt.savefig('fig/R1D8_parallel_filter.eps',
            format='eps', dpi=1000, bbox_inches='tight')
