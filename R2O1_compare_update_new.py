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

subcolumn_df_append = pd.read_csv('result/update/subcolumn_append.csv')
subcolumn_df_insert_larger = pd.read_csv(
    'result/update/subcolumn_update_larger.csv')
subcolumn_df_insert_smaller = pd.read_csv(
    'result/update/subcolumn_update_smaller.csv')
subcolumn_df_insert_larger['Update Time (Larger Value)'] = subcolumn_df_insert_larger['Insert Time with Sub-column']
subcolumn_df_insert_smaller['Update Time (Smaller Value)'] = subcolumn_df_insert_smaller['Insert Time with Sub-column']

time_update_df = subcolumn_df_append.merge(
    subcolumn_df_insert_larger[['Dataset', 'Update Time (Larger Value)']],
    on='Dataset',
    how='left',
)
time_update_df = time_update_df.merge(
    subcolumn_df_insert_smaller[['Dataset', 'Update Time (Smaller Value)']],
    on='Dataset',
    how='left',
)

time_update_df['Append-only Time'] = time_update_df['Append-only Time with Sub-column'] / \
    time_update_df['Remaining Points']

time_update_df = time_update_df[[
    'Dataset',
    'Append-only Time',
    'Update Time (Smaller Value)',
    'Update Time (Larger Value)',
]]

time_update_df = time_update_df[time_update_df['Dataset'].isin(
    dataset_abbreviations.keys())].reset_index(drop=True)

time_update_df['Dataset'] = time_update_df['Dataset'].map(
    dataset_abbreviations)

time_update_df['Dataset'] = pd.Categorical(
    time_update_df['Dataset'], categories=dataset_abbreviations.values(), ordered=True)

time_update_df.sort_values('Dataset', inplace=True)

time_update_df = time_update_df.reset_index(drop=True)
data_to_plot3 = [
    time_update_df['Append-only Time'],
    time_update_df['Update Time (Smaller Value)'],
    time_update_df['Update Time (Larger Value)']
]
labels3 = ['Append-only', 'Update (Smaller)', 'Update (Larger)']

color_palette = ['#FF0000', "#AD62EE", "#2A90EA", '#008000']
fontsize = 16
labelsize = 16
fig, ax1 = plt.subplots(1, 1, figsize=(3.7, 3))
plt.subplots_adjust(wspace=0.4)


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


methods = time_update_df.columns[1:]
rotation = 30
ha = 'right'
colors = ['#FF0000', '#008000', "#AD62EE",
          '#4ECDC4', '#FFA500', "#0A94EA", "#43FFFF"]

hatches = ['/' if i % 2 == 0 else '\\' for i in range(len(methods))]

means1, stds1 = calculate_stats(time_update_df, methods)
bars4 = ax1.bar(range(len(methods)), means1,
                color=colors, hatch=hatches, edgecolor='black', linewidth=1, label=methods)

ax1.set_ylabel('Time (ns/point)', fontsize=fontsize)
ax1.set_xticks([])
ax1.tick_params(axis='y', labelsize=labelsize)
ax1.set_yscale('log')

handles, labels = ax1.get_legend_handles_labels()

ax1.legend(
    handles=handles,
    labels=labels,
    loc='upper center',
    bbox_to_anchor=(0.37, 1.38),
    ncol=1,
    fontsize=fontsize-2,
    columnspacing=0.1,
    labelspacing=0.1,
    handletextpad=0.1,
)


plt.savefig('fig/R2O1_compare_update.png', dpi=300, bbox_inches='tight')
plt.savefig('fig/R2O1_compare_update.eps',
            format='eps', dpi=300, bbox_inches='tight')
