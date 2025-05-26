# ✅ [1] analysis.py - النسخة المتقدمة من تحليل البيانات (مع دعم skiprows و encoding الذكي)

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype, is_object_dtype, is_datetime64_any_dtype

def clean_and_analyze_file(file_path, lang="ar", output_csv="cleaned_initial_dataset.csv"):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".csv":
        encodings = ['utf-8', 'utf-16', 'windows-1256']
        for enc in encodings:
            try:
                df_sample = pd.read_csv(file_path, encoding=enc, nrows=10)
                if any(df_sample.columns.str.contains('[a-zA-Zأ-ي]')):
                    df = pd.read_csv(file_path, encoding=enc)
                else:
                    df = pd.read_csv(file_path, encoding=enc, skiprows=1)
                break
            except Exception:
                continue
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    else:
        return {"error": "Unsupported file format."}

    original_shape = df.shape
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # ✅ فحص وجود أعمدة حقيقية بعد القراءة
    if df.empty or len(df.columns) == 0 or all(col.startswith("unnamed") or col.strip() == "" for col in df.columns.astype(str)):
        return {"error": "الملف لا يحتوي على رؤوس أعمدة مفهومة. الرجاء التحقق من تنسيقه."}

    numeric_cols = [col for col in df.columns if is_numeric_dtype(df[col])]
    text_cols = [col for col in df.columns if is_object_dtype(df[col])]
    date_cols = [col for col in df.columns if is_datetime64_any_dtype(df[col])]

    if lang == "ar":
        summary_text = (
            f"تم تحميل الملف بنجاح\n"
            f"عدد الصفوف: {df.shape[0]}\n"
            f"عدد الأعمدة: {df.shape[1]}\n"
            f"الأعمدة الرقمية: {len(numeric_cols)}\n"
            f"الأعمدة النصية: {len(text_cols)}\n"
            f"الأعمدة الزمنية: {len(date_cols)}"
        )
    else:
        summary_text = (
            f"✅ File loaded successfully\n"
            f"Rows: {df.shape[0]}\n"
            f"Columns: {df.shape[1]}\n"
            f"Numeric columns: {len(numeric_cols)}\n"
            f"Text columns: {len(text_cols)}\n"
            f"Date columns: {len(date_cols)}"
        )


    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, df.nunique() > 1]
    df.drop_duplicates(inplace=True)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].fillna("undefined")
        elif pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]): # type: ignore
            df[col] = df[col].fillna("undefined")

    os.makedirs("uploaded", exist_ok=True)
    cleaned_csv_path = os.path.join("uploaded", output_csv)
    df.to_csv(cleaned_csv_path, index=False)

    stats = df[numeric_cols].describe().transpose().round(2)

    cat_cols = [col for col in df.columns if is_object_dtype(df[col])]
    most_common_col = None
    max_freq = 0
    for col in cat_cols:
        freq = df[col].value_counts().iloc[0]
        if freq > max_freq:
            max_freq = freq
            most_common_col = col

    import matplotlib.pyplot as plt
    from matplotlib import font_manager, rc

    font_path = "fonts/DejaVuSans.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    rc('font', family=font_prop.get_name())

    chart_path = None
    if most_common_col:
        plt.figure(figsize=(10, 5)) # type: ignore
        sns.countplot(data=df, x=most_common_col, order=df[most_common_col].value_counts().iloc[:10].index)
        plt.title(f"Top values in '{most_common_col}'") # type: ignore
        plt.xticks(rotation=45) # type: ignore
        plt.tight_layout() # type: ignore
        chart_path = os.path.join("uploaded", "chart.png")
        plt.savefig(chart_path) # type: ignore
        plt.close() # type: ignore

    font_path = "fonts/DejaVuSans.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    rc('font', family=font_prop.get_name())

    corr_path = None
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr().round(2)
        plt.figure(figsize=(8, 6)) # type: ignore
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title("Correlation Between Numeric Columns") # type: ignore
        corr_path = os.path.join("uploaded", "correlation.png")
        plt.savefig(corr_path) # type: ignore
        plt.close() # type: ignore

    # ✅ محاولة إيجاد target للتنبؤ
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score

    prediction_result = None
    prediction_chart_path = None

    if len(numeric_cols) >= 2:
        candidates = [col for col in numeric_cols if df[col].nunique() > 5 and not col.lower().startswith("id")]
        target_col = None

        keywords = ["target", "price", "amount", "score", "value", "total", "سعر", "قيمة", "الإجمالي", "الهدف", "مجموع", "كمية", "الكمية"]
        for col in candidates:
            if any(word in col.lower() for word in keywords):
                target_col = col
                break

        if not target_col and candidates:
            target_col = candidates[-1]  # آخر رقم محتمل

        if target_col:
            X = df[[col for col in numeric_cols if col != target_col]]
            y = df[target_col]

            if X.shape[1] > 0:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                score = r2_score(y_test, y_pred)

                prediction_result = {
                    "target": target_col,
                    "r2_score": round(score, 3), # type: ignore
                    "sample_prediction": list(zip(y_test.head(5).values, y_pred[:5])),
                }

                font_path = "fonts/DejaVuSans.ttf"
                font_prop = font_manager.FontProperties(fname=font_path)
                rc('font', family=font_prop.get_name())
                
                # رسم بياني للمقارنة
                import matplotlib.pyplot as plt
                plt.figure(figsize=(8, 4))
                plt.scatter(y_test, y_pred, alpha=0.6)
                plt.xlabel("Actual")
                plt.ylabel("Predicted")
                plt.title(f"Prediction of {target_col}")
                plt.grid(True)
                prediction_chart_path = os.path.join("uploaded", "prediction.png")
                plt.savefig(prediction_chart_path)
                plt.close()

    return {
    "summary_text": summary_text,
    "cleaned_file": cleaned_csv_path,
    "chart_path": chart_path,
    "corr_path": corr_path,
    "stats": stats,
    "shape": df.shape,
    "columns": df.columns.tolist(),
    "numeric_cols": numeric_cols,
    "text_cols": text_cols,
    "date_cols": date_cols,
    "prediction_result": prediction_result,
    "prediction_chart_path": prediction_chart_path
}
