import os
import json
import hashlib
from tkinter import Tk
from fragment import Fragment
from tkinter import filedialog

def browse_file():
    # Create a Tkinter window for browsing files/folders
    root = Tk()
    root.withdraw()

    # Ask the user to select a file or folder
    file_path = filedialog.askopenfilename(initialdir=os.getcwd())

    # Define the file_data variable
    file_data = b''

    # Read the file/folder data
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()
    elif os.path.isdir(file_path):
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'rb') as file:
                    file_data += file.read()

    return file_data, os.path.basename(file_path)

def fragment_file(file_data, fragment_size):
    num_fragments = (len(file_data) + fragment_size - 1) // fragment_size
    fragments = []
    file_hash = hashlib.sha256()
    for i in range(num_fragments):
        start = i * fragment_size
        end = (i + 1) * fragment_size
        fragment_data = file_data[start:end]
        fragment_hash = hashlib.sha256(fragment_data).hexdigest()
        fragment_id = f"{i+1}/{num_fragments}"
        if i < num_fragments - 1:
            next_fragment_data = file_data[end:end+fragment_size]
            next_fragment_hash = hashlib.sha256(next_fragment_data).hexdigest()
        else:
            next_fragment_hash = None
        fragments.append(Fragment(fragment_id, fragment_hash, len(fragment_data), next_fragment_hash))
        file_hash.update(fragment_data)
    return fragments, file_hash.hexdigest()

def browse_and_fragment():
    # Browse for a file
    file_data, file_name = browse_file()

    # Fragment the file
    fragment_size = (len(file_data) + 2) // 3
    first_fragment, file_hash = fragment_file(file_data, fragment_size)

    # Process the metadata
    metadata = {'file_name': file_name, 'file_hash': file_hash, 'num_fragments': len(file_data) // fragment_size + 1}

    print(f"File {file_name} fragmented and metadata processed")

    return first_fragment, metadata