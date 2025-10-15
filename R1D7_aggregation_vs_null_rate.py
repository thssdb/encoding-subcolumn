import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

null_rate_list = [0.0, 0.5]

fontsize = 18
labelsize = 18

query_types = [
    ('max', 'MAX(X)'),
    ('sum', 'SUM(X)'),
    ('count', 'COUNT(X)'),
]

medians_by_query = {qt[0]: [] for qt in query_types}

for query_type, title in query_types:
    beta_to_times = {beta: [] for beta in null_rate_list}

    for beta in null_rate_list:
        file_name = f'result/query_{query_type}_null/subcolumn_query_{query_type}_null_{beta}.csv'
        try:
            df = pd.read_csv(file_name)
        except Exception as e:
            print(f'Warning: cannot read {file_name}: {e}')
            continue

        for _, row in df.iterrows():
            points = row.get('Points', 0)
            decoding = row.get('Decoding Time', np.nan)
            denom = points
            if query_type == 'count':
                denom = points
            else:
                denom = points * (1 - beta) if points * \
                    (1 - beta) != 0 else points
            if denom == 0 or np.isnan(decoding):
                continue
            time_per_point = decoding / denom
            beta_to_times[beta].append(time_per_point)

    for beta in null_rate_list:
        times = beta_to_times.get(beta, [])
        if len(times) == 0:
            mean_val = np.nan
        else:
            mean_val = float(np.mean(times))
        medians_by_query[query_type].append(mean_val)

labels_x = [t[1] for t in query_types]
n_groups = len(labels_x)
n_bars = len(null_rate_list)

x = np.arange(n_groups)
bar_width = 0.35

fig, ax = plt.subplots(figsize=(5, 5.5))

colors = ['#FF0000', '#008000']
hatches = ['/', '\\']

for i, beta in enumerate(null_rate_list):
    heights = []
    for query_type, _ in query_types:
        val = medians_by_query[query_type][i] if query_type in medians_by_query else np.nan
        heights.append(val)
    print(heights)
    offset = (i - (n_bars - 1) / 2.0) * bar_width
    ax.bar(x + offset, heights, bar_width, label=('Aggregation without NULL' if beta == 0.0 else 'Aggregation with NULL'),
           color=colors[i], hatch=hatches[i], edgecolor='black', linewidth=1)

ax.set_xticks(x)
ax.set_xticklabels(labels_x, fontsize=labelsize-1, rotation=0)

ax.set_ylabel('Aggregation Time (ns/point)', fontsize=fontsize)
ax.tick_params(axis='y', labelsize=labelsize)
ax.set_yscale('log')
ax.set_ylim(0.001, 20)

all_vals = []
for q in medians_by_query:
    all_vals.extend([v for v in medians_by_query[q]
                    if not (v is None or np.isnan(v))])
if len(all_vals) > 0:
    ymin = 0
    ymax = max(all_vals) * 1.25
    ax.set_ylim(ymin, ymax)

ax.legend(fontsize=labelsize, loc='lower center',
          bbox_to_anchor=(0.4, 0.98),
          ncol=1,
          columnspacing=0.05,
          labelspacing=0.05,
          handletextpad=0.05)

plt.savefig('fig/R1D7_aggregation_combined_medians.png',
            dpi=300, bbox_inches='tight')
plt.savefig('fig/R1D7_aggregation_combined_medians.eps',
            format='eps', dpi=300, bbox_inches='tight')
