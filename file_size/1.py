# get file size in python
import os

file_name = "C:/Users/piero/Desktop/preview/gifs/20210827-1.gif"

file_stats = os.stat(file_name)

print(file_stats)
print(f'File Size in Bytes is {file_stats.st_size}')
print(f'File Size in MegaBytes is {round((file_stats.st_size / 1e+9), 2)}')