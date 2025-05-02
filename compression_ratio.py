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

df = pd.read_csv('result/compression_ratio/baseline.csv')
df2 = pd.read_csv('trans_data_result/compression_ratio/baseline.csv')

for col in df2.columns[1:]:
    df2[col] = 1 / df2[col]

df = pd.concat([df, df2], ignore_index=True)

bp_df = pd.read_csv('result/bp.csv')
bp_df2 = pd.read_csv('trans_data_result/bp.csv')
bp_df = pd.concat([bp_df, bp_df2], ignore_index=True)

df = df.merge(
    bp_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Compression Ratio': 'BP'},
    inplace=True
)

subcolumn_df = pd.read_csv('result/subcolumn.csv')
subcolumn_df2 = pd.read_csv('trans_data_result/subcolumn.csv')
subcolumn_df = pd.concat([subcolumn_df, subcolumn_df2], ignore_index=True)

df = df.merge(
    subcolumn_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Compression Ratio': 'Sub-column'},
    inplace=True
)

sprintz_subcolumn_df = pd.read_csv('result/sprintz_subcolumn.csv')
sprintz_subcolumn_df2 = pd.read_csv('trans_data_result/sprintz_subcolumn.csv')
sprintz_subcolumn_df = pd.concat(
    [sprintz_subcolumn_df, sprintz_subcolumn_df2], ignore_index=True)

df = df.merge(
    sprintz_subcolumn_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Compression Ratio': 'SPRINTZ+Sub-column'},
    inplace=True
)

ts2diff_subcolumn_df = pd.read_csv('result/ts2diff_subcolumn.csv')
ts2diff_subcolumn_df2 = pd.read_csv('trans_data_result/ts2diff_subcolumn.csv')
ts2diff_subcolumn_df = pd.concat(
    [ts2diff_subcolumn_df, ts2diff_subcolumn_df2], ignore_index=True)

df = df.merge(
    ts2diff_subcolumn_df[['Dataset', 'Compression Ratio']],
    on='Dataset',
    how='left'
)
df.rename(columns={'Compression Ratio': 'TS2DIFF+Sub-column'}, inplace=True)

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

for col in df.columns[1:]:
    df[col] = 1 / df[col]

df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

# print(df)

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
plt.ylabel('Compression Ratio', fontsize=fontsize)

x_min = x[0] - width
x_max = x[-1] + (len(combined_df.columns[1:]) * width)
plt.xlim(x_min, x_max)

plt.legend(
    loc='upper center',
    ncol=len(combined_df.columns[1:]),
    bbox_to_anchor=(0.47, 1.38),
    fontsize=fontsize,
    columnspacing=2.6,
    ncols=6
)

plt.savefig(
    'fig/dataset_compression_ratio.png',
    dpi=1000,
    bbox_inches='tight'
)

plt.savefig(
    'fig/dataset_compression_ratio.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
