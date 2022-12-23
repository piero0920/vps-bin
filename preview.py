import os, subprocess, threading, time

class ElapsedTimeThread(threading.Thread):
    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time.time()
        while not self.stopped():
            hours, rem = divmod(time.time()-thread_start, 3600)
            minutes, seconds = divmod(rem, 60)
            print("\rElapsed {:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours),int(minutes),seconds), end="")

if __name__ == "__main__":
    start = time.time()
    thread = ElapsedTimeThread()
    thread.start()
    for root, dirs, files in os.walk('E:/b2_data/vods'):
        c = 1
        for file in files:
            errors_files = ['20210917-1', '20210916-1', '20210918-1']
            if file.endswith(".mp4"):
                print()
                if any(f in file for f in errors_files):
                    print(f'    {c}/{len(files)} --------------------------------')
                    print(f'        Skiping file contais error : {os.path.join(root, file)}')
                else:
                    video_path = os.path.join(root, file)
                    temp_path = os.path.join('tmp', file)
                    gif_path = os.path.join('gifs', file[:-3] + 'gif')
                    print(f'    {c}/{len(files)} --------------------------------')
                    if(os.path.isfile(gif_path) is False):
                        print(f'        Speeding up : {video_path}')
                        subprocess.call(['ffmpeg', '-itsscale', '0.004', '-i', video_path, '-an', '-c', 'copy', temp_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                        print(f'        Converting to GIF: {gif_path}')
                        subprocess.call(['ffmpeg', '-i', temp_path, '-pix_fmt', 'rgb24', gif_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                        print(f'        Deleting temp file {temp_path}')
                        os.remove(temp_path)
                    else:
                        print(f'        GIF exits : {gif_path}')
                print()
            c = c + 1
    thread.stop()
    thread.join()
    print()
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Finished in {:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours),int(minutes),seconds))
