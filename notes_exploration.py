import os
import pandas as pd


df = pd.DataFrame(columns=['file', 'client', 'date', 'position', 'session1', 'session2', 'session3'])


def process_documents(directory: str) -> list:
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
    Parses a string in the format "<client> <date> pos <pos1> <pos2> <pos3> <sessions>"
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
    session1 = ''
    session2 = ''
    session3 = ''
    sessions_idx = 4
    if 'pos' in parts[2].lower():
        if parts[3].isdigit():
            pos += ' ' + parts[3]
        if len(parts) > 4 and parts[4].isdigit():
            pos += ' ' + parts[4]
            sessions_idx = 5
        if len(parts) > 5 and parts[5].isdigit():
            pos += ' ' + parts[5]
            sessions_idx = 6
    if len(parts) > sessions_idx:
        sessions = " ".join(parts[sessions_idx:])
        if '+' in sessions:
            sess_split = sessions.split('+')
            session1 = sess_split[0]
            session2 = sess_split[1]
            if len(sess_split) > 2:
                session3 = sess_split[2]
        else:
            session1 = sessions

    # Create and return the dictionary
    return {"file": filename, "client": client, "date": date, "position": pos, "session1": session1, "session2": session2, "session3": session3}


dir = '/Users/apereira/Documents/Upshot/US02 - Pronotez/dataset'
docs = process_documents(dir)
doc_filter = lambda filename: filename.endswith('.doc')
docx_filter = lambda filename: filename.endswith('.docx')
pos_filter = lambda filename: ' pos ' in filename.lower()
plus_filter = lambda filename: '+' in filename
session_filter = lambda filename: 'session' in filename
not_session_filter = lambda filename: 'session' not in filename

format_filename_lambda = lambda f: f.split()

# doc_list = list(filter(doc_filter, docs))
# docx_list = list(filter(docx_filter, docs))
docs_with_pos = list(filter(pos_filter, docs))
# docs_with_plus = list(filter(plus_filter, docs_with_pos))
# docs_with_sessions = list(filter(session_filter, docs_with_pos))
# docs_not_sessions = list(filter(not_session_filter, docs_with_pos))

for filename in docs_with_pos:
    try:
        new_record = parse_filename(filename)
        df.loc[len(df)] = new_record
    except Exception as e:
        print(f'Error parsing file: {filename}')

df.to_csv('filenames_parsed.csv', index=False)
