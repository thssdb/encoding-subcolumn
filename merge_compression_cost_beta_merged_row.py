



import math
import os
from decimal import Decimal

import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D




dataset_abbreviations = {

    'Bird-migration': 'BM',
    'Bitcoin-price': 'BP',
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

# 绘图结果中排除 BP (Bitcoin-price)
PLOT_EXCLUDE_DATASET_KEYS = frozenset({'Bitcoin-price'})
PLOT_EXCLUDE_DATASETS = frozenset({'BP'})


def is_plot_excluded(dataset_label: str) -> bool:
    return (
        dataset_label in PLOT_EXCLUDE_DATASETS
        or dataset_label in PLOT_EXCLUDE_DATASET_KEYS
    )

t = np.linspace(0, 2 * np.pi, 100)
x = 16 * np.sin(t) ** 3
y = (
    13 * np.cos(t)
    - 5 * np.cos(2 * t)
    - 2 * np.cos(3 * t)
    - np.cos(4 * t)
)
x = x / np.max(np.abs(x))
y = y / np.max(np.abs(y))
heart_parametric = mpath.Path(np.column_stack([x, y]))

trapezoid_vertices = [
    (-0.8, -1),
    (0.8, -1),
    (0.4, 1),
    (-0.4, 1),
    (-0.8, -1),
]
trapezoid = mpath.Path(trapezoid_vertices)

parallelogram_vertices = [
    (-1, -0.6),
    (0.5, -0.6),
    (1, 0.6),
    (-0.5, 0.6),
    (-1, -0.6),
]
parallelogram = mpath.Path(parallelogram_vertices)

colors = [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00',
    '#ffc107',
    '#a65628',
    '#f781bf',
    '#999999',
    '#66c2a5',
    '#fc8d62',
    '#8da0cb',
    '#ff69b4',
    '#8b0000',
    '#00ced1',
]
markers = [
    heart_parametric,
    'o',
    's',
    '^',
    'v',
    '>',
    '<',
    'D',
    'p',
    '*',
    'X',
    'P',
    'd',
    trapezoid,
    parallelogram,
    '1',
    '2',
    '3',
    '4',
    '|',
    '_',
]

dataset_marker_color_map = {
    ds: (markers[i % len(markers)], colors[i % len(colors)])
    for i, ds in enumerate(dataset_abbreviations.values())
}

fontsize = 20
labelsize = 20
legend_fontsize = 20
markersize_compression = 12
marker_size_cost = 12
MAX_BETA = 30





def find_decimal_places(value_str):
    if '.' not in value_str and 'e' not in value_str.lower():
        return 0
    value_str = value_str.strip()
    if 'e' in value_str.lower():
        mantissa, exponent = value_str.lower().split('e')
        exp = int(exponent)
        if '.' in mantissa:
            decimal_part = mantissa.split('.')[1]
            return max(0, len(decimal_part) - exp)
        return max(0, -exp)
    if '.' in value_str:
        decimal_part = value_str.split('.')[1]
        return len(decimal_part)
    return 0


datasets_data = {}
dataset_names = list(dataset_abbreviations.keys())

for dataset_name in dataset_names:
    file_path = f'dataset/{dataset_name}.csv'
    if not os.path.exists(file_path):
        continue
    values = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(float(line))
    max_decimal_places = 0
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                max_decimal_places = max(
                    max_decimal_places, find_decimal_places(line)
                )
    scale_factor = 10 ** max_decimal_places
    integer_values = [int(round(v * scale_factor)) for v in values]
    datasets_data[dataset_name] = {
        'values': integer_values,
        'scale_factor': scale_factor,
        'max_decimal_places': max_decimal_places,
    }

block_size = 1024
bitwidth_stats = {}
for dataset_name in dataset_names:
    if dataset_name not in datasets_data:
        continue
    integer_values = datasets_data[dataset_name]['values']
    max_bitwidth = 0
    for block_start in range(0, len(integer_values), block_size):
        block_end = min(block_start + block_size, len(integer_values))
        block = integer_values[block_start:block_end]
        block_min = min(block)
        normalized_block = [v - block_min for v in block]
        block_max = max(normalized_block)
        if block_max > 0:
            bitwidth = block_max.bit_length()
        else:
            bitwidth = 1
        max_bitwidth = max(max_bitwidth, bitwidth)
    bitwidth_stats[dataset_name] = max_bitwidth

beta_list = list(range(1, 32))
file_names = [
    f'result/compression_vs_beta/subcolumn_beta_{beta}.csv' for beta in beta_list
]

compression_ratios = {}
compression_times = {}
decompression_times = {}

for file_name, beta in zip(file_names, beta_list):
    df = pd.read_csv(file_name)
    df['Dataset'] = df['Dataset'].map(dataset_abbreviations)

    df = df.dropna(subset=['Dataset']).copy()
    df['Dataset'] = pd.Categorical(
        df['Dataset'],
        categories=dataset_abbreviations.values(),
        ordered=True,
    )
    df = df.sort_values('Dataset')
    for _, row in df.iterrows():
        dataset = row['Dataset']
        compression_ratio = 1 / row['Compression Ratio']
        compression_time = row['Encoding Time'] / row['Points']
        decompression_time = row['Decoding Time'] / row['Points']
        if dataset not in compression_ratios:
            compression_ratios[dataset] = []
            compression_times[dataset] = []
            decompression_times[dataset] = []
        compression_ratios[dataset].append((beta, compression_ratio))
        compression_times[dataset].append((beta, compression_time))
        decompression_times[dataset].append((beta, decompression_time))

filtered_compression_ratios = {}
best_betas = {}

for dataset in compression_ratios:
    ratios = compression_ratios[dataset]
    compression_values = [ratio[1] for ratio in ratios]
    original_dataset_name = None
    for key, value in dataset_abbreviations.items():
        if value == dataset:
            original_dataset_name = key
            break
    if original_dataset_name and original_dataset_name in bitwidth_stats:
        b0 = bitwidth_stats[original_dataset_name]
    else:
        b0 = 31
    best_beta = ratios[compression_values.index(max(compression_values))][0]
    best_betas[dataset] = best_beta
    if not is_plot_excluded(dataset):
        print(f"{dataset}: best_beta={best_beta} (b0={b0})")
    filtered_compression_ratios[dataset] = [
        (beta, ratio) for beta, ratio in ratios if beta <= b0
    ]





def get_decimal_places(value):
    if isinstance(value, int):
        return 0
    d = Decimal(str(value))
    return abs(d.as_tuple().exponent)


def convert_to_integer_and_shift(values):
    alpha = 0
    for val in values:
        alpha = max(alpha, get_decimal_places(val))
    if alpha > 0:
        multiplier = 10 ** alpha
        int_values = np.array([int(val * multiplier) for val in values])
    else:
        int_values = np.array([int(val) for val in values])
    min_val = int_values.min()
    shifted_values = int_values - min_val
    return shifted_values, alpha, min_val


def extract_subcolumn(values, j, beta):
    subcolumn = []
    for val in values:
        extracted = (val >> (j * beta)) & ((1 << beta) - 1)
        subcolumn.append(extracted)
    return np.array(subcolumn)


def process_dataset(file_path, max_beta=30):
    try:
        df = pd.read_csv(file_path)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            return None
        col_name = numeric_cols[0]
        raw_values_bpe_list = []
        for start_index in range(len(df) - 8):
            raw_values_bpe = df[col_name].values[start_index : start_index + 8]
            raw_values_bpe_list.append(raw_values_bpe)
        all_bpe_costs = []
        betas = list(range(1, max_beta + 1))
        for raw_values_bpe in raw_values_bpe_list:
            X_bpe, _, _ = convert_to_integer_and_shift(raw_values_bpe)
            n_bpe = len(X_bpe)
            max_val_bpe = int(X_bpe.max())
            max_bits_bpe = max_val_bpe.bit_length()
            if max_bits_bpe == 0:
                continue
            betas = list(range(1, min(max_bits_bpe, max_beta) + 1))
            beta_costs_parts = []
            for beta in betas:
                total_bpe = 0
                num_subcolumns_bpe = math.ceil(max_bits_bpe / beta)
                for j in range(num_subcolumns_bpe):
                    subcolumn_bpe = extract_subcolumn(X_bpe, j, beta)
                    max_subcolumn_bpe = subcolumn_bpe.max()
                    if max_subcolumn_bpe == 0:
                        bpe_bits_per_value = 0
                    else:
                        bpe_bits_per_value = math.ceil(
                            math.log2(max_subcolumn_bpe + 1)
                        )
                    bpe_cost_j = bpe_bits_per_value * n_bpe
                    total_bpe += bpe_cost_j
                beta_costs_parts.append(total_bpe / n_bpe)
            all_bpe_costs.append(beta_costs_parts)
        variances = [np.var(costs) for costs in all_bpe_costs]
        max_var_index = np.argmax(variances)
        bpe_costs = all_bpe_costs[max_var_index]
        raw_values_rle_de = df[col_name].values[1024:2048]
        X_rle_de, _, _ = convert_to_integer_and_shift(raw_values_rle_de)
        n_rle_de = len(X_rle_de)
        rle_costs = []
        de_costs = []
        max_val_rle_de = int(X_rle_de.max())
        max_bits_rle_de = max_val_rle_de.bit_length()
        betas = list(range(1, len(bpe_costs) + 1))
        for beta in betas:
            num_subcolumns_rle_de = math.ceil(max_bits_rle_de / beta)
            total_rle = 0
            total_de = 0
            for j in range(num_subcolumns_rle_de):
                subcolumn_rle_de = extract_subcolumn(X_rle_de, j, beta)
                runs = 1
                for i in range(1, len(subcolumn_rle_de)):
                    if subcolumn_rle_de[i] != subcolumn_rle_de[i - 1]:
                        runs += 1
                rle_run_length_overhead = math.ceil(math.log2(n_rle_de + 1))
                rle_cost_j = runs * (beta + rle_run_length_overhead)
                unique_values = len(np.unique(subcolumn_rle_de))
                if unique_values == 0:
                    de_index_bits = 1
                else:
                    de_index_bits = math.ceil(math.log2(unique_values + 1))
                de_cost_j = (
                    de_index_bits * n_rle_de
                    + unique_values * (beta + unique_values)
                )
                total_rle += rle_cost_j
                total_de += de_cost_j
            rle_costs.append(total_rle / n_rle_de)
            de_costs.append(total_de / n_rle_de)
        return {
            'betas': betas,
            'bpe_costs': bpe_costs,
            'rle_costs': rle_costs,
            'de_costs': de_costs,
            'max_bits': max_bits_bpe,
        }
    except Exception:
        return None


dataset_dir = 'dataset/'
csv_files = [f for f in os.listdir(dataset_dir) if f.endswith('.csv')]
csv_files.sort()

all_results = {}
for csv_file in csv_files:
    file_path = os.path.join(dataset_dir, csv_file)
    dataset_name = os.path.splitext(csv_file)[0]
    abbrev_name = dataset_abbreviations.get(dataset_name, dataset_name)
    result = process_dataset(file_path, max_beta=MAX_BETA)
    if result is not None:
        all_results[abbrev_name] = result

max_y_value = 0
min_y_value = float('inf')
# for _, result in all_results.items():
for dataset_name, result in all_results.items():
    if is_plot_excluded(dataset_name):
        continue
    max_y_value = max(max_y_value, max(result['bpe_costs']))
    max_y_value = max(max_y_value, max(result['rle_costs']))
    max_y_value = max(max_y_value, max(result['de_costs']))
    min_y_value = min(min_y_value, min(result['bpe_costs']))
    min_y_value = min(min_y_value, min(result['rle_costs']))
    min_y_value = min(min_y_value, min(result['de_costs']))






fig, (ax_a, ax_b, ax_c, ax_d) = plt.subplots(1, 4, figsize=(32, 5))
plt.subplots_adjust(wspace=0.3, right=0.88)

abbrev_order = list(dataset_abbreviations.values())

plot_compression_ratios = {
    dataset: ratios
    for dataset, ratios in filtered_compression_ratios.items()
    if not is_plot_excluded(dataset)
}
plot_all_results = {
    dataset_name: result
    for dataset_name, result in all_results.items()
    if not is_plot_excluded(dataset_name)
}

# for dataset in filtered_compression_ratios.keys():
for dataset, ratios in plot_compression_ratios.items():
    beta = [x[0] for x in ratios]
    compression_values = [x[1] for x in ratios]
    di = abbrev_order.index(dataset)
    marker = markers[di]
    color = colors[di]
    ax_a.plot(beta, compression_values, marker='', color=color)
    max_index = compression_values.index(max(compression_values))
    ax_a.plot(
        beta[max_index],
        compression_values[max_index],
        marker=marker,
        color=color,
        markersize=markersize_compression,
    )

ax_a.tick_params(axis='both', which='major', labelsize=labelsize)
ax_a.set_xlabel(r'Column Width $\alpha$', fontsize=fontsize)
ax_a.set_ylabel('Compression Ratio', fontsize=fontsize)
ax_a.set_title('(a) Compression ratio', fontsize=fontsize)
ax_a.set_xticks(range(1, 32, 3))

legend_handles = []
legend_labels = []


# for dataset_name, result in all_results.items():
for dataset_name, result in plot_all_results.items():
    if dataset_name not in dataset_marker_color_map:
        continue
    betas = result['betas']
    costs = result['bpe_costs']
    min_cost_idx = costs.index(min(costs))
    marker, color = dataset_marker_color_map[dataset_name]
    ax_b.plot(betas, costs, color=color, linewidth=1.5)
    ax_b.plot(
        betas[min_cost_idx],
        costs[min_cost_idx],
        marker=marker,
        color=color,
        markersize=marker_size_cost,
        markerfacecolor=color,
        markeredgecolor=color,
    )
    legend_handles.append(
        Line2D(
            [0],
            [0],
            marker=marker,
            color=color,
            linestyle='-',
            linewidth=1.5,
            markersize=8,
            markerfacecolor=color,
            markeredgecolor=color,
        )
    )
    legend_labels.append(dataset_name)


# for dataset_name, result in all_results.items():
for dataset_name, result in plot_all_results.items():
    if dataset_name not in dataset_marker_color_map:
        continue
    betas = result['betas']
    costs = result['rle_costs']
    min_cost_idx = costs.index(min(costs))
    marker, color = dataset_marker_color_map[dataset_name]
    ax_c.plot(betas, costs, color=color, linewidth=1.5)
    ax_c.plot(
        betas[min_cost_idx],
        costs[min_cost_idx],
        marker=marker,
        color=color,
        markersize=marker_size_cost,
        markerfacecolor=color,
        markeredgecolor=color,
    )


# for dataset_name, result in all_results.items():
for dataset_name, result in plot_all_results.items():
    if dataset_name not in dataset_marker_color_map:
        continue
    betas = result['betas']
    costs = result['de_costs']
    min_cost_idx = costs.index(min(costs))
    marker, color = dataset_marker_color_map[dataset_name]
    ax_d.plot(betas, costs, color=color, linewidth=1.5)
    ax_d.plot(
        betas[min_cost_idx],
        costs[min_cost_idx],
        marker=marker,
        color=color,
        markersize=marker_size_cost,
        markerfacecolor=color,
        markeredgecolor=color,
    )

for ax_cost, title in (
    (ax_b, '(b) BPE'),
    (ax_c, '(c) RLE'),
    (ax_d, '(d) DE'),
):
    ax_cost.set_yscale('log')
    ax_cost.tick_params(axis='both', which='major', labelsize=labelsize)
    ax_cost.set_xlabel(r'Column Width $\alpha$', fontsize=fontsize)
    ax_cost.set_ylabel('Cost (bits/point)', fontsize=fontsize)
    ax_cost.set_title(title, fontsize=fontsize)
    ax_cost.set_xlim(1, MAX_BETA)
    ax_cost.set_ylim(min_y_value * 0.8, max_y_value * 1.2)
    ax_cost.set_xticks(range(1, MAX_BETA + 1, 3))

fig.legend(
    legend_handles,
    legend_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.08),
    ncol=14,
    columnspacing=0.2,
    labelspacing=0.2,
    handletextpad=0.2,
    fontsize=legend_fontsize,
    frameon=True,
)

output_dir = 'fig'
os.makedirs(output_dir, exist_ok=True)
out_base = f'{output_dir}/compression_cost_beta_merged_row'
plt.savefig(f'{out_base}.png', dpi=300, bbox_inches='tight')
plt.savefig(f'{out_base}.eps', format='eps', dpi=300, bbox_inches='tight')
plt.close()
print(f'Wrote {out_base}.png and {out_base}.eps')
print(
    f'Plotted datasets ({len(legend_labels)}): '
    f'{", ".join(legend_labels)}'
)
if any(is_plot_excluded(label) for label in legend_labels):
    raise RuntimeError('Excluded dataset appeared in plot legend')
print(f'Excluded from plot: {", ".join(sorted(PLOT_EXCLUDE_DATASETS))}')
