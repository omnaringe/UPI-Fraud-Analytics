import pandas as pd
import mysql.connector
from getpass import getpass

# ============================================================
# SETTINGS
# ============================================================

CSV_FILE = "Data/upi_fraud_cleaned.csv"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_DATABASE = "upi_fraud"
MYSQL_TABLE = "transactions"


# ============================================================
# LOAD CSV
# ============================================================

print("\nLoading cleaned CSV...")

df = pd.read_csv(CSV_FILE)

print(f"Rows found: {len(df):,}")
print(f"Columns found: {len(df.columns)}")


# ============================================================
# CLEAN VALUES FOR MYSQL
# ============================================================

boolean_columns = [
    "UnusualLocation",
    "UnusualAmount",
    "NewDevice",
    "FraudFlag"
]

for col in boolean_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().map({
            "true": 1,
            "false": 0,
            "1": 1,
            "0": 0
        })


# Convert NaN / NaT to None
df = df.where(pd.notnull(df), None)


# ============================================================
# MYSQL CONNECTION
# ============================================================

print("\nConnecting to MySQL...")

password = getpass("Enter MySQL password: ")

connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=password,
    database=MYSQL_DATABASE
)

cursor = connection.cursor()

print("Connected successfully!")


# ============================================================
# GET TABLE COLUMNS
# ============================================================

cursor.execute(f"DESCRIBE {MYSQL_TABLE}")

mysql_columns = [
    row[0]
    for row in cursor.fetchall()
]

print(f"\nMySQL table columns: {len(mysql_columns)}")


# ============================================================
# MATCH CSV COLUMNS WITH MYSQL COLUMNS
# ============================================================

missing_columns = [
    col for col in mysql_columns
    if col not in df.columns
]

extra_columns = [
    col for col in df.columns
    if col not in mysql_columns
]

if missing_columns:
    print("\nMissing columns:")
    print(missing_columns)

    cursor.close()
    connection.close()

    raise Exception("CSV and MySQL table columns do not match.")


if extra_columns:
    print("\nExtra CSV columns:")
    print(extra_columns)


df = df[mysql_columns]


# ============================================================
# CREATE INSERT QUERY
# ============================================================

column_names = ", ".join(
    f"`{col}`"
    for col in mysql_columns
)

placeholders = ", ".join(
    ["%s"] * len(mysql_columns)
)

insert_query = f"""
INSERT INTO {MYSQL_TABLE}
({column_names})
VALUES ({placeholders})
"""


# ============================================================
# PREPARE DATA
# ============================================================

data = []

for row in df.itertuples(index=False, name=None):

    cleaned_row = []

    for value in row:

        if pd.isna(value):
            cleaned_row.append(None)

        elif isinstance(value, pd.Timestamp):
            cleaned_row.append(value.to_pydatetime())

        elif isinstance(value, (pd.Int64Dtype,)):
            cleaned_row.append(int(value))

        else:
            cleaned_row.append(value)

    data.append(tuple(cleaned_row))


# ============================================================
# CLEAR EXISTING DATA
# ============================================================

cursor.execute(
    f"DELETE FROM {MYSQL_TABLE}"
)

connection.commit()

print("\nExisting table data cleared.")


# ============================================================
# INSERT DATA
# ============================================================

print("\nImporting data into MySQL...")

batch_size = 500

for i in range(0, len(data), batch_size):

    batch = data[i:i + batch_size]

    cursor.executemany(
        insert_query,
        batch
    )

    connection.commit()

    print(
        f"Imported {min(i + batch_size, len(data)):,}"
        f" / {len(data):,}"
    )


# ============================================================
# VERIFY
# ============================================================

cursor.execute(
    f"SELECT COUNT(*) FROM {MYSQL_TABLE}"
)

total_rows = cursor.fetchone()[0]

print("\n" + "=" * 60)
print("IMPORT COMPLETED")
print("=" * 60)

print(f"Rows in MySQL: {total_rows:,}")


# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("\nMySQL connection closed.")