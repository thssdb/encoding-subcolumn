import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df = pd.read_csv('./result/compression_time/baseline.csv')

bp_df = pd.read_csv('./result/bp.csv')
bp_df['Encoding Time / Points'] = bp_df['Encoding Time'] / bp_df['Points']

df = df.merge(
    bp_df[['Dataset', 'Encoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Encoding Time / Points': 'BP'},
    inplace=True
)

subcolumn_df = pd.read_csv('./result/subcolumn.csv')
subcolumn_df['Encoding Time / Points'] = subcolumn_df['Encoding Time'] / \
    subcolumn_df['Points']

df = df.merge(
    subcolumn_df[['Dataset', 'Encoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Encoding Time / Points': 'Sub-columns'},
    inplace=True
)

sprintz_subcolumn_df = pd.read_csv('./result/sprintz_subcolumn.csv')
sprintz_subcolumn_df['Encoding Time / Points'] = sprintz_subcolumn_df['Encoding Time'] / \
    sprintz_subcolumn_df['Points']

df = df.merge(
    sprintz_subcolumn_df[['Dataset', 'Encoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Encoding Time / Points': 'SPRINTZ+Sub-columns'},
    inplace=True
)

ts2diff_subcolumn_df = pd.read_csv('./result/ts2diff_subcolumn.csv')
ts2diff_subcolumn_df['Encoding Time / Points'] = ts2diff_subcolumn_df['Encoding Time'] / \
    ts2diff_subcolumn_df['Points']

df = df.merge(
    ts2diff_subcolumn_df[['Dataset', 'Encoding Time / Points']],
    on='Dataset',
    how='left'
)
df.rename(
    columns={'Encoding Time / Points': 'TS2DIFF+Sub-columns'},
    inplace=True
)

buff_df = pd.read_csv('./result/buff.csv')
buff_df['Encoding Time / Points'] = buff_df['Encoding Time'] / buff_df['Points']

df = df.merge(
    buff_df[['Dataset', 'Encoding Time / Points']],
    on='Dataset',
    how='left'
)
df['BUFF'] = df['Encoding Time / Points']

df = df[[
    'Dataset', 'Gorilla', 'Chimp', 'Elf', 'RLE', 'BP', 'Sub-columns',
    'SPRINTZ', 'SPRINTZ+Sub-columns',
    'TS2DIFF', 'TS2DIFF+Sub-columns',
    'BUFF',
]]
df.rename(
    columns={
        'SPRINTZ': 'SPRINTZ+BP',
        'TS2DIFF': 'TS2DIFF+BP'
    },
    inplace=True
)

df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

color_palette = [
    '#A5D6A7', '#90CAF9', '#CE93D8', '#BCAAA4', '#AED581', '#FF0000', '#81D4FA', '#FF6600', '#9575CD', '#FF9900', '#FFE082',
]

fontsize = 13

plt.figure(figsize=(15, 3.5))

x = np.arange(len(df['Dataset'])) * len(df.columns[1:]) * 0.12
width = 0.1
for i, column in enumerate(df.columns[1:]):
    plt.bar(
        x + i * width,
        df[column],
        width,
        label=column,
        color=color_palette[i]
    )

plt.xticks(
    x + (len(df.columns[1:]) - 1) * width / 2,
    df['Dataset'],
    fontsize=fontsize
)
plt.yticks(fontsize=fontsize)

plt.xlabel('Datasets', fontsize=fontsize)
plt.ylabel('Compression Time (ns/point)', fontsize=fontsize)

x_min = x[0] - width
x_max = x[-1] + (len(df.columns[1:]) * width)
plt.xlim(x_min, x_max)

plt.legend(
    loc='upper center',
    ncol=len(df.columns[1:]),
    bbox_to_anchor=(0.475, 1.28),
    fontsize=fontsize,
    columnspacing=2.6,
    ncols=6
)

plt.savefig(
    './fig/dataset_compression_time.png',
    dpi=1000,
    bbox_inches='tight'
)
plt.savefig(
    './fig/dataset_compression_time.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
# plt.show()
