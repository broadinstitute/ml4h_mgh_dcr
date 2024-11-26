import os
import pandas as pd
import shutil
import argparse

class NoteType:
    default_mapping = {'text': 'Report_Text', 'date': 'Report_Date_Time', 'linker_id': 'linker_id'}
    
    def __init__(self, filename, note_type, column_mapping=None):
        """
        Initializes the NoteType instance.

        :param filename: The name of the input file.
        :param note_type: A string representing the file type.
        :param column_mapping: Optional. A dictionary mapping default columns to actual column names in the file.
                               If None, the default mapping is used.
        """
        self.filename = filename
        self.note_type = note_type
        self.column_mapping = column_mapping if column_mapping else NoteType.default_mapping

    def get_actual_columns(self):
        """
        Returns a list of actual column names to be used when reading the file.

        :return: List of actual column names.
        """
        return list(self.column_mapping.values())

    def map_to_default_columns(self, df):
        """
        Renames the DataFrame columns from actual names to default names.

        :param df: The DataFrame with actual column names.
        :return: DataFrame with columns renamed to default names.
        """
        reverse_mapping = {v: k for k, v in self.column_mapping.items()}
        df = df.rename(columns=reverse_mapping)
        return df

    def get_dtypes(self):
        """
        Returns a dictionary mapping column names to their data types, excluding date columns.

        :return: Dictionary of {column_name: dtype}
        """
        dtypes = {
            self.column_mapping['text']: str,
            self.column_mapping['linker_id']: 'Int64'  # Use 'Int64' for nullable integer
        }
        return dtypes

    def get_parse_dates(self):
        """
        Returns a list of column names that should be parsed as dates.

        :return: List of column names to parse as dates.
        """
        return [self.column_mapping['date']]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process TSV files and convert them to Parquet files grouped by linker_id.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing input TSV files.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to store output Parquet files.')
    parser.add_argument('--temp_dir', type=str, required=True, help='Temporary directory for intermediate CSV files.')
    args = parser.parse_args()
    return args

def main():
    # Parse command-line arguments
    args = parse_arguments()
    input_dir = args.input_dir
    output_dir = args.output_dir
    temp_dir = args.temp_dir

    # Create output and temp directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # List of known file types and their column mappings
    known_note_types = {
        'Hnp': None,  # None value indicate default column mapping
        'Car': None,
        'Opn': None,
        'Dis': None,
        'End': None,
        'Pat': None,
        'Prg': None,
        'Pul': None,
        'Rad': None,
        'Vis': None,
        'Trn': {'text': 'Comments', 'date': 'Transaction_Date_Time', 'linker_id': 'linker_id'},
        'Lno': {'text': 'Comments', 'date': 'LR_Note_Date', 'linker_id': 'linker_id'},
        'Mic': {'text': 'Organism_Text', 'date': 'Microbiology_Date_Time', 'linker_id': 'linker_id'},
    }

    # Adjust chunk_size based on your system's memory
    chunk_size = 100000  # Number of rows read per chunk

    # Process all files in the input directory
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        if os.path.isfile(input_file):
            matched_note_type = None
            for note_type, column_mapping in known_note_types.items():
                if note_type in filename:
                    matched_note_type = NoteType(
                        filename=input_file,
                        note_type=note_type,
                        column_mapping=column_mapping
                    )
                    break
            if matched_note_type is None:
                print(f"Skipping file '{filename}' as it doesn't match any known note types.")
                continue

            note_type_instance = matched_note_type
            note_type = note_type_instance.note_type
            actual_columns = note_type_instance.get_actual_columns()
            print(f'Processing file: {input_file}')
            reader = pd.read_csv(
                input_file,
                sep='|',
                usecols=actual_columns,
                chunksize=chunk_size,
                dtype=note_type_instance.get_dtypes(),
                parse_dates=note_type_instance.get_parse_dates()            )
            for chunk in reader:
                # Map actual columns to default columns
                chunk = note_type_instance.map_to_default_columns(chunk)
                chunk['note_type'] = note_type
                # Drop rows where 'linker_id' is NA
                chunk = chunk.dropna(subset=['linker_id'])
                # Group by 'linker_id' within the chunk
                grouped = chunk.groupby('linker_id')
                for linker_id, group in grouped:
                    temp_file = os.path.join(temp_dir, f'{linker_id}.csv')
                    # Append to the per-linker_id CSV file
                    if os.path.exists(temp_file):
                        group.to_csv(temp_file, mode='a', header=False, index=False, sep='|')
                    else:
                        group.to_csv(temp_file, mode='w', header=True, index=False, sep='|')
        else:
            print(f"Skipping '{filename}' as it is not a file.")

    # Convert temporary CSV files to Parquet
    print('Converting CSV files to Parquet...')
    for temp_file in os.listdir(temp_dir):
        temp_file_path = os.path.join(temp_dir, temp_file)
        if os.path.isfile(temp_file_path):
            linker_id = os.path.splitext(temp_file)[0]
            df = pd.read_csv(
                temp_file_path,
                dtype={'text': str, 'linker_id': int},
                parse_dates=['date'],
                sep='|'
            )
            parquet_file = os.path.join(output_dir, f'{linker_id}.notes.parquet')
            df.to_parquet(parquet_file, index=False)
        else:
            print(f"Skipping '{temp_file}' as it is not a file.")

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_dir)
    print('Processing complete.')

if __name__ == '__main__':
    main()

