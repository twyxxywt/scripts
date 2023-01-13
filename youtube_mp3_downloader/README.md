# YouTube MP3 downloader
Download from YouTube playlist(s) and convert to MP3s.

## 🧐 Functionalities

1. Read off a config file containing YT playlists and download folder locations.
2. Randomize all songs and prefix number to filename - for devices that cannot do shuffle play.
3. Ability to re-randomize all songs.

## 🎓 Future improvements

1. Check and see if MP3 already exists and not re-download again.
2. Performance enhancements utilzing concurrency (multiprocessing and/or threading) in certain parts of the code.
    * When checking if video is already downloaded or not against YT playlist?
    * When reverting prefix number from filename?
3. Right now it's using two folders approach to randomize+rename final files. Keeping the original downloads in <source> intact. Very optimized at this point because it destroys the <destination> folder (containing the 'final' files), re-create, and copies all MP3 files from <source> for operation.
4. Use pathlib instead of os package to locate and load the config file? This really isn't an issue but nice to have.
    * Allow user to pass path of config file as argument (argparse) in CLI.
5. Current output using yaspin package looks a bit funky during runtime - sleep() issue?
