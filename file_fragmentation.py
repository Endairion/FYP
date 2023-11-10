import os
import json
import hashlib
from tkinter import Tk
import uuid
from fragment import Fragment
from metadata import FileMetadata
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

    return file_data, os.path.basename(file_path), os.path.getsize(file_path)

def fragment_file(file_data, file_name, file_size, sender):
    file_id = str(uuid.uuid4())
    num_fragments = 3
    fragment_size = (len(file_data) + num_fragments - 1) // num_fragments
    fragment_hashes = []
    fragment_data_list = []
    file_hash = hashlib.sha256()
    for i in range(num_fragments):
        start = i * fragment_size
        end = (i + 1) * fragment_size if i != num_fragments - 1 else len(file_data)
        fragment_data = file_data[start:end]
        fragment_hash = hashlib.sha256(fragment_data).hexdigest()
        fragment_hashes.append(fragment_hash)
        fragment_data_list.append(fragment_data)
        file_hash.update(fragment_data)
    fragments = Fragment(fragment_hashes, num_fragments)
    file_metadata = FileMetadata(file_id, file_name, file_size, fragments, sender, file_hash.hexdigest())
    return file_metadata, fragment_data_list

def browse_and_fragment():
    # Browse for a file
    file_data, file_name, file_size = browse_file()

    file_metadata, fragment_data_list = fragment_file(file_data, file_name, file_size, "Endairion")
    
    print("File Metadata:")
    print(file_metadata.to_dict())

    # Print the fragment data list
    print("Fragment Data List:")
    for fragment_data in fragment_data_list:
        print(fragment_data)

    return file_metadata, fragment_data_list

    