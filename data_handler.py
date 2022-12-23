import json, subprocess, requests, os, pathlib, cv2, re

with open('data-main.json', 'r', encoding='utf-8')as f:
    data = json.loads(f.read())


def gameThumbnail():
    for entry in data:
        for game in entry["games"]:
            if game["gameArtURL"]:
                game_new_name = game["gameName"].replace(" ", "-").lower()
                game_new_name = re.sub(r'[/\\:*?"<>|]', '--', game_new_name)
                game_url = game["gameArtURL"]
                game_path = './thumbnails/games/'+game_new_name + '.jpg'
                if (os.path.isfile(game_path) is False):
                    print('Downloading: ' + game_new_name)
                    img_data = requests.get(game_url).content

                    with open(game_path, 'wb') as handler:
                        handler.write(img_data)
                else:
                    print('Skiping: ' + game_new_name)
            else:
                print('No gameArtURL for ' + game["gameName"])


def clipThumbnail():
    for entry in data:
        if entry["clips"] != []:
            for clip in entry["clips"]:
                clip_name = str(clip["view_count"]) + "-" + clip["slug"]
                clip_url = clip["thumbnail_url"]
                clip_path = './thumbnails/clips/' + clip_name + '.jpg'
                if (os.path.isfile(clip_path) is False):
                    print('Downloading: ' + clip_name)
                    img_data = requests.get(clip_url).content
                    with open(clip_path, 'wb') as handler:
                        handler.write(img_data)
                else:
                    print('Skiping: ' + clip_name)


def clipDownload():
    for entry in data:
        for clip in entry["clips"]:
            clips_path = f'./clips/{entry["id"]}'
            if(os.path.isdir(clips_path) is False):
                os.makedirs(clips_path)
            clip_name = str(clip["view_count"]) + "-" + clip["slug"]
            clip_slug = clip["slug"]
            clip_path = os.path.join(clips_path, clip_name + '.mp4')
            clip_path_ts = os.path.join(clips_path, clip_name + '.ts')
            if (os.path.isfile(clip_path) is False):
                print('Downloading: ' + clip_name)
                subprocess.call(['TwitchDownloaderCLI', 'clipdownload', '--id', clip_slug, '-q', 'best', '--output', clip_path])
                print('proccesing: ' + clip_path_ts)
                subprocess.call(['ffmpeg', '-i', clip_path, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'mpegts', clip_path_ts], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                print('Skiping: ' + clip_name)

def clipCompile():
    main_path = './clips'
    folders = os.listdir(main_path)

    for folder in folders:
        files = os.listdir(os.path.join(main_path, folder))
        clip_folder = str(pathlib.Path(os.path.join(main_path, folder)).absolute())
        if files != []:
            for file in files:
                if file.endswith('.ts'):
                    clip = str(pathlib.Path(os.path.join(main_path, folder, file)).absolute())
                    with open(clip_folder + '/clips.txt', 'a', encoding='utf-8') as f:
                        f.write("file '" + clip + "'\n")
            compile_path = clip_folder + f'/{folder}-full.mp4'
            if(os.path.isfile(compile_path) is False):
                print(f'Compiling {clip_folder}')
                subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', clip_folder + '/clips.txt', '-c', 'copy', compile_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                for file in files:
                    if file.endswith('.ts'):
                        clip_ts = str(pathlib.Path(os.path.join(main_path, folder, file)).absolute())
                        os.remove(clip_ts)
                    if file.startswith('clips') or file.endswith('.txt') or file == 'clips.txt':
                        clip_txt = str(pathlib.Path(os.path.join(main_path, folder, file)).absolute())
                        os.remove(clip_txt)                    
            else:
                print('Skiping compilation for ' + compile_path)
            

def clipCompileThumbnail():
    main_path = './clips'
    folders = os.listdir(main_path)
    for folder in folders:
        files = os.listdir(os.path.join(main_path, folder))
        clip_folder = str(pathlib.Path(os.path.join(main_path, folder)).absolute())
        if files != []:
            compile_path = clip_folder + f'/{folder}-full.mp4'
            compile_thumbnail = f'./thumbnails/clips/{folder}-full.jpg'
            if(os.path.isfile(compile_thumbnail) is False):
                print('Creating thumbnail for ' + folder + ' compilation')
                subprocess.call(['ffmpeg', '-i', compile_path, '-ss', '00:00:00.000', '-vframes', '1', compile_thumbnail], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                print('Thumbnail for ' + compile_thumbnail + ' already exits')


def uploadFiles(folder):
    upload = folder
    if (os.path.isdir(upload) is True):
        print('Uploading :' + upload)
        subprocess.call(['rclone', 'copy', upload, 'b2:kala-media/'+upload, '-P'])
    else:
        print(upload + ' folder does not exits')
                
def addClipsData():
    for entry in data:
        if entry["clips"] != []:
            compilation_path = f"clips/{entry['id']}/{entry['id']}-full.mp4"
            video = cv2.VideoCapture(compilation_path)
            frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video.get(cv2.CAP_PROP_FPS)
            duration = int(frame_count/fps)
            clipCompilation = {
                "title": f"Top clips compilation for {entry['main']['date']}.",
                "date": entry['main']['date'],
                "clipURL": f"https://data.kalathrasarchives.com/clips/{entry['id']}-full.mp4",
                "thumbnailURL": f"https://data.kalathrasarchives.com/thumbnails/clips/{entry['id']}-full.jpg",
                "b2ID": f"{entry['id']}-full",
                "duration": duration
            }
            if clipCompilation not in entry["clips"]:
                print('Adding clip compilation to DATA')
                entry["clips"].append(clipCompilation)
            else:
                print('clip compilation data already exits in DATA')
            for clip in entry["clips"]:                
                if "slug" in clip:
                    clip["thumbnailURL"] = f'https://data.kalathrasarchives.com/thumbnails/clips/{str(clip["view_count"]) + "-" + clip["slug"]}.jpg'
                    clip["clipURL"] = f'https://data.kalathrasarchives.com/clips/{str(clip["view_count"]) + "-" + clip["slug"]}.mp4'
                    clip["b2ID"] = f'{str(clip["view_count"]) + "-" + clip["slug"]}'


    with open('data.json', 'w', encoding='utf-8')as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def addGamesData():
    for entry in data:
        if entry["games"] != []:
            for game in entry["games"]:
                print('Adding game data to DATA')
                game_new_name = game["gameName"].replace(" ", "-").lower()
                game_new_name = re.sub(r'[/\\:*?"<>|]', '--', game_new_name)
                game["gameURL"] = f'https://data.kalathrasarchives.com/file/kala-media/thumbnails/games/{game_new_name}.jpg'
                game["b2ID"] = game_new_name


    with open('data.json', 'w', encoding='utf-8')as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#clipThumbnail()
uploadFiles('thumbnails/games')
uploadFiles('thumbnails/clips')