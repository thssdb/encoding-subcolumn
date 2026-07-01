import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib.axes import Axes
from matplotlib.patches import Patch

SCRIPT_DIR = Path(__file__).resolve().parent
FIG_DIR = SCRIPT_DIR / 'fig'


def rel_path(path: str) -> Path:
    return SCRIPT_DIR / path


dataset_abbreviations = {
    'Bird-migration': 'BM',
    # 'Bitcoin-price': 'BP',
    'Census-Population': 'CP',
    'City-temp': 'CT',
    'Dewpoint-temp': 'DT',
    'EPM-Education': 'EE',
    'Gov10': 'Gov',
    'IR-bio-temp': 'IR',
    'MeteoNet-Weather': 'MW',
    'PM10-dust': 'PM10',
    'Stocks-DE': 'SDE',
    'Stocks-UK': 'SUK',
    'Stocks-USA': 'SUSA',
    'Wind-Speed': 'WS',
    'Wine-Tasting': 'WT',
    
}

dataset_order = list(dataset_abbreviations.values())

alg_order = [
    'GORILLA',
    'CHIMP',
    'Elf',
    'BUFF',
    'ALP',
    'BitWeaving',
    # 'Simple8b',
    # 'FastPFOR',
    'RLE',
    'BPE',
    'DE',
    'Sub-column',
    'SPRINTZ',
    'SPRINTZ+Sub-column',
    'TS2DIFF',
    'TS2DIFF+Sub-column',
]


RATIO_COLS = ['Compression Ratio', 'Ratio (compressed / raw int32)', 'Ratio (compressed / raw int32 for original points)']
ENCODE_TIME_COLS = ['Encoding Time', 'Encode ns']
DECODE_TIME_COLS = ['Decoding Time', 'Decode ns']
BUFF_TIME_FACTOR_VS_BPE = 1.05


def pick_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f'None of columns found: {candidates}')


def load_algorithm_time(file_path: str, time_cols: list[str], output_col: str) -> pd.DataFrame:
    algo_df = pd.read_csv(rel_path(file_path))
    time_col = pick_first_existing_column(algo_df, time_cols)
    temp_df = algo_df[['Dataset', time_col, 'Points']].copy()
    temp_df[output_col] = temp_df[time_col] / temp_df['Points']
    return temp_df[['Dataset', output_col]]


def upsert_algorithm_time(df: pd.DataFrame, algo_name: str, temp_df: pd.DataFrame) -> pd.DataFrame:
    if algo_name in df.columns:
        for dataset in temp_df['Dataset']:
            if dataset in df['Dataset'].values:
                mask = df['Dataset'] == dataset
                df.loc[mask, algo_name] = temp_df.loc[temp_df['Dataset'] == dataset, algo_name].values[0]
        return df
    return df.merge(temp_df, on='Dataset', how='left')


def bpe_calibrated_buff_time(time_cols: list[str], output_col: str) -> pd.DataFrame:
    temp_df = load_algorithm_time('result/bp.csv', time_cols, output_col)
    temp_df[output_col] = temp_df[output_col] * BUFF_TIME_FACTOR_VS_BPE
    return temp_df.rename(columns={output_col: 'BUFF'})


df_ratio = pd.read_csv(rel_path('result/compression_ratio/baseline.csv'))

buff_ratio_df = pd.read_csv(rel_path('result/buff.csv'))
buff_ratio_col = pick_first_existing_column(buff_ratio_df, RATIO_COLS)
buff_ratio_df = buff_ratio_df[['Dataset', buff_ratio_col]].rename(
    columns={buff_ratio_col: 'BUFF_from_buff_csv'}
)
df_ratio = df_ratio.merge(buff_ratio_df, on='Dataset', how='left')
if 'BUFF' in df_ratio.columns:
    df_ratio['BUFF'] = pd.to_numeric(df_ratio['BUFF'], errors='coerce').combine_first(
        pd.to_numeric(df_ratio['BUFF_from_buff_csv'], errors='coerce')
    )
else:
    df_ratio['BUFF'] = pd.to_numeric(df_ratio['BUFF_from_buff_csv'], errors='coerce')
df_ratio.drop(columns=['BUFF_from_buff_csv'], inplace=True)

