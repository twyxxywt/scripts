import os
import random
import re
import shutil
from time import perf_counter, sleep

import moviepy.editor as mp  # Cconvert the mp4 to wavv then mp3
from pytube import Playlist, YouTube
from yaspin import yaspin
from yaspin.spinners import Spinners

#####
### https://www.pythontutorial.net/python-concurrency/python-threading/
### https://www.pythontutorial.net/python-concurrency/python-threadpoolexecutor/ See if we can try ThreadPoolExecutor to speed up downloads!
### https://www.pythontutorial.net/python-concurrency/python-multiprocessing/ See if we can multiprocessing to speed up converting to MP3!
### https://www.pythontutorial.net/python-concurrency/python-processpoolexecutor/
#####


MP3_FOLDER = './mp3/'
MP3_FOLDER_RENAME = './mp3-renamed/'


def mp3_download_convert():
    MP3_FILES: list = os.listdir(MP3_FOLDER)
    print('\nDownloading and converting YouTube playlist!\n')
    with yaspin(color='yellow', attrs=['bold', 'blink']) as spinner:
        for url in PLAYLIST:
            spinner.spinner = Spinners.clock
            sleep(0.2)

            song_title = YouTube(url).title
            # When actually downloading the song some character gets blank out.
            # Do not append ".mp3" because of the conversion process.
            song_title = (
                song_title.replace("'", '')
                .replace('*', '')
                .replace('#', '')
                .replace('"', '')
                .replace(',', '')
                .replace('|', '')
                .replace('.', '')
                .replace('/', '')
                .replace('?', '')
                .replace(':', '')
                .replace('$', '')
                .replace('~', '')
            )
            if song_title + '.mp3' in MP3_FILES:
                spinner.text = f'Skip downloading "{song_title}"'
            else:
                spinner.spinner = Spinners.fistBump
                spinner.text = f'Processing "{song_title}"... '
                YouTube(url).streams.filter(only_audio=True).first().download(
                    MP3_FOLDER
                )

                spinner.write(f'Downloading and converting {song_title} to MP3...')
                mp4_path = os.path.join(MP3_FOLDER, song_title + '.mp4')
                mp3_path = os.path.join(
                    MP3_FOLDER, os.path.splitext(song_title)[0] + '.mp3'
                )
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)


def mp3_rename():
    with yaspin(color='yellow', attrs=['bold', 'blink']) as spinner:
        # Re-copying all files.
        spinner.spinner = Spinners.clock
        spinner.text = f'Copying MP3s from "{MP3_FOLDER}" to "{MP3_FOLDER_RENAME}"...'
        shutil.rmtree(MP3_FOLDER_RENAME)
        shutil.copytree(MP3_FOLDER, MP3_FOLDER_RENAME)

        # Random the MP3 songs.
        spinner.text = f'Randomize MP3 files in "{MP3_FOLDER_RENAME}"...'
        MP3_FILES: list = os.listdir(MP3_FOLDER_RENAME)
        random.shuffle(MP3_FILES)

        for count, item in enumerate(MP3_FILES, 1):
            MP3_NAME = str(count) + 'X - ' + item
            spinner.text = f'Renaming "{item}" to "{MP3_NAME}"...'
            sleep(0.2)

            os.rename(
                os.path.join(MP3_FOLDER_RENAME + item),
                os.path.join(MP3_FOLDER_RENAME + MP3_NAME),
            )


def mp3_rename_revert():
    with yaspin(color='yellow', attrs=['bold', 'blink']) as spinner:
        spinner.spinner = Spinners.clock

        RENAMED_MP3_FILES: list = os.listdir(MP3_FOLDER_RENAME)
        REGEX_PATTERN = '^(\d{1}|\d{2}|\d{3})(\w+\s-\s)'

        for file_name in RENAMED_MP3_FILES:
            spinner.text = f'Removing prefix from "{file_name}"...'
            sleep(0.2)

            str_to_remove = re.match(REGEX_PATTERN, file_name)
            os.rename(
                os.path.join(MP3_FOLDER_RENAME + file_name),
                os.path.join(
                    MP3_FOLDER_RENAME + file_name.replace(str_to_remove.group(0), '')
                ),
            )


if __name__ == '__main__':
    start_time = perf_counter()

    with open('.config/yt_playlists.txt') as playlist_file:
        playlists = [line for line in playlist_file]

    for playlist in playlists:
        PLAYLIST = Playlist(playlist).video_urls
        mp3_download_convert()
        mp3_rename()
        # mp3_rename_revert()

    end_time = perf_counter()
    print(f'\n✅ Took {end_time - start_time:0.2f} seconds to complete.')
