import subprocess

DOWNLOADS_FILE = r"./Ytdl.txt"
LIBRARY_OUTPUT_PATH = r"./SoLib/%(title)s.%(ext)s"
FILES_SUCCESSFULLY_DOWNLOADED = r"./Downloaded.txt"

with open(DOWNLOADS_FILE, encoding="utf8") as f:
    print("Initiating batch download")
    for line in f.read().splitlines()[:]:
        subprocess.call(["youtube-dl",
                        # "-v",
                         "-i",
                         f"ytsearch:{line.strip()}",
                         "-x",
                         "--audio-format",
                         "best",
                         "--audio-quality",
                         "0",
                         "--download-archive",
                         FILES_SUCCESSFULLY_DOWNLOADED,
                         "--add-metadata",
                        #  "--embed-thumbnail",
                         "-o",
                         LIBRARY_OUTPUT_PATH,
                         ])
print("Batch download completed")