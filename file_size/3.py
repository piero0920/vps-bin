

errors = ['a', 'b', 'c']

files = ['aaaa', 'a', 'sd', 'xf', 'sccc', 'ffff', 'qqwew']

for file in files:
    if any(f in file for f in errors):
        print(file)
    else:
        print(f'{file}  --- ssssssssss')