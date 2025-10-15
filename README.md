# Sub-columns for Data Encoding and Query Processing

In our paper **Sub-columns for Data Encoding and Query Processing**, we show some example and perfomance about Sub-columns.

To enable reproductivity, we share all datasets, algorithms and codes in the repository, and this readme guides will help you reproduce the results of the experiment and figures in the paper.

## 1. Directory Structure

    ├── README.md           // Help Document

    ├── result       // Results of the experiments

    ├── fig      // Figures of the experiments

    ├── other .py       // codes of drawing results

    ├── dataset   // datasets

## 2. Environment Requirement

- python: 3.8+
- modules needed: numpy, pandas, matplotlib

## 3. Code Execution

- Get results of compression ratio and time

```shell
java xxx.java
```

- The algorithm corresponding to the java code is as follows

| algorithms          | java code                                                                             |
| ------------------- | ------------------------------------------------------------------------------------- |
| Sub-columns         | iotdb\tsfile\src\test\java\org\apache\iotdb\tsfile\encoding\SubcolumnTest.java        |
| SPRINTZ+Sub-columns | iotdb\tsfile\src\test\java\org\apache\iotdb\tsfile\encoding\SPRINTZSubcolumnTest.java |
| TS2DIFF+Sub-columns | iotdb\tsfile\src\test\java\org\apache\iotdb\tsfile\encoding\TSDIFFSubcolumnTest.java  |

- Get figures about xxx.py

```shell
python xxx.py
```

- The figures corresponding to the python code are as follows

| Figures   | python code                           |
| --------- | ------------------------------------- |
| Figure 1  | decimal_8_distribution.py             |
| Figure 7  | R0_merge_compression_ratio_time_de.py |
| Figure 8  | R4O5_compression_vs_beta(a).py        |
| Figure 9  | R1D1_R1D4_R3O1_query.py               |
| Figure 10 | R1D3_materialization.py               |
| Figure 11 | R1D7_aggregation_vs_null_rate.py      |
| Figure 12 | R1D8_compare_parallel_filter.py       |
| Figure 13 | R1D6_compare_sort_key_and_value.py    |
| Figure 14 | R2O1_compare_update_new.py            |
| Figure 15 | R2O2_add_dictionary.py                |
| Figure 16 | R3O2_compare_pso.py                   |
| Figure 17 | R4O6_ablation_study.py                |
