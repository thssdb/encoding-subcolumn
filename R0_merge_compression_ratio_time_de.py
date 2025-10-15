import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

fontsize = 12

axes: list[Axes]

fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))

df_ratio = pd.read_csv('result/compression_ratio/baseline.csv')

algorithms = {
    'BP': 'result/bp.csv',
    'Sub-column': 'result/subcolumn.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn.csv',
    'RLE': 'result/rle.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
}

for algo_name, file_path in algorithms.items():
    algo_df = pd.read_csv(file_path)
    algo_df.rename(columns={'Compression Ratio': algo_name}, inplace=True)
    df_ratio = df_ratio.merge(
        algo_df[['Dataset', algo_name]],
        on='Dataset',
        how='left'
    )


df_ratio.rename(columns={
    'BP': 'BPE',
    'SPRINTZ': 'SPRINTZ+BPE',
    'TS2DIFF': 'TS2DIFF+BPE',
}, inplace=True)

df_ratio = df_ratio[df_ratio['Dataset'].isin(
    dataset_abbreviations.keys())].reset_index(drop=True)
df_ratio['Dataset'] = df_ratio['Dataset'].map(dataset_abbreviations)


for col in df_ratio.columns[1:]:
    df_ratio[col] = 1 / df_ratio[col]

df_ratio_long = pd.melt(df_ratio, id_vars=[
                        'Dataset'], var_name='Algorithm', value_name='Compression Ratio')

colors = [
    '#A5D6A7',
    '#90CAF9',
    '#8A2BE2',
    '#FFD700',
    "#43FFFF",
    "#0A94EA",
    '#008000',
    '#FF0000',
    '#81D4FA',
    '#FF6600',
    '#AD62EE',
    '#FF9900',
]

hatches = ['/' if i % 2 == 0 else '\\' for i in range(len(colors))]


alg_order = [
    'GORILLA',
    'CHIMP',
    'Elf',
    'BUFF',
    'ALP',
    'RLE',
    'BPE',
    'Sub-column',
    'SPRINTZ+BPE',
    'SPRINTZ+Sub-column',
    'TS2DIFF+BPE',
    'TS2DIFF+Sub-column',
]

color_mapping = {alg: colors[i] for i, alg in enumerate(alg_order)}

sns.boxplot(data=df_ratio_long, x='Algorithm', y='Compression Ratio', ax=axes[0],
            order=alg_order,
            palette=color_mapping,
            hue='Algorithm',
            legend=False)

for i, patch in enumerate(axes[0].patches):
    hatch = hatches[i % len(hatches)]
    patch.set_hatch(hatch)

axes[0].set_title('(a) Compression Ratio', fontsize=fontsize)
axes[0].set_xticks([])
axes[0].set_yticks(axes[0].get_yticks())
axes[0].set_yticklabels(axes[0].get_yticklabels(), fontsize=fontsize)
axes[0].set_xlabel('', fontsize=fontsize)
axes[0].set_ylabel('Compression Ratio', fontsize=fontsize)
for lbl in axes[0].get_xticklabels():
    x, y = lbl.get_position()
    lbl.set_y(y+0.02)

df_encode = pd.read_csv('result/compression_time/baseline.csv')
df_encode.iloc[:, 1:] = 1 / df_encode.iloc[:, 1:].astype(float)

encode_algorithms = {
    'RLE': 'result/rle.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
    'BP': 'result/bp.csv',
    'Sub-column': 'result/subcolumn.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn.csv',
    'BUFF': 'result/buff.csv',
    'ALP': 'result/alp.csv'
}

for algo_name, file_path in encode_algorithms.items():
    algo_df = pd.read_csv(file_path)
    algo_df['Points / Encoding Time'] = algo_df['Points'] / \
        algo_df['Encoding Time']
    df_encode = df_encode.merge(
        algo_df[['Dataset', 'Points / Encoding Time']],
        on='Dataset',
        how='left'
    )
    df_encode.rename(
        columns={'Points / Encoding Time': algo_name}, inplace=True)

df_encode.rename(columns={
    'BP': 'BPE',
    'SPRINTZ': 'SPRINTZ+BPE',
    'TS2DIFF': 'TS2DIFF+BPE',
}, inplace=True)

plt.subplots_adjust(wspace=0.3)