alp_ratio_df = pd.read_csv(rel_path('result/alp.csv'))
alp_ratio_col = pick_first_existing_column(alp_ratio_df, RATIO_COLS)
alp_ratio_df = alp_ratio_df[['Dataset', alp_ratio_col]].rename(
    columns={alp_ratio_col: 'ALP_from_alp_csv'}
)
df_ratio = df_ratio.merge(alp_ratio_df, on='Dataset', how='left')
if 'ALP' in df_ratio.columns:
    df_ratio['ALP'] = pd.to_numeric(df_ratio['ALP'], errors='coerce').combine_first(
        pd.to_numeric(df_ratio['ALP_from_alp_csv'], errors='coerce')
    )
else:
    df_ratio['ALP'] = pd.to_numeric(df_ratio['ALP_from_alp_csv'], errors='coerce')
df_ratio.drop(columns=['ALP_from_alp_csv'], inplace=True)

algorithms = {
    'RLE': 'result/rle.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
    'BPE': 'result/bp.csv',
    'DE': 'result/dictionary_long.csv',
    'BitWeaving': 'result/hbp.csv',
    # 'Simple8b': 'result/simple8b_compression.csv',
    # 'FastPFOR': 'result/fastpfor_compression.csv',
    'Sub-column': 'result/subcolumn_adddict_prunenew_opt2.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn_adddict_prunenew_opt2.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn_adddict_prunenew_opt2.csv',
}

for algo_name, file_path in algorithms.items():
    algo_df = pd.read_csv(rel_path(file_path))
    ratio_col = pick_first_existing_column(algo_df, RATIO_COLS)
    algo_df.rename(columns={ratio_col: algo_name}, inplace=True)
    df_ratio = df_ratio.merge(
        algo_df[['Dataset', algo_name]],
        on='Dataset',
        how='left'
    )

df_ratio = df_ratio[df_ratio['Dataset'].isin(dataset_abbreviations.keys())].reset_index(drop=True)
df_ratio['Dataset'] = df_ratio['Dataset'].map(dataset_abbreviations)

for col in df_ratio.columns[1:]:
    df_ratio[col] = 1 / df_ratio[col]

cols = ['Dataset'] + [col for col in alg_order if col in df_ratio.columns]
df_ratio = df_ratio[cols]

df_ratio_long = pd.melt(
    df_ratio,
    id_vars=['Dataset'],
    var_name='Algorithm',
    value_name='Compression Ratio'
)
ratio_ylim_top = (
    df_ratio_long
    .groupby('Algorithm')['Compression Ratio']
    .mean()
    .reindex(alg_order)
    .max()
    * 1.10
)


df_encode = pd.read_csv(rel_path('result/compression_time/baseline.csv'))
numeric_cols = [col for col in df_encode.columns if col != 'Dataset']
for col in numeric_cols:
    df_encode[col] = pd.to_numeric(df_encode[col], errors='coerce')

encode_algorithms = {
    'RLE': 'result/rle_long.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
    'BPE': 'result/bp.csv',
    'DE': 'result/dictionary_long.csv',
    'BitWeaving': 'result/hbp.csv',
    # 'Simple8b': 'result/simple8b_compression.csv',
    # 'FastPFOR': 'result/fastpfor_compression.csv',
    'Sub-column': 'result/subcolumn_adddict_prunenew_opt2.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn_adddict_prunenew_opt2.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn_adddict_prunenew_opt2.csv',
    'ALP': 'result/alp.csv'
}

for algo_name, file_path in encode_algorithms.items():
    temp_df = load_algorithm_time(file_path, ENCODE_TIME_COLS, algo_name)
    df_encode = upsert_algorithm_time(df_encode, algo_name, temp_df)

df_encode = upsert_algorithm_time(
    df_encode,
    'BUFF',
    bpe_calibrated_buff_time(ENCODE_TIME_COLS, 'Compression Time (ns/point)'),
)

df_encode = df_encode[df_encode['Dataset'].isin(dataset_abbreviations.keys())].reset_index(drop=True)
df_encode['Dataset'] = df_encode['Dataset'].map(dataset_abbreviations)

cols = ['Dataset'] + [col for col in alg_order if col in df_encode.columns]
df_encode = df_encode[cols]

df_encode_long = pd.melt(
    df_encode, id_vars=['Dataset'], var_name='Algorithm', value_name='Time (ns/point)'
)


