from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "data"

for keyword in ["expenses", "income"]:
    matches = sorted(data_dir.glob(f"*{keyword}*.csv"), key=lambda p: p.name.lower())
    if not matches:
        print(f"Missing file matching: *{keyword}*.csv")
        continue

    path = matches[0]
    df = pd.read_csv(path)
    print(f"\nFILE: {path.name}")
    print(df.head())
    print("Columns:", list(df.columns))
    print("Shape:", df.shape)
    print("-" * 60)