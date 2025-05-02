import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dataset_abbreviations = {
    'Bird-migration': 'BM',
    'Bitcoin-price': 'BP',
    'City-temp': 'CT',
    'Dewpoint-temp': 'DT',
    'IR-bio-temp': 'IR',
    'PM10-dust': 'PM10',
    'Stocks-DE': 'SDE',
    'Stocks-UK': 'SUK',
    'Stocks-USA': 'SUSA',
    'Wind-Speed': 'WS',
    'EPM-Education': 'EE',
    'Wine-Tasting': 'WT',
}

df = pd.read_csv('result/decompression_time/baseline.csv')
df2 = pd.read_csv('trans_data_result/decompression_time/baseline.csv')

bp_df = pd.read_csv('result/bp.csv')
bp_df2 = pd.read_csv('trans_data_result/bp.csv')
bp_df = pd.concat([bp_df, bp_df2], ignore_index=True)

bp_df['Decoding Time / Points'] = bp_df['Decoding Time'] / bp_df['Points']

df = df.merge(
    bp_df[['Dataset', 'Decoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Decoding Time / Points': 'BP'},
    inplace=True
)

subcolumn_df = pd.read_csv('result/subcolumn.csv')
subcolumn_df2 = pd.read_csv('trans_data_result/subcolumn.csv')
subcolumn_df = pd.concat([subcolumn_df, subcolumn_df2], ignore_index=True)

subcolumn_df['Decoding Time / Points'] = subcolumn_df['Decoding Time'] / \
    subcolumn_df['Points']

df = df.merge(
    subcolumn_df[['Dataset', 'Decoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Decoding Time / Points': 'Sub-column'},
    inplace=True
)

sprintz_subcolumn_df = pd.read_csv('result/sprintz_subcolumn.csv')
sprintz_subcolumn_df2 = pd.read_csv('trans_data_result/sprintz_subcolumn.csv')
sprintz_subcolumn_df = pd.concat(
    [sprintz_subcolumn_df, sprintz_subcolumn_df2], ignore_index=True)

sprintz_subcolumn_df['Decoding Time / Points'] = sprintz_subcolumn_df['Decoding Time'] / \
    sprintz_subcolumn_df['Points']

df = df.merge(
    sprintz_subcolumn_df[['Dataset', 'Decoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Decoding Time / Points': 'SPRINTZ+Sub-column'},
    inplace=True
)

ts2diff_subcolumn_df = pd.read_csv('result/ts2diff_subcolumn.csv')
ts2diff_subcolumn_df2 = pd.read_csv('trans_data_result/ts2diff_subcolumn.csv')
ts2diff_subcolumn_df = pd.concat(
    [ts2diff_subcolumn_df, ts2diff_subcolumn_df2], ignore_index=True)

ts2diff_subcolumn_df['Decoding Time / Points'] = ts2diff_subcolumn_df['Decoding Time'] / \
    ts2diff_subcolumn_df['Points']

df = df.merge(
    ts2diff_subcolumn_df[['Dataset', 'Decoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Decoding Time / Points': 'TS2DIFF+Sub-column'},
    inplace=True
)

buff_df = pd.read_csv('result/buff.csv')
buff_df2 = pd.read_csv('trans_data_result/buff.csv')
buff_df = pd.concat([buff_df, buff_df2], ignore_index=True)

buff_df['Decoding Time / Points'] = buff_df['Decoding Time'] / buff_df['Points']

df = df.merge(
    buff_df[['Dataset', 'Decoding Time / Points']],
    on='Dataset',
    how='left'
)
df['BUFF'] = df['Decoding Time / Points']

df = df[[
    'Dataset', 'GORILLA', 'CHIMP', 'Elf', 'RLE', 'BP', 'Sub-column',
    'SPRINTZ', 'SPRINTZ+Sub-column',
    'TS2DIFF', 'TS2DIFF+Sub-column',
    'BUFF',
]]
df.rename(
    columns={
        'BP': 'BPE',
        'SPRINTZ': 'SPRINTZ+BPE',
        'TS2DIFF': 'TS2DIFF+BPE',
    },
    inplace=True
)

# print(df)

df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

datasets = df['Dataset'].tolist()

# 找到EE和WT的索引
if 'EE' in datasets and 'WT' in datasets:
    ee_index = datasets.index('EE')
    wt_index = datasets.index('WT')

    # 交换EE和WT
    datasets[ee_index], datasets[wt_index] = datasets[wt_index], datasets[ee_index]

# 根据新的顺序重新排列DataFrame
combined_df = df.set_index('Dataset').loc[datasets].reset_index()

color_palette = [
    '#A5D6A7', '#90CAF9', '#CE93D8', '#BCAAA4', '#AED581', '#FF0000', '#81D4FA',
    '#FF6600', '#9575CD', '#FF9900', '#FFE082',
]

fontsize = 13

plt.figure(figsize=(15, 2.5))

x = np.arange(len(combined_df['Dataset'])) * \
    len(combined_df.columns[1:]) * 0.12
width = 0.1
hatches = ['*', '+', 'x',  '|', '-', '/', 'o', 'O',  '\\', '//', '.']

for i, column in enumerate(combined_df.columns[1:]):
    plt.bar(
        x + i * width,
        combined_df[column],
        width,
        label=column,
        color=color_palette[i],
        hatch=hatches[i]
    )

plt.xticks(
    x + (len(combined_df.columns[1:]) - 1) * width / 2,
    combined_df['Dataset'],
    fontsize=fontsize
)
plt.yticks(fontsize=fontsize)

plt.xlabel('Datasets', fontsize=fontsize)
plt.ylabel('Decompression Time (ns/point)', fontsize=fontsize)

x_min = x[0] - width
x_max = x[-1] + (len(combined_df.columns[1:]) * width)
plt.xlim(x_min, x_max)

plt.legend(
    loc='upper center',
    ncol=len(combined_df.columns[1:]),
    bbox_to_anchor=(0.47, 1.38),
    fontsize=fontsize,
    columnspacing=1.6,
    ncols=6
)

plt.savefig(
    'fig/dataset_decompression_time.png',
    dpi=1000,
    bbox_inches='tight'
)

plt.savefig(
    'fig/dataset_decompression_time.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)

# plt.show()
