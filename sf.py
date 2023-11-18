import pandas as pd

def convert_xlsx_to_csv(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file)

    # Save as CSV file
    df.to_csv(output_file, index=False)

# Example usage
convert_xlsx_to_csv('final_datasett.xlsx', 'final_dataset.csv')