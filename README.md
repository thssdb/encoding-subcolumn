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
| TS2DIFF+Sub-columns | iotdb\tsfile\src\test\java\org\apache\iotdb\tsfile\encoding\TSDIFFSubcolumnTest.java |

- Get figures about xxx.py

```shell
python xxx.py
```

- The figures corresponding to the python code are as follows

| Figures   | python code                     |
| --------- | ------------------------------- |
| Figure 1  | decimal_8_distribution.py       |
| Figure 7  | compression_ratio.py            |
| Figure 8  | compression_time.py             |
| Figure 9  | decompression_time.py           |
| Figure 10 | compression_vs_beta.py          |
| Figure 11 | compression_vs_block_boxplot.py |
| Figure 12 | query_vs_beta_boxplot.py        |
| Figure 13 | query_vs_block_boxplot.py       |
