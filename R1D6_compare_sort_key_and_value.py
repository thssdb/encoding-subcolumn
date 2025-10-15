import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df = pd.read_csv('result/subcolumn_long_on_sorted.csv')
df.rename(
    columns={'Compression Ratio': 'Sub-column (Sorted by key)',
             'Compression Ratio Sort': 'Sub-column (Sorted by value)'},
    inplace=True
)

rle_df = pd.read_csv('result/rle_long_on_sorted.csv')

rle_df.rename(
    columns={'Compression Ratio': 'RLE (Sorted by key)',
             'Compression Ratio Sort': 'RLE (Sorted by value)'},
    inplace=True
)

dictionary_df = pd.read_csv('result/dictionary_long_on_sorted.csv')
dictionary_df.rename(
    columns={'Compression Ratio': 'Dictionary (Sorted by key)',
             'Compression Ratio Sort': 'Dictionary (Sorted by value)'},
    inplace=True
)


df = df.merge(
    rle_df[['Dataset', 'RLE (Sorted by key)', 'RLE (Sorted by value)']],
    on='Dataset',
    how='left',
)
df = df.merge(
    dictionary_df[[
        'Dataset', 'Dictionary (Sorted by key)', 'Dictionary (Sorted by value)']],
    on='Dataset',
    how='left',
)

df = df[[
    'Dataset',
    'Dictionary (Sorted by key)',
    'Dictionary (Sorted by value)',
    'RLE (Sorted by key)',
    'RLE (Sorted by value)',
    'Sub-column (Sorted by key)',
    'Sub-column (Sorted by value)',
]]

for col in df.columns[1:]:
    df[col] = 1 / df[col]

df = df[df['Dataset'].isin(dataset_abbreviations.keys())
        ].reset_index(drop=True)

df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

df['Dataset'] = pd.Categorical(
    df['Dataset'], categories=dataset_abbreviations.values(), ordered=True)

df.sort_values('Dataset', inplace=True)

df = df.reset_index(drop=True)

color_palette = ['#FF0000', '#008000', '#FF0000', '#008000', '#FF0000',
                 '#008000', "#FFE082", '#BCAAA4', "#9C8CAB", '#FFE082', '#4B9CF9',]

methods = [
    'Sub-column (Sorted by key)',
    'Sub-column (Sorted by value)',
    'RLE (Sorted by key)',
    'RLE (Sorted by value)',
    'Dictionary (Sorted by key)',
    'Dictionary (Sorted by value)']


fontsize = 18


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


n_groups = 3
bars_per_group = 2
bar_width = 0.35
group_gap = 0.6
colors_key = '#FF0000'
colors_value = '#008000'

hatches = ['/', '\\']
labels = ['Sorted by key', 'Sorted by value']

positions = []
for g in range(n_groups):
    group_left = g * (bars_per_group * bar_width + group_gap)
    positions.append(group_left)
    positions.append(group_left + bar_width)

fig, ax2 = plt.subplots(figsize=(5, 4))
means1, stds1 = calculate_stats(df, methods)

bar_containers = []
for i, (pos, mean) in enumerate(zip(positions, means1)):
    color = colors_key if (i % 2 == 0) else colors_value
    hatch = hatches[i % 2]
    label = labels[i % 2]
    bar = ax2.bar(
        pos, mean, width=bar_width,
        edgecolor='black', linewidth=1,
        color=color, align='edge', hatch=hatch, label=label
    )
    bar_containers.append(bar)


pair_centers = [(positions[2*i] + positions[2*i+1] +
                 bar_width) / 2 for i in range(n_groups)]
ax2.set_xticks(pair_centers)
ax2.set_xticklabels(['Sub-column', 'RLE', 'Dictionary'],
                    rotation=0, ha='center', fontsize=fontsize)


plt.yticks(fontsize=fontsize)
plt.ylabel('Compression Ratio', fontsize=fontsize)

handles = [bar_containers[0], bar_containers[1]]

ax2.legend(handles=handles, loc='upper center',
           bbox_to_anchor=(0.44, 1.2), fontsize=fontsize, ncols=2,
           columnspacing=0.05,
           labelspacing=0.05,
           handletextpad=0.05,
           handlelength=0.8)


plt.savefig('fig/R1D6_sort_key_and_value.png', dpi=1000, bbox_inches='tight')

plt.savefig('fig/R1D6_sort_key_and_value.eps',
            format='eps', dpi=1000, bbox_inches='tight')
