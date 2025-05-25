import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

def clean_and_analyze_file(file_path, output_csv="cleaned_initial_dataset.csv"):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    else:
        return {"error": "Unsupported file format."}

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(0, inplace=True)
        elif df[col].dtype.name in ['category', 'bool']:
            df[col].fillna('undefined', inplace=True)
        elif df[col].dtype == 'object':
            df[col].fillna('undefined', inplace=True)

    os.makedirs("uploaded", exist_ok=True)
    cleaned_csv_path = os.path.join("uploaded", output_csv)
    df.to_csv(cleaned_csv_path, index=False)

    numeric_cols = df.select_dtypes(include=['number']).columns
    stats = df[numeric_cols].describe().transpose().round(2)

    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    most_common_col = None
    max_freq = 0
    for col in cat_cols:
        freq = df[col].value_counts().iloc[0]
        if freq > max_freq:
            max_freq = freq
            most_common_col = col

    chart_path = None
    if most_common_col:
        plt.figure(figsize=(10, 5))
        sns.countplot(data=df, x=most_common_col, order=df[most_common_col].value_counts().iloc[:10].index)
        plt.title(f"Top values in '{most_common_col}'")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join("uploaded", "chart.png")
        plt.savefig(chart_path)
        plt.close()

    nulls_before = pd.read_csv(file_path).isnull().sum()
    nulls_after = df.isnull().sum()
    stats_table = tabulate(stats, headers='keys', tablefmt='github', showindex=True) # type: ignore
    nulls_before_table = tabulate(nulls_before.reset_index().values, headers=["العمود", "قبل التنظيف"], tablefmt='github')
    nulls_after_table = tabulate(nulls_after.reset_index().values, headers=["العمود", "بعد التنظيف"], tablefmt='github')

    return {
        "first_rows": df.head().to_string(),
        "last_rows": df.tail().to_string(),
        "nulls_before": nulls_before,
        "nulls_after": nulls_after,
        "stats": stats,
        "chart_path": chart_path,
        "cleaned_file": cleaned_csv_path,
        "shape": df.shape,
        "sample_head": df.head().to_string(),
        "stats_table": stats_table,
        "nulls_before_table": nulls_before_table,
        "nulls_after_table": nulls_after_table
    }
