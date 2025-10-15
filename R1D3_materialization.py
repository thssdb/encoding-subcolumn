import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Patch

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

beta_list = list(range(1, 32))

buff_df = pd.read_csv('result/materialization/subcolumn_materialization.csv')
buff_df['LM-pipelined per Point'] = buff_df['LM-pipelined'] / buff_df['Points']
buff_df['LM-parallel per Point'] = buff_df['LM-parallel'] / buff_df['Points']
buff_df['EM-pipelined per Point'] = buff_df['EM-pipelined'] / buff_df['Points']
buff_df['EM-parallel per Point'] = buff_df['EM-parallel'] / buff_df['Points']

cstore_df = pd.read_csv('result/materialization/cstore_materialization.csv')
cstore_df['Decoding Time per Point'] = cstore_df['Decoding Time'] / \
    cstore_df['Points']

cstore_df = cstore_df[['Dataset', 'Decoding Time per Point']]

buff_df = buff_df.merge(cstore_df, on='Dataset', how='left')

buff_df.rename(
    columns={'Decoding Time per Point': 'C-Store'}, inplace=True)

bitweaving_df = pd.read_csv(
    'result/materialization/bitweaving_materialization.csv')
bitweaving_df['Decoding Time per Point'] = bitweaving_df['Decoding Time'] / \
    bitweaving_df['Points']

bitweaving_df = bitweaving_df[['Dataset', 'Decoding Time per Point']]

buff_df = buff_df.merge(bitweaving_df, on='Dataset', how='left')

buff_df.rename(
    columns={'Decoding Time per Point': 'BitWeaving'}, inplace=True)

buff_df = buff_df[[
    'Dataset',
    'LM-pipelined per Point',
    'LM-parallel per Point',
    'EM-pipelined per Point',
    'EM-parallel per Point',
    'C-Store',
    'BitWeaving',
]]
buff_df.rename(
    columns={
        'LM-pipelined per Point': 'LM-pipelined',
        'LM-parallel per Point': 'LM-parallel',
        'EM-pipelined per Point': 'EM-pipelined',
        'EM-parallel per Point': 'EM-parallel',
    },
    inplace=True
)

labels = [
    'Sub-column',
    'Sub-column',
    'Sub-column',
    'Sub-column',
    'C-Store',
    'BitWeaving',
]

methods = [
    'LM-pipelined',
    'LM-parallel',
    'EM-pipelined',
    'EM-parallel',
    'C-Store',
    'BitWeaving',
]

buff_df = buff_df[buff_df['Dataset'].isin(
    dataset_abbreviations.keys())].reset_index(drop=True)

buff_df['Dataset'] = buff_df['Dataset'].map(dataset_abbreviations)

buff_df['Dataset'] = pd.Categorical(
    buff_df['Dataset'], categories=dataset_abbreviations.values(), ordered=True)

buff_df.sort_values('Dataset', inplace=True)

buff_df = buff_df.reset_index(drop=True)

data_to_plot1 = [
    buff_df['LM-pipelined'],
    buff_df['LM-parallel'],
    buff_df['EM-pipelined'],
    buff_df['EM-parallel'],
    buff_df['BitWeaving'],
    buff_df['C-Store'],
]

buff_df = buff_df[[
    'LM-pipelined',
    'LM-parallel',
    'EM-pipelined',
    'EM-parallel',
    'BitWeaving',
    'C-Store'
]]

axes: list[Axes]
fig, axes = plt.subplots(1, 1, figsize=(5, 5.5))


fontsize = 18
labelsize = 19

ax: Axes = axes

color_palette = [
    '#FF0000','#008000', "#AD62EE", "#2A90EA",  '#FF0000', '#FF0000',
]

hatches = ['/', '\\', '/', '\\', '/', '/']


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


rotation = 30
ha = 'right'

width = 1

bar_positions = np.arange(len(methods)) * width + np.array([0, 0, 0, 0, 0.7, 2.7])

means1, stds1 = calculate_stats(buff_df, methods)
bars1 = ax.bar(
    bar_positions,
    means1,
    width=width,
    capsize=8, color=color_palette, hatch=hatches, alpha=0.8, edgecolor='black', linewidth=1
)

ax.set_xticks([])

ax.set_ylabel('Query Time (ns/point)', fontsize=fontsize)
ax.tick_params(axis='y', labelsize=labelsize)

ax.text((bar_positions[1] + bar_positions[2]) / 2, ax.get_ylim()[0] - (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02, 
        'Sub-column', fontsize=fontsize, ha='center', va='top')

ax.text(bar_positions[4], ax.get_ylim()[0] - (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02, 
        'C-Store', fontsize=fontsize, ha='center', va='top')

ax.text(bar_positions[5], ax.get_ylim()[0] - (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02, 
        'BitWeaving', fontsize=fontsize, ha='center', va='top')

legend_handles = [Patch(facecolor=color_palette[i], label=methods[i],
                        hatch=hatches[i], edgecolor='black') for i in range(4)]

ax.legend(
    handles=legend_handles,
    labels=methods[:4],
    loc='upper center',
    bbox_to_anchor=(0.4, 1.23),
    ncol=2,
    fontsize=labelsize,
    columnspacing=0.2,
    labelspacing=0.2,
    handletextpad=0.2,
)

plt.savefig('fig/R1D3_materialization.png', dpi=1000, bbox_inches='tight')

plt.savefig('fig/R1D3_materialization.eps',
            format='eps', dpi=1000, bbox_inches='tight')
