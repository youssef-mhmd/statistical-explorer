import pandas as pd
import numpy as np
import os
import re

def parse_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    headers = []

    # Find the first markdown table
    for i, line in enumerate(lines):
        if '|' in line and i + 1 < len(lines) and re.match(r'^[|\s\-:]+$', lines[i+1].strip()):
            start_idx = i
            # Extract headers
            headers = [cell.strip() for cell in line.split('|') if cell.strip()]
            break

    if start_idx == -1:
        raise ValueError("No markdown table found in the selected file.")

    rows = []
    # Skip header and separator
    for line in lines[start_idx + 2:]:
        line = line.strip()
        if not line or not line.startswith('|'):
            break
        
        # Split by | and clean up
        cells = [cell.strip() for cell in line.split('|')]
        # Filter out empty cells caused by leading/trailing pipes
        if line.startswith('|'): cells = cells[1:]
        if line.endswith('|'): cells = cells[:-1]
        
        # Ensure row matches header length or pad/truncate
        row_data = [c.strip() for c in cells]
        if len(row_data) > len(headers):
            row_data = row_data[:len(headers)]
        elif len(row_data) < len(headers):
            row_data += [""] * (len(headers) - len(row_data))
            
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers)

    # Clean data and attempt type conversion
    for col in df.columns:
        # Convert checkbox icons to Booleans
        if df[col].dtype == object:
            if df[col].apply(lambda x: '✅' in str(x) or '❌' in str(x)).any():
                df[col] = df[col].apply(lambda x: True if '✅' in str(x) else False)
                continue

        # Try numeric conversion
        try:
            temp_ser = pd.to_numeric(df[col].replace('—', np.nan))
            df[col] = temp_ser
        except (ValueError, TypeError):
            # Keep as object/string if it fails
            pass

    return df

if __name__ == "__main__":
    # Test with provided file if exists
    try:
        data = parse_dataset('cs-students-dataset.md')
        print("Successfully parsed markdown table!")
        print(data.head())
    except Exception as e:
        print(f"Test failed: {e}")
