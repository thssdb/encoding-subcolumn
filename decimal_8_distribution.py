from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import os

files = [f.replace('.csv', '') for f in os.listdir('dataset') if f.endswith('.csv')]

positions = [4, 5, 6, 7]

title = [
    '(a) 5th sub-column', '(b) 6th sub-column',
    '(c) 7th sub-column', '(d) 8th sub-column',
]

position_data = {}

for file in files:
    numbers_str = []

    decimal_places = []

    with open(f'dataset/{file}.csv', 'r') as f:
        for line in f:
            num_str = line.strip()
            if num_str != '""':
                numbers_str.append(num_str)
                
                if '.' in num_str:
                    decimal_part = num_str.split('.')[1]
                    decimal_places.append(len(decimal_part))
                else:
                    decimal_places.append(0)

    n = max(decimal_places)

    digit_counters = [Counter({str(i): 0 for i in range(8)}) for _ in range(8)]

    for num_str in numbers_str:
        num = float(num_str)
        num *= 10 ** n

        octal_str = oct(int(num))

        o_index = octal_str.find('o')
        octal_str = octal_str[o_index + 1:].zfill(8)

        # 反转octal_str
        octal_str = octal_str[::-1]

        for i in range(8):
            digit = octal_str[i]
            digit_counters[i][digit] += 1

    position_data[file] = {
        'counters': [digit_counters[i] for i in positions],
        'total_count': len(numbers_str)
    }

# print(position_data)

title_text = [
    'sub-columns: (8th,  7th,  6th,  5th,  4th,  3rd, 2nd,  1st)',
    '10791147  =  (101, 001, 001, 010, 100, 011, 101, 011)',
    '10792951  =  (101, 001, 001, 010, 111, 111, 110, 111)',
    '10786947  =  (101, 001, 001, 001, 100, 010, 000, 011)',
    '10819218  =  (101, 001, 010, 001, 011, 010, 010, 010)',
]

# 101001001010100011101011
# 101001001010111111110111
# 101001001001100010000011
# 101001010001011010010010

fontsize = 24
xlabelsize = 16

axes: np.ndarray
fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 10)
)

for i, line in enumerate(title_text):
    fig.text(
        0.85,
        0.96 - i * 0.03,
        line,
        fontsize=fontsize,
        horizontalalignment='right',
        verticalalignment='top'
    )

plt.subplots_adjust(
    top=0.76,
    hspace=0.35,
    wspace=0.3
)

axes_flat = axes.flatten()

all_digits = set('01234567')

for subplot_idx, ax in enumerate(axes_flat):
    ax: Axes

    digit_percentages = {}

    for digit in sorted(all_digits):
        digit_percentages[digit] = []

    for file, data in position_data.items():
        counter: Counter = data['counters'][subplot_idx]
        total_count = data['total_count']

        for digit in sorted(all_digits):
            count = counter.get(digit, 0)
            percentage = (count / total_count) * 100
            digit_percentages[digit].append(percentage)

    box_data = [digit_percentages[digit] for digit in sorted(all_digits)]

    bp = ax.boxplot(
        box_data,
        tick_labels=[format(int(digit), '03b') for digit in sorted(all_digits)]
    )

    medians = [np.median(data) for data in box_data]
    ax.plot(
        list(range(1, 9)),
        medians,
        color='orange',
        linestyle='-',
        marker='o',
        linewidth=2,
        markersize=6
    )

    ax.set_title(title[subplot_idx], fontsize=fontsize)
    ax.set_xlabel('Bits', fontsize=fontsize)
    ax.set_ylabel('Percentage (%)', fontsize=fontsize)
    ax.tick_params(
        axis='x',
        which='major',
        labelsize=xlabelsize
    )
    ax.tick_params(
        axis='y',
        which='major',
        labelsize=fontsize
    )

# handles, labels = axes[0].get_legend_handles_labels()

# fig.legend(handles, labels, loc='upper center', fontsize=fontsize,
#            ncol=6, bbox_to_anchor=(0.5, 1.15))

plt.savefig(
    'fig/digit_distribution_8.png',
    dpi=1000,
    bbox_inches='tight'
)

plt.savefig(
    'fig/digit_distribution_8.eps',
    format='eps',
    dpi=1000,
    bbox_inches='tight'
)
# plt.show()