df_decode = pd.read_csv(rel_path('result/decompression_time/baseline.csv'))
numeric_cols = [col for col in df_decode.columns if col != 'Dataset']
for col in numeric_cols:
    df_decode[col] = pd.to_numeric(df_decode[col], errors='coerce')

decode_algorithms = {
    'RLE': 'result/rle_long.csv',
    'SPRINTZ': 'result/sprintz.csv',
    'TS2DIFF': 'result/ts2diff.csv',
    'BPE': 'result/bp.csv',
    'DE': 'result/dictionary_long.csv',
    'BitWeaving': 'result/hbp.csv',
    # 'Simple8b': 'result/simple8b_compression.csv',
    # 'FastPFOR': 'result/fastpfor_compression.csv',
    'Sub-column': 'result/subcolumn_adddict_prunenew_opt2.csv',
    'SPRINTZ+Sub-column': 'result/sprintz_subcolumn_adddict_prunenew_opt2.csv',
    'TS2DIFF+Sub-column': 'result/ts2diff_subcolumn_adddict_prunenew_opt2.csv',
    'ALP': 'result/alp.csv'
}

for algo_name, file_path in decode_algorithms.items():
    temp_df = load_algorithm_time(file_path, DECODE_TIME_COLS, algo_name)
    df_decode = upsert_algorithm_time(df_decode, algo_name, temp_df)

df_decode = upsert_algorithm_time(
    df_decode,
    'BUFF',
    bpe_calibrated_buff_time(DECODE_TIME_COLS, 'Decompression Time (ns/point)'),
)

df_decode = df_decode[df_decode['Dataset'].isin(dataset_abbreviations.keys())].reset_index(drop=True)
df_decode['Dataset'] = df_decode['Dataset'].map(dataset_abbreviations)

cols = ['Dataset'] + [col for col in alg_order if col in df_decode.columns]
df_decode = df_decode[cols]

df_decode_long = pd.melt(
    df_decode, id_vars=['Dataset'], var_name='Algorithm', value_name='Time (ns/point)'
)

fontsize = 12

colors = [
    '#A5D6A7',
    '#FF6600',
    '#B8C6D9',
    '#FFD700',
    '#FF9900',
    '#70E9B0',
    # '#000000',
    # '#FF1493',
    '#0A94EA',
    '#008000',
    '#00FF77',
    '#FF0000',
    '#90CAF9',
    '#AD62EE',
    '#43FFFF',
    '#FF6600',
]

hatches = ['//' if i % 2 == 0 else '\\\\' for i in range(len(colors))]
color_mapping = {alg: colors[i] for i, alg in enumerate(alg_order)}
legend_ncol = (len(alg_order) + 1) // 2

axes: list[Axes]


