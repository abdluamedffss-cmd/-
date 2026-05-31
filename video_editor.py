import shutil

def process_video(input_file, output_file):
    shutil.copy(input_file, output_file)
    return output_file
