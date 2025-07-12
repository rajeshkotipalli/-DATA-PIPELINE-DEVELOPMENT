import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def extract_data(file_path):
    print("🔹 Reading data from file...")
    return pd.read_csv(file_path)

def transform_data(df):
    print("🔹 Starting data preprocessing...")

    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = df.select_dtypes(include=['object']).columns

    # Numeric pipeline: handle missing + scale
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Categorical pipeline: handle missing + encode
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))  # Important fix!
    ])

    # Combine both pipelines
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_pipeline, numeric_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

         
    processed_data = preprocessor.fit_transform(df)
    print("✅ Preprocessing done.")
    return processed_data, preprocessor.get_feature_names_out()

def save_data(processed_data, column_names, output_path):
    print(f"🔹 Saving processed data to '{output_path}'...")
    df_output = pd.DataFrame(processed_data, columns=column_names)
    df_output.to_csv(output_path, index=False)
    print("✅ File saved successfully.")

def main():
    input_file = input("Enter input CSV file path: ").strip()
    output_file = input("Enter name for output CSV file (e.g., cleaned_data.csv): ").strip()

    try:
        df = extract_data(input_file)
        processed_data, column_names = transform_data(df)
        save_data(processed_data, column_names, output_file)
        print("🎉 ETL Pipeline completed successfully!")
    except Exception as e:
        print("❌ Something went wrong:", e)

if __name__ == "__main__":
    main()