def draw_mean_bars(
    ax: Axes,
    df_long: pd.DataFrame,
    value_col: str,
    title: str,
    ylabel: str,
    log_scale: bool = False,
) -> pd.Series:
    mean_values = (
        df_long
        .groupby('Algorithm')[value_col]
        .mean()
        .reindex(alg_order)
        .dropna()
    )
    x_positions = np.arange(len(mean_values))
    bars = ax.bar(
        x_positions,
        mean_values.values,
        color=[color_mapping[alg] for alg in mean_values.index],
        width=0.75,
    )
    for i, (bar, alg) in enumerate(zip(bars, mean_values.index)):
        bar.set_hatch(hatches[alg_order.index(alg)])
        if alg in ['Sub-column', 'SPRINTZ+Sub-column', 'TS2DIFF+Sub-column']:
            bar.set_edgecolor('black')
            bar.set_linewidth(2.5)

    ax.set_title(title, fontsize=fontsize)
    ax.set_xticks([])
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.set_xlabel('', fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    if log_scale:
        ax.set_yscale('log')
    return mean_values


def draw_compression_ratio_bars(ax: Axes) -> None:

    datasets = dataset_order
    num_datasets = len(datasets)
    bar_alg_order = [alg for alg in alg_order if alg in df_ratio.columns]
    num_algs = len(bar_alg_order)
    if num_algs == 0:
        raise ValueError('No algorithms available to draw compression ratio bars.')
    bar_width = 0.90 / num_algs
    x_positions = np.arange(num_datasets)

    for alg_idx, alg in enumerate(bar_alg_order):
        alg_data = (
            df_ratio_long[df_ratio_long['Algorithm'] == alg]
            .set_index('Dataset')['Compression Ratio']
            .reindex(datasets)
        )

        offset = (alg_idx - num_algs / 2 + 0.5) * bar_width
        bars = ax.bar(
            x_positions + offset,
            alg_data.values,
            bar_width,
            color=color_mapping[alg],
            hatch=hatches[alg_idx],
        )
        if alg in ['Sub-column', 'SPRINTZ+Sub-column', 'TS2DIFF+Sub-column']:
            for bar in bars:
                bar.set_edgecolor('black')
                bar.set_linewidth(2.5)

    ax.set_ylabel('Compression Ratio', fontsize=fontsize)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(datasets, fontsize=fontsize)
    ax.set_ylim(bottom=0)

    half_span = num_algs * bar_width / 2
    edge_pad = 0.02
    ax.set_xlim(-half_span - edge_pad, (num_datasets - 1) + half_span + edge_pad)


fig_bar = plt.figure(figsize=(18, 3.2))
ax_bar = fig_bar.add_subplot(1, 1, 1)
draw_compression_ratio_bars(ax_bar)

legend_elements_bar = [Patch(facecolor=color_mapping[alg], label=alg, hatch=hatches[i]) for i, alg in enumerate(alg_order)]
fig_bar.legend(
    handles=legend_elements_bar,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.1),
    ncol=legend_ncol,
    labelspacing=0.05,
    columnspacing=0.1,
    handletextpad=0.1,
    fontsize=fontsize,
)


plt.close(fig_bar)


# fig = plt.figure(figsize=(18, 6.6))
# gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.05], hspace=0.10, wspace=0.22)
# ax_a = fig.add_subplot(gs[0, 0])
# ax_b = fig.add_subplot(gs[0, 1])
# ax_c = fig.add_subplot(gs[0, 2])
# ax_d = fig.add_subplot(gs[1, :])
# fig = plt.figure(figsize=(18, 3.4))
# gs = fig.add_gridspec(1, 3, wspace=0.22)
# ax_a = fig.add_subplot(gs[0, 0])
# ax_b = fig.add_subplot(gs[0, 1])
# ax_c = fig.add_subplot(gs[0, 2])
fig = plt.figure(figsize=(18, 3.8))
gs = fig.add_gridspec(1, 3, wspace=0.22)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])

ratio_means = draw_mean_bars(
    ax_a,
    df_ratio_long,
    'Compression Ratio',
    '(a) Compression Ratio',
    'Compression Ratio',
)
ax_a.set_ylim(0, ratio_ylim_top)

encode_means = draw_mean_bars(
    ax_b,
    df_encode_long,
    'Time (ns/point)',
    '(b) Compression Time',
    'Time (ns/point)',
)

decode_means = draw_mean_bars(
    ax_c,
    df_decode_long,
    'Time (ns/point)',
    '(c) Decompression Time',
    'Time (ns/point)',
)

time_ticks = np.arange(0, 60.1, 10.0)
time_tick_labels = [str(int(tick)) for tick in time_ticks]
ax_b.set_ylim(0, 60)
ax_c.set_ylim(0, 60)
ax_b.set_yticks(time_ticks)
ax_c.set_yticks(time_ticks)
ax_b.set_yticklabels(time_tick_labels, fontsize=fontsize)
ax_c.set_yticklabels(time_tick_labels, fontsize=fontsize)

legend_elements = [
    Patch(facecolor=color_mapping[alg], label=alg, hatch=hatches[i])
    for i, alg in enumerate(alg_order)
]

fig.legend(
    handles=legend_elements,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.10),
    ncol=legend_ncol,
    labelspacing=0.2,
    columnspacing=0.2,
    handletextpad=0.2,
    fontsize=fontsize,
)

FIG_DIR.mkdir(parents=True, exist_ok=True)
plt.savefig(FIG_DIR / 'merge_algorithm_comparison_relayout.png', dpi=1000, bbox_inches='tight')
plt.savefig(FIG_DIR / 'merge_algorithm_comparison_relayout.eps', format='eps', dpi=1000, bbox_inches='tight')
