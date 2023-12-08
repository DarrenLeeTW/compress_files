import os
import json
import zipfile
from datetime import datetime, timedelta

def read_config(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

def get_files_to_compress(source_dir, days_before):
    target_date = datetime.now() - timedelta(days=days_before)
    files_to_compress = []

    for foldername, subfolders, filenames in os.walk(source_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            file_modification_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modification_date < target_date:
                files_to_compress.append(file_path)

    return files_to_compress

def compress_files(files, destination_dir, source_dir):
    today = datetime.now().strftime("%Y-%m-%d")
    zip_file_path = os.path.join(destination_dir, f"compressed_{today}.zip")

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.relpath(file, source_dir))
            print(f"Compressed {file}")

# 主程序
config = read_config(r"config.json")
files_to_compress = get_files_to_compress(config["source_directory"], config["days_before"])
compress_files(files_to_compress, config["destination_directory"], config["source_directory"])
