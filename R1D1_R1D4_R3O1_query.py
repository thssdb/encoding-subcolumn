import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

query_types = {
    'greater': 'X > v',
    'less': 'X < v',
    'equal': 'X = v',
    'greater_less': 'X > a and X < b',
    'max': 'MAX(X)',
    'sum': 'SUM(X)',
    'count': 'COUNT(X)',
    'less_parts': 'X < a and Y < b'
}

bitweaving_results = {}
subcolumn_results = {}
parquet_select_results = {}
buff_results = {}
saphana_results = {}
parquet_dict_results = {}
parquet_delta_results = {}

for query_type in query_types.keys():
    try:
        df = pd.read_csv(f'result/vbp_query/vbp_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        bitweaving_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file vbp_query_{query_type}.csv not found, using placeholder data")
        bitweaving_results[query_type] = np.nan

df = pd.read_csv(
    f'result/vbp_query/vbp_query_{list(query_types.keys())[0]}.csv')
compression_ratio_vbp = 1 / df['Compression Ratio']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(
            f'result/subcolumn_query/subcolumn_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        subcolumn_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file subcolumn_query_{query_type}.csv not found, using placeholder data")
        subcolumn_results[query_type] = np.nan

df = pd.read_csv(
    f'result/subcolumn_query/subcolumn_query_{list(query_types.keys())[0]}.csv')
compression_ratio_subcolumn = 1 / df['Compression Ratio']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(
            f'result/query_parquetproto/parquetselect_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        parquet_select_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file parquetselect_query_{query_type}.csv not found, using placeholder data")
        parquet_select_results[query_type] = np.nan

df = pd.read_csv(
    f'result/query_parquetproto/parquetselect_query_{list(query_types.keys())[0]}.csv')
compression_ratio_parquet = 1 / df['Compression Ratio']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(f'result/buff_query/buff_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        buff_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file buff_query_{query_type}.csv not found, using placeholder data")
        buff_results[query_type] = np.nan

df = pd.read_csv(
    f'result/buff_query/buff_query_{list(query_types.keys())[0]}.csv')
compression_ratio_buff = 1 / df['Compression Ratio']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(
            f'result/saphana_query/saphana_query_{query_type}.csv')
        decoding_time_per_point = df['Query Time'] / df['Points']
        saphana_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file saphana_query_{query_type}.csv not found, using placeholder data")
        saphana_results[query_type] = np.nan

df = pd.read_csv('result/saphana.csv')
compression_ratio_saphana = df['Points'] * 8 / df['Compressed Size']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(
            f'result/parquet_dict_query/parquet_dict_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        parquet_dict_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file parquet_dict_query_{query_type}.csv not found, using placeholder data")
        parquet_dict_results[query_type] = np.nan

df_parquet_dict = pd.read_csv('result/parquet_dict.csv')
compression_ratio_parquet_dict = 1 / df_parquet_dict['Compression Ratio']

for query_type in query_types.keys():
    try:
        df = pd.read_csv(
            f'result/parquet_delta_query/parquet_delta_query_{query_type}.csv')
        decoding_time_per_point = df['Decoding Time'] / df['Points']
        parquet_delta_results[query_type] = decoding_time_per_point
    except FileNotFoundError:
        print(
            f"warning: file parquet_delta_query_{query_type}.csv not found, using placeholder data")
        parquet_delta_results[query_type] = np.nan

df_parquet_delta = pd.read_csv('result/parquet_delta.csv')
compression_ratio_parquet_delta = 1 / df_parquet_delta['Compression Ratio']

data = {
    'Sub-column': compression_ratio_subcolumn,
    'BitWeaving': compression_ratio_vbp,
    'BUFF': compression_ratio_buff,
    'Parquet (BPE)': compression_ratio_parquet,
    'Parquet (Dictionary)': compression_ratio_parquet_dict,
    'Parquet (Delta)': compression_ratio_parquet_delta,
    'SAP HANA': compression_ratio_saphana,
}
df_compression_ratio = pd.DataFrame(data)

fontsize = 15
labelsize = 15

query_labels = list(query_types.values())

ax1: Axes
ax2: Axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(
    8, 3.5), gridspec_kw={'width_ratios': [1, 1]})
box_width = 0.6


def calculate_stats(data_df, columns):
    means = [data_df[col].mean() for col in columns]
    stds = [data_df[col].std() for col in columns]
    return means, stds


labels = list(df_compression_ratio.columns)
x = np.arange(len(labels))

rotation = -45
ha = 'left'
x_offset = -0.3

colors = ['#FF0000', '#4ECDC4', '#008000',
          "#0A94EA", "#43FFFF", "#FFD700", "#8A2BE2"]

hatches = ['/' if i % 2 == 0 else '\\' for i in range(len(labels))]

means1, stds1 = calculate_stats(df_compression_ratio, data.keys())
bars4 = ax1.bar(x, means1, color=colors, hatch=hatches,
                edgecolor='black', linewidth=1, label=labels)
ax1.set_title('(a) Compression Ratio', fontsize=fontsize)
ax1.set_ylabel('Compression Ratio', fontsize=fontsize)
ax1.set_xticks([])

ax1.tick_params(axis='both', which='major', labelsize=labelsize)

algorithms = {
    'Sub-column': subcolumn_results,
    'BitWeaving': bitweaving_results,
    'BUFF': buff_results,
    'Parquet (BPE)': parquet_select_results,
    'Parquet (Dictionary)': parquet_dict_results,
    'Parquet (Delta)': parquet_delta_results,
    'SAP HANA': saphana_results,
}

means_list = []
labels_algo = []
for name, alg_dict in algorithms.items():
    df_alg = pd.DataFrame(alg_dict)
    mean_per_dataset = df_alg.mean(axis=1)
    means_list.append(mean_per_dataset.values)
    labels_algo.append(name)

means_avg = [np.mean(arr) for arr in means_list]

bars = ax2.bar(range(len(means_avg)), means_avg, color=colors,
               hatch=hatches, edgecolor='black', linewidth=1, label=labels)

ax2.set_ylabel('Query Time (ns/points)', fontsize=fontsize)
ax2.set_title('(b) Query Time', fontsize=fontsize)
ax2.tick_params(axis='both', which='major', labelsize=labelsize)
ax2.set_xticks([])

handles, labels = ax1.get_legend_handles_labels()

fig.legend(
    handles,
    labels,
    loc='upper center',
    bbox_to_anchor=(0.48, 1.15),
    ncol=4,
    fontsize=labelsize-2,
    columnspacing=0.1,
    labelspacing=0.1,
    handletextpad=0.1,
    handlelength=1.4,
)

plt.subplots_adjust(wspace=0.5, bottom=0.2)

plt.savefig('fig/R1D1_R1D4_R3O1_query.png', dpi=1000, bbox_inches='tight')
plt.savefig('fig/R1D1_R1D4_R3O1_query.eps',
            format='eps', dpi=1000, bbox_inches='tight')
