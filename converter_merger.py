import sys
import cv2
import os
import subprocess

# Create a subfolder for outputs
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Prompt user to choose option
user_choice = input("Enter '1' for file type conversion or '2' for merge/extract option: ")

# Get list of all files in folder
folder_path = os.getcwd()
files = os.listdir(folder_path)

if user_choice == '1':
    # Prompt user for desired file type
    file_type = input("Enter desired file type (aac, mp3, waw, opus, mp4, mkv, m4a, webm, ogg*): ")

    # Convert each file to desired file type
    for file in files:
        if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm') or file.endswith('.aac') or file.endswith('.mp3') or file.endswith('.waw') or file.endswith('.opus') or file.endswith('.m4a') or file.endswith('.ogg'):
            output_file = os.path.splitext(file)[0] + '.' + file_type
            output_path = os.path.join(output_folder, output_file)
            subprocess.call(['ffmpeg', '-i', file, '-vn', '-acodec', file_type, output_path])

elif user_choice == '2':
    # Prompt user for merge or extract audio option
    merge_or_extract = input("Enter 'm' to merge videos or 'e' to extract audio: ")

    if merge_or_extract == 'm':
        # Filter list of files to only include .mp4, .mkv, .webm, or .m4a files
        valid_files = [file for file in files if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm') or file.endswith('.m4a')]

        # Create list of input files for FFmpeg concat filter
        input_files = ["file '" + file + "'" for file in valid_files]
        input_files_string = '\n'.join(input_files)

        # Write input file list to text file
        with open("input_files.txt", "w") as file:
            file.write(input_files_string)

        # Use FFmpeg concat filter to merge files
        output_file_merged = 'Merged' + '.' + 'mp4'
        output_path = os.path.join(output_folder, output_file_merged)
        subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'input_files.txt', '-c', 'copy', output_path])

    elif merge_or_extract == 'e':
        # Extract audio from each file
        for file in files:
            if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm') or file.endswith('.m4a'):
                output_file = 'Extracted_from_' + os.path.splitext(file)[0] + '.aac'
                output_path = os.path.join(output_folder, output_file)
                subprocess.call(['ffmpeg', '-i', file, '-vn', '-acodec', 'aac', output_path])
    else:
        print("Invalid option entered.")
else:
    print("Invalid option entered.")
