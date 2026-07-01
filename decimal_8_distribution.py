import os

from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

folder_path = 'dataset'


target_file_name = 'Gov10.csv'
block_size = 32
target_block_index = 364

positions = [4, 7]
title = [
    '(a) 5th sub-column', '(b) 8th sub-column',
    '(c) Repeats in 5th sub-column', '(d) Repeats in 8th sub-column',
]
position_data = {}

file_path = os.path.join(folder_path, target_file_name)
if not os.path.exists(file_path):
    raise FileNotFoundError(f'Dataset file not found: {file_path}')

numbers_str = []
decimal_places = []
with open(file_path, 'r') as f:
    for line in f:
        num_str = line.strip()
        if num_str != '""':
            numbers_str.append(num_str)
            if '.' in num_str:
                decimal_part = num_str.split('.')[1]
                decimal_places.append(len(decimal_part))
            else:
                decimal_places.append(0)

n = max(decimal_places) if decimal_places else 0
block_start = target_block_index * block_size
if block_start >= len(numbers_str):
    raise ValueError(
        f'target_block_index out of range: {target_block_index}, '
        f'total_blocks={(len(numbers_str) + block_size - 1) // block_size}'
    )
block_end = min(block_start + block_size, len(numbers_str))
numbers_str = numbers_str[block_start:block_end]

digit_counters = [Counter({str(i): 0 for i in range(8)}) for _ in range(8)]

consecutive_counts = [{} for _ in range(8)]
for i in range(8):
    for j in range(8):
        consecutive_counts[i][j] = Counter()

last_values = [None] * 8
current_streaks = [0] * 8

for num_str in numbers_str:
    num = float(num_str)
    num *= 10 ** n
    octal_str = oct(int(num))
    o_index = octal_str.find('o')
    octal_str = octal_str[o_index + 1:].zfill(8)[::-1]

    for i in range(8):
        digit = octal_str[i]
        digit_counters[i][digit] += 1

        if digit == last_values[i]:
            current_streaks[i] += 1
        else:
            if last_values[i] is not None and current_streaks[i] > 0:
                consecutive_counts[i][int(last_values[i])][current_streaks[i]] += 1

            current_streaks[i] = 1
            last_values[i] = digit

for i in range(8):
    if last_values[i] is not None and current_streaks[i] > 0:
        consecutive_counts[i][int(last_values[i])][current_streaks[i]] += 1

position_data[target_file_name] = {
    'counters': [digit_counters[i] for i in positions],
    'total_count': len(numbers_str),
    'consecutive_counts': [consecutive_counts[i] for i in positions]
}

print(target_file_name)
print(position_data[target_file_name])
print()

fontsize = 20
xlabelsize = 16
axes: np.ndarray
fig, axes = plt.subplots(2, 2, figsize=(12, 11))

title_text = [
    'sub-columns: (8th,  7th,  6th,  5th,  4th,  3rd, 2nd,  1st)',
    '       ...       =  ( ...,    ...,     ...,    ...,    ...,    ...,    ...,    ... )',
    ' 3479186  =  (001, 101, 010, 001, 011, 010, 010, 010)',
    ' 3446915  =  (001, 101, 001, 001, 100, 010, 000, 011)',
    ' 3446915  =  (001, 101, 001, 001, 100, 010, 000, 011)',
    ' 3479186  =  (001, 101, 010, 001, 011, 010, 010, 010)',
    '         146  =  (000, 000, 000, 000, 000, 010, 010, 010)',
    ' 3479191  =  (001, 101, 010, 001, 011, 010, 010, 111)',
    ' 3446919  =  (001, 101, 001, 001, 100, 010, 000, 111)',
    ' 3446919  =  (001, 101, 001, 001, 100, 010, 000, 111)',
    ' 3479190  =  (001, 101, 010, 001, 011, 010, 010, 110)',
    '       ...       =  ( ...,    ...,     ...,    ...,    ...,    ...,    ...,    ... )',
]

for i, line in enumerate(title_text):
    fig.text(0.45, 1.00 - i * 0.04, line, fontsize=fontsize, horizontalalignment='center', verticalalignment='top')

plt.subplots_adjust(top=0.50, hspace=0.55, wspace=0.3)

axes_flat = axes.flatten()
all_digits = sorted(set('01234567'))
tick_labels = [format(int(digit), '03b') for digit in all_digits]

for subplot_idx, ax in enumerate(axes_flat[:2]):
    data = position_data[target_file_name]
    counter: Counter = data['counters'][subplot_idx]
    total_count = data['total_count']
    percentages = [
        (counter.get(digit, 0) / total_count) * 100 if total_count > 0 else 0
        for digit in all_digits
    ]

    ax.bar(tick_labels, percentages, color='steelblue', edgecolor='black')
    ax.set_title(title[subplot_idx], fontsize=fontsize)
    ax.set_xlabel('Bits', fontsize=fontsize)
    ax.set_ylabel('Percentage (%)', fontsize=fontsize)
    ax.tick_params(axis='x', which='major', labelsize=xlabelsize)
    ax.tick_params(axis='y', which='major', labelsize=fontsize)


for subplot_idx, ax in enumerate(axes_flat[2:]):
    data = position_data[target_file_name]
    total_count = data['total_count']
    consecutive_count = data['consecutive_counts'][subplot_idx]

    threshold = 2
    percentages = []
    for digit in all_digits:
        count_above = sum(
            streak * count
            for streak, count in consecutive_count[int(digit)].items()
            if streak > threshold
        )
        percentage = (count_above / total_count) * 100 if total_count > 0 else 0
        percentages.append(percentage)

    ax.bar(tick_labels, percentages, color='darkorange', edgecolor='black')
    ax.set_title(title[subplot_idx + 2], fontsize=fontsize)
    ax.set_xlabel('Bits', fontsize=fontsize)
    ax.set_ylabel('Percentage (%)', fontsize=fontsize)
    ax.tick_params(axis='x', which='major', labelsize=xlabelsize)
    ax.tick_params(axis='y', which='major', labelsize=fontsize)


plt.savefig('fig/decimal_8_distribution.png', dpi=1000, bbox_inches='tight')
plt.savefig('fig/decimal_8_distribution.eps',
            format='eps', dpi=1000, bbox_inches='tight')
