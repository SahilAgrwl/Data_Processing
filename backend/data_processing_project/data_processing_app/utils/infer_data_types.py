import pandas as pd
from io import TextIOWrapper
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

def infer_and_convert_data_types(file, delimiter=None, sheet_name=None):
    try:
        # Rewind the file pointer to the beginning
        file.seek(0)

        # Use TextIOWrapper to wrap the file, allowing Pandas to read it
        wrapped_file = TextIOWrapper(file, encoding='utf-8')

          # Read the contents of the file using Pandas with optional parameters
        if file.name.endswith('.csv'):
            df = pd.read_csv(wrapped_file, delimiter=delimiter)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(wrapped_file, sheet_name=sheet_name)
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

         # Loop through columns to infer and convert data types
        for col in df.columns:
            if is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].nunique() / len(df[col]) < 0.05:
                # If the column has low cardinality, consider it as categorical
                df[col] = df[col].astype('category')
            elif df[col].apply(lambda x: isinstance(x, str)).all():
                # If all values in the column are strings, consider it as string data type
                df[col] = df[col].astype(str)

        return {'success': True, 'data': df.to_dict(orient='records')}

    
    except pd.errors.ParserError as pe:
        raise ValueError(f'Error parsing data: {str(pe)}')
    except Exception as e:
        raise ValueError(f'Error processing data: {str(e)}')

        
