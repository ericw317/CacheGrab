from CustomLibs import file_signatures as FS
import shutil
import os

# get file signature
def get_file_type(file_path):
    with open(file_path, 'rb') as file:
        file_bytes = file.read(12).hex().upper()
        for signature in FS.signatures:
            if signature in file_bytes:
                return FS.signatures[signature]
        return None

# parse cache
def main(cache_dir, output_dir, type_list):
    # loop through each file in the cache directory
    for cache_file in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, cache_file)

        # get extension
        try:
            extension = get_file_type(file_path)
        except PermissionError:
            continue

            # if valid signature and selected file type then output to output directory
        if extension is not None and extension[1:] in type_list:
            shutil.copy(file_path, os.path.join(output_dir, f"{cache_file}{extension}"))
