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
3. Use pathlib to locate and load the config file? This really shouln't be an issue.
    * Allow user to pass path of config file as argument in CLI.
