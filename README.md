# On Optimizing Sub-column Compression

Artifacts and Python tooling for the **sub-column compression** experiments reported in the paper *On Optimizing Sub-column Compression*. This repository makes **figure reproduction** and **inspection of tabulated metrics** straightforward.

**Fastest path:** **§3 → Quick path**, then **§4 → Quick lookup of script** (copy-paste **Commands** there; use the detailed table for tests and notes).

---

## 1. Core method (implementation location)

- **In this repository (`subcolumn/`):** analysis and plotting scripts, benchmark datasets under `dataset/`, and result CSVs under `result/`.
- **Java JUnit benchmarks:** `iotdb/iotdb-core/tsfile/src/test/java/org/apache/iotdb/tsfile/encoding/` (run with Maven from `iotdb/`; see **§3.2**).
- **Elf / Gorilla / Chimp baselines:** [Spatio-Temporal-Lab/elf](https://github.com/Spatio-Temporal-Lab/elf) (cloned as `elf/`; see **§3.3** and Figure 11 notes).

**PruneNew / block-size / ablation (this checkout):** the paper’s main sub-column codec lives in `SubcolumnPruneNewTest.java`; block-size and ablation benchmarks use dedicated test classes on top of it. See **§5** for file layout, `Mode` semantics, CSV paths, and Maven commands.

---

## 2. Repository snapshot

### This repository

### IoTDB research fork

Repository link: [https://anonymous.4open.science/r/iotdb-research-encoding-subcolumns](https://anonymous.4open.science/r/iotdb-research-encoding-subcolumns)

Included location: `subcolumn/iotdb/` (sibling of this README).

### TsFile research fork

Repository link: [https://anonymous.4open.science/r/tsfile-research-encoding-subcolumns](https://anonymous.4open.science/r/tsfile-research-encoding-subcolumns)

Included location: `subcolumn/tsfile/` (sibling of this README; retained as project source, not used by the current Figure 1/11/12/13/14 scripts).

### Elf (Gorilla / Chimp / Elf XOR baselines)

Repository link: [https://github.com/Spatio-Temporal-Lab/elf](https://github.com/Spatio-Temporal-Lab/elf)

Clone location: `subcolumn/elf/`

---

## 3. Commands to run

### Quick path (reproduce one figure)

Do steps **in this order**; the only figure-specific part is **§4**.

1. **One-time setup** — **§3.1** (`.\scripts\bootstrap_env.ps1` on Windows, or `./scripts/bootstrap_env.sh` on Linux/macOS; or manual steps: Python 3.11+ venv and `requirements.txt`; `iotdb/` and `tsfile/` are included in this checkout).
2. **Find your figure** — open **§4 → Quick lookup of script**; copy **Commands**; read the detailed table for extra CSV prerequisites.
3. **Generate inputs** — run the listed `mvn test …` or Elf steps from **§4**.
4. **Plot (Python)** — activate `.venv`, `cd` to `{basedir}` (this repo root), run the `python …` lines. Outputs usually go to `fig/`.

`{basedir}` is the root of this **subcolumn** checkout (the directory containing this README).

### 3.1 Environment

Use **Python 3.11 or newer**, **JDK 17 or newer**, and **Maven 3.6+**.

**Declared versions**


| Role            | File               | Purpose                                           |
| --------------- | ------------------ | ------------------------------------------------- |
| Python packages | `requirements.txt` | `pip install -r requirements.txt` inside the venv |


**Research repository layout**

```bash
cd {basedir}
ls iotdb tsfile
# Optional, only if the Elf baselines are missing:
git clone -b dev --single-branch https://github.com/Spatio-Temporal-Lab/elf.git elf
```

**One-command setup**

Windows (PowerShell):

```powershell
cd {basedir}
.\scripts\bootstrap_env.ps1
```

Linux / macOS:

```bash
cd {basedir}
chmod +x scripts/*.sh   # first time only
./scripts/bootstrap_env.sh
```

This creates `.venv`, installs `requirements.txt`, and clones `elf/` if missing. It does **not** install JDK or Maven.

**Manual setup (equivalent)**

Windows (PowerShell):

```powershell
cd {basedir}
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```bash
cd {basedir}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the **Table 2** benchmark CSVs under `dataset/` (one column per file, e.g. `Gov10.csv`, `PM10-dust.csv`, …).

### 3.2 Java benchmarks (Maven / Surefire)

All JUnit benchmarks live in the **IoTDB tsfile** module. Always run from `{basedir}/iotdb` with `**-pl iotdb-core/tsfile`** (the parent POM has no tests; omitting `-pl` fails with “No tests matching pattern …”).

```powershell
cd iotdb
mvn test -pl iotdb-core/tsfile "-Dtest=<Class>#<method>" "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"
```

**Helper script (same command, from `{basedir}`):**

Windows (PowerShell):

```powershell
.\scripts\run_iotdb_test.ps1 -Test "BPTest#test0"
```

Linux / macOS:

```bash
./scripts/run_iotdb_test.sh "BPTest#test0"
```

**Surefire selectors**

- One class, one method: `BPTest#test0`
- One class, several methods: `SubcolumnQuerySortTest#testOptimizedSort+testDecodeSort`
- Several classes: `BPTest#test0,BUFFTest#test0`

`mvn test` runs **compile → test-compile → test** automatically; after you edit Java sources, re-run the same command to rebuild and execute.

**Output layout:** most benchmarks write CSVs under `{basedir}/result/` (or subfolders such as `result/compression_vs_beta/`). Before running, set each test’s `parent_dir` / `parentDir` in `iotdb/iotdb-core/tsfile/src/test/java/org/apache/iotdb/tsfile/encoding/` to your `{basedir}` with a trailing slash (forward slashes), e.g. `D:/path/to/subcolumn/`.

### 3.3 Elf baselines (Figure 11 prerequisites)

Figure 11 reads **Gorilla / Chimp / Elf** ratio and timing columns from:

- `result/compression_ratio/baseline.csv`
- `result/compression_time/baseline.csv`
- `result/decompression_time/baseline.csv`

Prepare these with the [Elf](https://github.com/Spatio-Temporal-Lab/elf) project (`dev` branch; cloned as `{basedir}/elf/`):

1. Copy the benchmark CSVs from `{basedir}/dataset/` into `elf/src/test/resources/ElfTestData/`.
2. Run `elf/src/test/java/org/urbcomp/startdb/compress/elf/doubleprecision/TestCompressor.java` (via your IDE or Maven in the `elf/` project).
3. Read the output at `elf/src/test/resources/result/result.csv`.
4. Merge the Gorilla, Chimp, and Elf columns from that file into the three baseline CSVs under `{basedir}/result/` (same `Dataset` rows as `dataset/*.csv`).

If your checkout already contains the three baseline files under `result/`, you can skip regeneration.

### 3.4 Figures (plotting)

From `{basedir}` with the venv activated:

Windows (PowerShell):

```powershell
cd {basedir}
.\.venv\Scripts\Activate.ps1
python <script-from-section-4>.py
```

Linux / macOS:

```bash
cd {basedir}
source .venv/bin/activate
python <script-from-section-4>.py
```

Outputs are usually under `fig/` as PNG/EPS.

---

## 4. Figure <-> script and test mapping

On **Linux / macOS**, use `./scripts/run_iotdb_test.sh "<Test>"` wherever the **Commands** column shows `.\scripts\run_iotdb_test.ps1 -Test "..."`, and activate the venv with `source .venv/bin/activate` instead of `.\.venv\Scripts\Activate.ps1`.

### Quick lookup of script


| Quick lookup of script                        | Figure | Script(s)                                                                 | Commands (run in order)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------- | ------ | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `decimal_8_distribution.py`                   | 1      | `decimal_8_distribution.py`                                               | 1. `cd {basedir}` && `.\.venv\Scripts\Activate.ps1` && `python decimal_8_distribution.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `merge_compression_ratio_time_de_relayout.py` | 11     | `merge_compression_ratio_time_de_relayout.py`                             | 1. Prepare Elf baselines (**§3.3**) → `result/compression_ratio/baseline.csv`, `result/compression_time/baseline.csv`, `result/decompression_time/baseline.csv` 2. `.\scripts\run_iotdb_test.ps1 -Test "ALPTest#test0,BPTest#test0,BUFFTest#test0,DictionaryLongTest#test0,HBPIndexLongTest#test0,SPRINTZBPTest#test0,RLEBPTest#test0,SubcolumnPruneNewTest#test0,SPRINTZSubcolumnPruneNewTest#test0,TSDIFFTest#test0,TSDIFFSubcolumnPruneNewTest#test0"` 3. `.\scripts\run_iotdb_test.ps1 -Test "Simple8bCompressionBenchmarkTest#testCsvDatasetsIfPresent,FastPFORCompressionBenchmarkTest#testCsvDatasetsIfPresent"` 4. Extra timing CSVs (**Note** below): `SubcolumnTest#test0`, `RLEBPLongTest#test0`, `SPRINTZSubcolumnTest#test0`, `TSDIFFSubcolumnTest#test0` 5. `python merge_compression_ratio_time_de_relayout.py` |
| `merge_compression_cost_beta_merged_row.py`   | 12     | `merge_compression_cost_beta_merged_row.py`                               | 1. `.\scripts\run_iotdb_test.ps1 -Test "SubcolumnLongBetaTest#test0"` 2. `python merge_compression_cost_beta_merged_row.py` (panels (b)–(d) read `dataset/*.csv` directly)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `ablation_study.py`                           | 13     | `ablation_study.py`                                                       | 1. `.\scripts\run_iotdb_test.ps1 -Test "SubcolumnFullTest#test0,SubcolumnWithoutBPETest#test0,SubcolumnWithoutDETest#test0,SubcolumnWithoutRLETest#test0"` 2. Ensure `result/subcolumn_*2.csv` exist for ratio panels (**§5.3**) 3. `python ablation_study.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `compression_vs_block_prune_mean_line.py`     | 14     | `compression_vs_block_prune_mean_line.py`                                 | 1. `.\scripts\run_iotdb_test.ps1 -Test "SubcolumnPruneNewBlockSizeNoPruneTest#testBlockSizeBenchmark"` (slow; run first or alone) 2. `.\scripts\run_iotdb_test.ps1 -Test "SubcolumnPruneNewBlockSizeTest#testBlockSizeBenchmark"` 3. `python compression_vs_block_prune_mean_line.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |


**Equivalent raw Maven** (from `{basedir}/iotdb`, any row above):

```powershell
mvn test -pl iotdb-core/tsfile "-Dtest=BPTest#test0" "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"
```

### Detailed mapping (tests and notes)


| Manuscript item                                                                  | Script                                        | Test function(s) of results                                                                                                                                                                                                                                 | Note                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Figure 1: Decimal-digit distribution in sub-columns (Gov10 example block)        | `decimal_8_distribution.py`                   | — (Python-only)                                                                                                                                                                                                                                             | Reads `dataset/Gov10.csv`; writes `fig/decimal_8_distribution.png` / `.eps`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Figure 11: Compression ratio, encode/decode time, and per-dataset ratio relayout | `merge_compression_ratio_time_de_relayout.py` | See **Quick lookup** row **11**; tests under `iotdb/.../encoding/`                                                                                                                                                                                          | **Baseline (Elf, §3.3):** `result/compression_ratio/baseline.csv`, `result/compression_time/baseline.csv`, `result/decompression_time/baseline.csv`. **Ratio CSVs:** `ALPTest#test0` → `result/alp.csv`; `BPTest#test0` → `result/bp.csv`; `BUFFTest#test0` → `result/buff.csv`; `DictionaryLongTest#test0` → `result/dictionary_long.csv`; `HBPIndexLongTest#test0` → `result/hbp.csv`; `SPRINTZBPTest#test0` → `result/sprintz.csv`; `RLEBPTest#test0` → `result/rle.csv`; `Simple8bCompressionBenchmarkTest#testCsvDatasetsIfPresent` → `result/simple8b_compression.csv`; `FastPFORCompressionBenchmarkTest#testCsvDatasetsIfPresent` → `result/fastpfor_compression.csv`; **`SubcolumnPruneNewTest#test0`** → `result/subcolumn_adddict_prunenew_opt2.csv` (**§5.1**); `SPRINTZSubcolumnPruneNewTest#test0` → `result/sprintz_subcolumn_adddict_prunenew_opt2.csv`; `TSDIFFTest#test0` → `result/ts2diff.csv`; `TSDIFFSubcolumnPruneNewTest#test0` → `result/ts2diff_subcolumn_adddict_prunenew_opt2.csv`. **Extra timing CSVs:** `SubcolumnTest#test0` → `result/subcolumn.csv`; `RLEBPLongTest#test0` → `result/rle_long.csv`; `SPRINTZSubcolumnTest#test0` → `result/sprintz_subcolumn.csv`; `TSDIFFSubcolumnTest#test0` → `result/ts2diff_subcolumn.csv`. Output: `fig/merge_algorithm_comparison_relayout.png` / `.eps`. |
| Figure 12: Compression ratio vs column width α and BPE/RLE/DE cost curves        | `merge_compression_cost_beta_merged_row.py`   | `test0()` in `SubcolumnLongBetaTest.java` (Surefire: `SubcolumnLongBetaTest#test0`)                                                                                                                                                                         | Writes `result/compression_vs_beta/subcolumn_beta_{1..31}.csv`. Panels (b)–(d) read `dataset/*.csv` directly. Output: `fig/compression_cost_beta_merged_row.png` / `.eps`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Figure 13: Ablation (full sub-column vs without BPE / RLE / DE)                  | `ablation_study.py`                           | `test0()` in `SubcolumnFullTest.java`, `SubcolumnWithoutBPETest.java`, `SubcolumnWithoutRLETest.java`, `SubcolumnWithoutDETest.java` — all delegate to `SubcolumnAblationPruneNewEngine.runAblationBenchmark` (**§5.3**)                                                                                                                        | Fresh runs: `result/subcolumn_full.csv`, `subcolumn_without_bp.csv`, `subcolumn_without_rle.csv`, `subcolumn_without_de.csv` (times). **Ratio panels** read frozen backups: `result/subcolumn_full2.csv`, `subcolumn_without_bp2.csv`, `subcolumn_without_rle2.csv`, `subcolumn_without_de2.csv`. Output: `fig/ablation_study.png` / `.eps`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Figure 14: Block size vs compression ratio / time (prune vs no-prune)            | `compression_vs_block_prune_mean_line.py`     | `testBlockSizeBenchmark()` in `SubcolumnPruneNewBlockSizeTest.java` (with pruning) and `SubcolumnPruneNewBlockSizeNoPruneTest.java` (without pruning) (**§5.2**)                                                                                                                                                          | **With pruning:** `SubcolumnPruneNewBlockSizeTest#testBlockSizeBenchmark` → `result/compression_vs_block_prune_fast/subcolumn_block_{32..8192}.csv` (uses `SubcolumnPruneNewTest.Encoder` / `Decoder`). **Without pruning:** `SubcolumnPruneNewBlockSizeNoPruneTest#testBlockSizeBenchmark` → `result/compression_vs_block_noprune/subcolumn_block_*.csv` (slow boolean-based beta search; decode still via `SubcolumnPruneNewTest.Decoder`). Output: `fig/block_size_comparison_pruning_mean_line.png` / `.eps`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

---

## 5. PruneNew, block-size, and ablation benchmarks

All classes below live under `iotdb/iotdb-core/tsfile/src/test/java/org/apache/iotdb/tsfile/encoding/`. Before running, set each test’s `parentDir` / `parent_dir` to your `{basedir}` (forward slashes, trailing slash), e.g. `D:/path/to/subcolumn/`.

Run Maven from `{basedir}/iotdb` (see **§3.2**). On Windows, prefer the project venv Python at `{basedir}/.venv/Scripts/python.exe` for plotting scripts.

### 5.1 `SubcolumnPruneNewTest` (main codec + Figure 11)

**Reference implementation** for the optimized sub-column codec (BPE + RLE + dictionary encoding, β ∈ {2, 3, 4}, group cache, inner-loop `cost >= cMin` early-break in `Subcolumn()`).

| Item | Value |
| ---- | ----- |
| Class | `SubcolumnPruneNewTest.java` |
| Benchmark method | `test0()` |
| Block size | 512 |
| Repeat count | 100 (`repeatTime`) |
| Input | All `dataset/*.csv` (one float column per file) |
| Output | `result/subcolumn_adddict_prunenew_opt2.csv` |
| Plot consumer | `merge_compression_ratio_time_de_relayout.py` (column label **Sub-column**) |

**CSV columns:** `Dataset`, `Encoding Algorithm`, `Encoding Time`, `Decoding Time`, `Points`, `Compressed Size`, `Compression Ratio`, `For Time`, `Subcolumn Encode Time`.

**Encoder path in `test0()`:** default `Encoder(...)` with `USE_ALPHA_HYBRID = false` and `USE_ALPHA_FAST_HYBRID = false`. The same file also exposes `EncoderHybridAlpha` / `EncoderFastHybridAlpha` (optional β-order heuristics); those are **not** used by Figure 11 or the ablation **Full** baseline.

**Maven:**

```powershell
cd iotdb
mvn test -pl iotdb-core/tsfile "-Dtest=SubcolumnPruneNewTest#test0" "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"
```

Related Figure 11 companions (same PruneNew stack, different front-end):

- `SPRINTZSubcolumnPruneNewTest#test0` → `result/sprintz_subcolumn_adddict_prunenew_opt2.csv`
- `TSDIFFSubcolumnPruneNewTest#test0` → `result/ts2diff_subcolumn_adddict_prunenew_opt2.csv`

### 5.2 Block-size sweep (Figure 14)

Compares **fast sub-column planning (with pruning)** vs **legacy slow planning (without pruning)** across block sizes 32 … 8192 on 13 named datasets.

| Curve | Java test | Encode | Decode | Output directory |
| ----- | --------- | ------ | ------ | ---------------- |
| **With pruning** | `SubcolumnPruneNewBlockSizeTest#testBlockSizeBenchmark` | `SubcolumnPruneNewTest.Encoder` | `SubcolumnPruneNewTest.Decoder` | `result/compression_vs_block_prune_fast/` |
| **Without pruning** | `SubcolumnPruneNewBlockSizeNoPruneTest#testBlockSizeBenchmark` | Local `Encoder` (boolean/`ArrayList` β search, same decisions as old `SubcolumnPruneTest`) | `SubcolumnPruneNewTest.Decoder` | `result/compression_vs_block_noprune/` |

Both tests use `repeatTime = 200`, cap `maxDecimal` at 8, and write one CSV per block size: `subcolumn_block_{size}.csv`.

The no-prune test is **much slower** (especially at large block sizes). Run it separately first; do not pair it with the fast test in one long Surefire invocation unless you intend to wait.

**Maven (run separately):**

```powershell
cd iotdb

# Without pruning (slow)
mvn test -pl iotdb-core/tsfile "-Dtest=SubcolumnPruneNewBlockSizeNoPruneTest#testBlockSizeBenchmark" "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"

# With pruning (fast; uses SubcolumnPruneNewTest)
mvn test -pl iotdb-core/tsfile "-Dtest=SubcolumnPruneNewBlockSizeTest#testBlockSizeBenchmark" "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"
```

**Plot:**

```powershell
cd {basedir}
.\.venv\Scripts\python.exe compression_vs_block_prune_mean_line.py
```

Output: `fig/block_size_comparison_pruning_mean_line.png` / `.eps`.

> **Note:** `SubcolumnPruneFastTest#testBlockSizeBenchmark` writes under `result/compression_vs_block_noprune_legacy/` and is **not** used by Figure 14 in this checkout.

### 5.3 Ablation study (Figure 13)

Ablation reuses the PruneNew wire format but switches **which encoding strategies participate in sub-column planning** via a shared engine and four thin JUnit wrappers.

**Core engine:** `SubcolumnAblationPruneNewEngine.java`

| `Mode` | Meaning in `Subcolumn()` |
| ------ | ------------------------ |
| `FULL` | BPE, RLE, and DE all allowed (aligned with `SubcolumnPruneNewTest#test0` default path) |
| `WITHOUT_BPE` | BPE is excluded from β grouping and per-group encoding-type choice; RLE/DE unchanged |
| `WITHOUT_RLE` | RLE excluded |
| `WITHOUT_DE` | Dictionary encoding (DE) excluded |

Disabling a mode affects **strategy selection only** (which of type 0/1/2 is chosen). The byte layout (`SubcolumnEncoder` / `SubcolumnDecoder`) is unchanged; RLE/DE paths still use bit-packing for metadata and payloads.

**Test wrappers** (each calls `runAblationBenchmark(outputPath, mode)`):

| Test | Mode | Output CSV |
| ---- | ---- | ---------- |
| `SubcolumnFullTest#test0` | `FULL` | `result/subcolumn_full.csv` |
| `SubcolumnWithoutBPETest#test0` | `WITHOUT_BPE` | `result/subcolumn_without_bp.csv` |
| `SubcolumnWithoutRLETest#test0` | `WITHOUT_RLE` | `result/subcolumn_without_rle.csv` |
| `SubcolumnWithoutDETest#test0` | `WITHOUT_DE` | `result/subcolumn_without_de.csv` |

**Benchmark settings** (in `runAblationBenchmark`): `blockSize = 512`, `repeatTime = 100` (check source if you change it), all `dataset/*.csv`, `maxDecimal` capped at 8. CSV has 7 columns (no separate For / sub-column encode timing).

**Maven (all four variants):**

```powershell
cd iotdb
mvn test -pl iotdb-core/tsfile `
  "-Dtest=SubcolumnFullTest#test0,SubcolumnWithoutBPETest#test0,SubcolumnWithoutRLETest#test0,SubcolumnWithoutDETest#test0" `
  "-Dcheckstyle.skip=true" "-Dmaven.checkstyle.skip=true" "-Dspotless.check.skip=true"
```

**Plotting (`ablation_study.py`):**

- **Encode/decode time panels** — read the four fresh CSVs above (`Encoding Time` / `Decoding Time`, normalized per point).
- **Compression-ratio panel** — reads frozen backups `result/subcolumn_full2.csv`, `subcolumn_without_bp2.csv`, `subcolumn_without_rle2.csv`, `subcolumn_without_de2.csv`. After a full re-run, copy or rename new ratio columns into the `*2.csv` files if you want the ratio panel to match the latest run.

```powershell
cd {basedir}
.\.venv\Scripts\python.exe ablation_study.py
```

Output: `fig/ablation_study.png` / `.eps`.

**Maintenance note:** `SubcolumnAblationPruneNewEngine` is a fork of the PruneNew codec with `Mode` hooks (including the same `cost >= cMin` early-break as `SubcolumnPruneNewTest`). Keep it in sync when changing the main PruneNew planner.
