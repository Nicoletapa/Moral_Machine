import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

INPUT_FILE  = "Datasets/SharedResponses.csv"
OUTPUT_FILE = "Datasets/SharedResponses_clean.parquet"
CHUNK_SIZE  = 500_000

cols_to_drop = [
    "UserID", "ResponseID",
    "LeftHand", "ScenarioType",
    "Template", "DescriptionShown", "ScenarioOrder"
]

char_cols = [
    "Man", "Woman", "Pregnant", "Stroller", "OldMan", "OldWoman",
    "Boy", "Girl", "Homeless", "LargeWoman", "LargeMan", "Criminal",
    "MaleExecutive", "FemaleExecutive", "FemaleAthlete", "MaleAthlete",
    "FemaleDoctor", "MaleDoctor", "Dog", "Cat"
]

bool_cols     = ["Barrier", "Intervention", "DefaultChoiceIsOmission", "Saved", "PedPed"]
category_cols = ["ExtendedSessionID", "UserCountry3", "DefaultChoice", "NonDefaultChoice", "AttributeLevel", "ScenarioTypeStrict"]
uint8_cols    = ["NumberOfCharacters", "CrossingSignal"] + char_cols
int8_cols     = ["DiffNumberOFCharacters"]

def process_chunk(chunk):
    # Step 1 — drop unwanted columns
    chunk = chunk.drop(columns=cols_to_drop, errors="ignore")

    # Step 2 — drop all rows with any nulls
    chunk = chunk.dropna()

    # Step 3 — fix corrupted Man values then cast
    chunk["Man"] = pd.to_numeric(chunk["Man"], errors="coerce")
    chunk = chunk.dropna(subset=["Man"])  # drop the 2 corrupted rows

    # Step 4 — cast dtypes (no nullable types needed since no nulls)
    for col in uint8_cols:
        chunk[col] = chunk[col].astype("uint8")

    for col in int8_cols:
        chunk[col] = chunk[col].astype("int8")

    for col in bool_cols:
        chunk[col] = chunk[col].astype("bool")

    for col in category_cols:
        chunk[col] = chunk[col].astype("category")

    return chunk

# ── Read → process → write ──────────────────────────────────────────────────
writer    = None
total_in  = 0
total_out = 0

for i, chunk in enumerate(pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE)):
    total_in += len(chunk)
    chunk = process_chunk(chunk)
    total_out += len(chunk)

    table = pa.Table.from_pandas(chunk)
    if writer is None:
        writer = pq.ParquetWriter(OUTPUT_FILE, table.schema)
    writer.write_table(table)

    if i % 10 == 0:
        print(f"Processed {(i + 1) * CHUNK_SIZE:,} rows...")

writer.close()
print(f"\nRows before:  {total_in:,}")
print(f"Rows after:   {total_out:,}")
print(f"Rows dropped: {total_in - total_out:,}")
print(f"Saved to {OUTPUT_FILE}")