df_encode = df_encode[df_encode['Dataset'].isin(
    dataset_abbreviations.keys())].reset_index(drop=True)
df_encode['Dataset'] = df_encode['Dataset'].map(dataset_abbreviations)

df_encode_long = pd.melt(
    df_encode, id_vars=['Dataset'], var_name='Algorithm', value_name='Throughput')

sns.boxplot(data=df_encode_long, x='Algorithm', y='Throughput', ax=axes[1],
            order=alg_order,
            palette=color_mapping,
            hue='Algorithm',
            legend=False)

for i, patch in enumerate(axes[1].patches):
    hatch = hatches[i % len(hatches)]
    patch.set_hatch(hatch)

axes[1].set_title('(b) Compression Throughput', fontsize=fontsize)  # ,x=0.3
axes[1].set_xticks([])
axes[1].set_yticks(axes[1].get_yticks())
axes[1].set_yticklabels(axes[1].get_yticklabels(), fontsize=fontsize)
axes[1].set_xlabel('', fontsize=fontsize)
axes[1].set_ylabel('Throughput (point/ns)', fontsize=fontsize)
axes[1].set_ylim(0.0009, 1.1)
axes[1].set_yscale('log')
for lbl in axes[1].get_xticklabels():
    x, y = lbl.get_position()
    lbl.set_y(y+0.02)

df_decode = pd.read_csv('result/decompression_time/baseline.csv')
df_decode.iloc[:, 1:] = 1 / df_decode.iloc[:, 1:].astype(float)

decode_algorithms = {
    'RLE': 'result/rle.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
    'BP': 'result/bp.csv',
    'Sub-column': 'result/subcolumn.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn.csv',
    'BUFF': 'result/buff.csv',
    'ALP': 'result/alp.csv'
}

for algo_name, file_path in decode_algorithms.items():
    algo_df = pd.read_csv(file_path)
    algo_df['Points / Decoding Time'] = algo_df['Points'] / \
        algo_df['Decoding Time']
    df_decode = df_decode.merge(
        algo_df[['Dataset', 'Points / Decoding Time']],
        on='Dataset',
        how='left'
    )
    df_decode.rename(
        columns={'Points / Decoding Time': algo_name}, inplace=True)

df_decode.rename(columns={
    'BP': 'BPE',
    'SPRINTZ': 'SPRINTZ+BPE',
    'TS2DIFF': 'TS2DIFF+BPE',
}, inplace=True)

df_decode = df_decode[df_decode['Dataset'].isin(
    dataset_abbreviations.keys())].reset_index(drop=True)
df_decode['Dataset'] = df_decode['Dataset'].map(dataset_abbreviations)

df_decode_long = pd.melt(
    df_decode, id_vars=['Dataset'], var_name='Algorithm', value_name='Throughput')

sns.boxplot(data=df_decode_long, x='Algorithm', y='Throughput', ax=axes[2],
            order=alg_order,
            palette=color_mapping,
            hue='Algorithm',
            legend=False)

for i, patch in enumerate(axes[2].patches):
    hatch = hatches[i % len(hatches)]
    patch.set_hatch(hatch)

axes[2].set_title('(c) Decompression Throughput', fontsize=fontsize, x=0.5)
axes[2].set_xticks([])
axes[2].set_yticks(axes[2].get_yticks())
axes[2].set_yticklabels(axes[2].get_yticklabels(), fontsize=fontsize)
axes[2].set_xlabel('', fontsize=fontsize)
axes[2].set_ylabel('Throughput (point/ns)', fontsize=fontsize)
axes[2].set_ylim(0.0009, 1.1)
axes[2].set_yscale('log')
for lbl in axes[2].get_xticklabels():
    x, y = lbl.get_position()
    lbl.set_y(y+0.02)

legend_elements = [Patch(facecolor=color_mapping[alg], label=alg,
                         hatch=hatches[i]) for i, alg in enumerate(alg_order)]

fig.legend(
    handles=legend_elements,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.11),
    ncol=6,
    labelspacing=0.01,
    fontsize=fontsize,
)


plt.savefig('fig/merge_algorithm_comparison_boxplots.png',
            dpi=1000, bbox_inches='tight')
plt.savefig('fig/merge_algorithm_comparison_boxplots.eps',
            format='eps', dpi=1000, bbox_inches='tight')
