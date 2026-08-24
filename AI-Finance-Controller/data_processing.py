import pandas as pd

# =========================
# 1. LOAD DATA
# =========================

expenses = pd.read_csv("data/Expenses_clean.csv")
income = pd.read_csv("data/Income_clean.csv")

print("Original Expenses:", expenses.shape)
print("Original Income:", income.shape)


# =========================
# 2. CLEAN COLUMN NAMES
# =========================

expenses.columns = (
    expenses.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

income.columns = (
    income.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nExpense columns:")
print(expenses.columns.tolist())

print("\nIncome columns:")
print(income.columns.tolist())


# =========================
# 3. REMOVE DUPLICATES
# =========================

expenses = expenses.drop_duplicates()
income = income.drop_duplicates()


# =========================
# 4. DISPLAY MISSING VALUES
# =========================

print("\nMissing values - Expenses:")
print(expenses.isnull().sum())

print("\nMissing values - Income:")
print(income.isnull().sum())


# =========================
# 5. CLEAN ALL TEXT COLUMNS
# =========================

for column in expenses.select_dtypes(include="object"):
    expenses[column] = expenses[column].astype(str).str.strip()

for column in income.select_dtypes(include="object"):
    income[column] = income[column].astype(str).str.strip()


# =========================
# 6. FIND DATE AND AMOUNT COLUMNS
# =========================

print("\nExpenses data types:")
print(expenses.dtypes)

print("\nIncome data types:")
print(income.dtypes)


# =========================
# 7. SAVE CLEANED COPIES
# =========================

expenses.to_csv(
    "data/Expenses_processed.csv",
    index=False
)

income.to_csv(
    "data/Income_processed.csv",
    index=False
)

print("\nCleaning completed!")
print("Saved:")
print("data/Expenses_processed.csv")
print("data/Income_processed.csv")

# =========================
# 8. ADD TRANSACTION TYPE
# =========================

expenses["type"] = "Expense"
income["type"] = "Revenue"


# =========================
# 9. COMBINE BOTH DATASETS
# =========================

transactions = pd.concat(
    [expenses, income],
    ignore_index=True
)


# =========================
# 10. REMOVE DUPLICATES
# =========================

transactions = transactions.drop_duplicates()


# =========================
# 11. SORT DATA
# =========================

# If your dataset has a column called "date"
if "date" in transactions.columns:
    transactions["date"] = pd.to_datetime(
        transactions["date"],
        errors="coerce"
    )

    transactions = transactions.sort_values(
        by="date"
    )


# =========================
# 12. RESET INDEX
# =========================

transactions = transactions.reset_index(
    drop=True
)


# =========================
# 13. SAVE MASTER DATASET
# =========================

transactions.to_csv(
    "data/transactions.csv",
    index=False
)


# =========================
# 14. DISPLAY RESULT
# =========================

print("\n==============================")
print("MASTER DATASET CREATED")
print("==============================")

print("Rows:", len(transactions))
print("Columns:", len(transactions.columns))

print("\nColumns:")
print(transactions.columns.tolist())

print("\nFirst 5 transactions:")
print(transactions.head())

print("\nTransaction types:")
print(transactions["type"].value_counts())