# Moral Machine Dataset — Setup & Preprocessing

This project analyses data from the [Moral Machine experiment](https://www.nature.com/articles/s41586-018-0637-6), a large-scale study on human moral decision-making in autonomous vehicle scenarios.

---

## Requirements

Make sure you have the following Python packages installed:

```bash
pip install pandas pyarrow tqdm
```

---

## Dataset Download

The raw datasets are **not included** in this repository due to their size (~several GB). You need to download them manually.

1. Go to: [https://osf.io/3hvt2/files/osfstorage](https://osf.io/3hvt2/files/osfstorage)
2. Navigate to **Datasets → Moral Machine Data**
3. Download the following two files:
   - `SharedResponses.csv.tar.gz`
   - `SharedResponsesSurvey.csv.tar.gz`
4. Unzip both files to obtain the `.csv` files
5. Place the extracted `.csv` files inside a folder named `Datasets/` in the project root (create it if it doesn't exist)

Your folder structure should look like this:

```
project-root/
├── Datasets/
│   ├── SharedResponses.csv
│   └── SharedResponsesSurvey.csv
├── generate_parquet_script.py
├── merge_datasets.ipynb
└── README.md
```

---

## Preprocessing Steps

### Step 1 — Generate the Parquet file

Run the `generate_parquet_script.py` script to generate the `SharedResponses_clean.parquet` memory-efficient dataset format:

This script:
- Drops unnecessary columns
- Removes rows with missing values
- Optimises data types (booleans, uint8, categories) to significantly reduce memory usage
- Outputs `SharedResponses_clean.parquet` into the `Datasets/` folder

> **Note:** The raw `SharedResponses.csv` contains ~70 million rows. The conversion may take several minutes but only needs to be run once. The resulting Parquet file is substantially smaller and faster to read than the original CSV.

### Step 2 — Merge the datasets

Open and run `merge_datasets.ipynb` in Jupyter Notebook.

This notebook:
- Reads `SharedResponses_clean.parquet` in chunks to keep memory usage low
- Merges demographic survey data from `SharedResponsesSurvey.csv` on `ExtendedSessionID`
- Outputs the final merged dataset as `SharedResponses_merged.csv`

> **Expected output:** ~62 million rows × 40 columns, ~8 GB in memory. Approximately 16% of rows will have matched survey data.

---

## Notes

- The merged CSV output is also too large for version control and is therefore excluded from this repository via `.gitignore`. Re-generate it by following the steps above.
- If you encounter memory issues, consider reducing `CHUNK_SIZE` in the scripts.
