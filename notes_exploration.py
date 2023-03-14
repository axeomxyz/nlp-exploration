import os
import pandas as pd
import re

uppercase_words_regex = r'\b[A-Z]+\b'

def list_documents(directory: str) -> list:
    """
    Iterates over all files and sub-folders of the input directory,
    filters only for ".doc" and "docx" files and returns their filenames in a list.

    Parameters:
    directory (str): An absolute path to a directory.

    Returns:
    List[str]: A list of filenames for ".doc" and ".docx" files in the directory and its sub-folders.
    """
    doc_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".docx"):  # ".doc"
                doc_files.append(file)
    return doc_files


def parse_filename(filename: str) -> dict:
    """
    Parses a string in the format "<client> <date> pos <pos1> <pos2> <sesions> <keywords>"
    and returns a dictionary with the extracted values.

    Parameters:
    string (str): A string in the specified format.

    Returns:
    dict: A dictionary with the extracted values.
    """
    # Split the string into parts (removing extension)
    parts = os.path.splitext(filename)[0].split()

    # Extract the values
    client = parts[0]
    date = parts[1]
    pos = ''
    sessions = 0
    keywords = ''
    keywords_start_idx = 4
    # Read positions and sessions after pos
    if parts[3].isdigit():
        pos += parts[3]
    if len(parts) > 5 and parts[4].isdigit() and not parts[5].isdigit():
        sessions = parts[4]
        keywords_start_idx = 5
    if len(parts) > 6 and parts[4].isdigit() and parts[5].isdigit():
        pos += ',' + parts[4]
        sessions = parts[5]
        keywords_start_idx = 6

    keywords = " ".join(parts[keywords_start_idx:])
    if '+' in keywords:
        keywords = keywords.replace('+', ',')
    keywords = keywords.replace('axel', '')
    keywords = keywords.replace('sessions', '')
    keywords = keywords.replace('session', '')

    # Create and return the dictionary
    return {"file": filename, "client": client, "date": date, "position": pos, "sessions": sessions,
            "keywords": keywords}


def process_documents(doc_list: list) -> pd.DataFrame:
    """
    Process a list of document filenames and return a Pandas DataFrame containing the parsed records.

    Parameters:
    doc_list (list): A list of document filenames to be parsed.

    Returns:
    pd.DataFrame: A Pandas DataFrame containing the parsed records, with columns for filename, client initials,
                  date, position, sessions, and keywords.

    Raises:
    Exception: If an error occurs during parsing of a filename, an error message is printed to the console.

    """
    df = pd.DataFrame(columns=['file', 'client', 'date', 'position', 'sessions', 'keywords'])
    for filename in doc_list:
        try:
            new_record = parse_filename(filename)
            df.loc[len(df)] = new_record
        except Exception as e:
            print(f'Error parsing file: {filename}')
    return df


dir = '/Users/apereira/Documents/Upshot/US02 - Pronotez/dataset'
csv_dir = './filenames_parsed.csv'
docs = list_documents(dir)
pos_filter = lambda filename: ' pos ' in filename.lower()
docs_with_pos = list(filter(pos_filter, docs))
df = process_documents(docs_with_pos)
df.to_csv(csv_dir)
# doc_filter = lambda filename: filename.endswith('.doc')
# docx_filter = lambda filename: filename.endswith('.docx')
# plus_filter = lambda filename: '+' in filename
# session_filter = lambda filename: 'session' in filename
# not_session_filter = lambda filename: 'session' not in filename

# format_filename_lambda = lambda f: f.split()

# doc_list = list(filter(doc_filter, docs))
# docx_list = list(filter(docx_filter, docs))
# docs_with_pos = list(filter(pos_filter, docs))
# docs_with_plus = list(filter(plus_filter, docs_with_pos))
# docs_with_sessions = list(filter(session_filter, docs_with_pos))
# docs_not_sessions = list(filter(not_session_filter, docs_with_pos))


# df = pd.read_csv(csv_dir)
# upper_matches = df['keywords'].apply(lambda x: re.findall(r'\b[A-Z]+\b', x)).explode().unique()
# upper_matches = [x for x in upper_matches if pd.notna(x)]
# alfanum_matches = df['keywords'].apply(lambda x: re.findall(r'\b[A-Za-z\d]+-[A-Za-z\d]+\b', x)).explode().unique()
# alfanum_matches = [x for x in alfanum_matches if pd.notna(x)]
# print(upper_matches)
# print(alfanum_matches)

