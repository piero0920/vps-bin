import os, json, pathlib

with open('data-main.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())


folderFiles = []


for root, dirs, files in os.walk(r"E:\google_drive\VODS\VOD - 2022"):
    for file in files:
        if file.endswith(".mp4"):
            file_name = os.path.join(root, file)
            print(os.path.join(root, file))            
            for entry in data:
                if file.startswith(f'{entry["id"]}'):                    
                    print(f'EXITS - {file_name}')
                    folderFiles.append(file_name)
                #else:
                    #print(f'DONT - {entry["id"]}')

dateFiles = []
'''
newDateFilesList = []
twoDateFilesList = []
trheDateFilesList = []
fourDateFilesList = []
fiveDateFilesList = []
sixDateFilesList = []
for file in folderFiles:
    dateName = os.path.basename(file)[0:8]
    parent = pathlib.Path(file).parent.resolve()
    b2Folder = r'E:\b2_data\vods'
    newName = os.path.join(b2Folder, dateName + '-{0}.mp4')    

    if dateName not in newDateFilesList:
        newDateFilesList.append(dateName)
        os.rename(file, newName.format('1'))        
    elif dateName not in twoDateFilesList:
        twoDateFilesList.append(dateName)
        os.rename(file, newName.format('2'))
    elif dateName not in trheDateFilesList:
        trheDateFilesList.append(dateName)
        os.rename(file, newName.format('3'))
    elif dateName not in fourDateFilesList:
        fourDateFilesList.append(dateName)
        os.rename(file, newName.format('4'))
    elif dateName not in fiveDateFilesList:
        fiveDateFilesList.append(dateName)
        os.rename(file, newName.format('5'))
    elif dateName not in sixDateFilesList:
        sixDateFilesList.append(dateName)
        os.rename(file, newName.format('6'))
    else:
        print('CHECk --- ' + file)

print(f'dups {twoDateFilesList}')
print(f'thrs {trheDateFilesList}')
print(f'fous {fourDateFilesList}')
print(f'fivs {fiveDateFilesList}')
print(f'sixs {sixDateFilesList}')
'''