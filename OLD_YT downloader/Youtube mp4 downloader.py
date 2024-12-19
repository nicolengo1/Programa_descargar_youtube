import os
import subprocess
import sys
import time

from github import Github
from pytubefix import YouTube, Playlist
from win10toast import ToastNotifier

from Variableenviroments import VariableEnviroments

VERSION = VariableEnviroments.VERSION
GITHUB_TOKEN = VariableEnviroments.GITHUB_TOKEN

toaster = ToastNotifier()

if getattr(sys, 'frozen', False):
    absolute_path = os.path.dirname(sys.executable)
    icon_path = os.path.join(sys._MEIPASS, "sanki.ico")
    ffmpeg_path = os.path.join(absolute_path, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_path):
        print("Error - ffmpeg.exe is not found, please re-download from github zip file "
              "( or put back the ffmpeg.exe file where it was )")
        time.sleep(7)
        exit(0)
elif __file__:
    absolute_path = os.path.dirname(__file__)
    icon_path = "sanki.ico"
    ffmpeg_path = "ffmpeg.exe"

print("Welcome!", end="\n\n")

time.sleep(1)

print("Don't forget to check from time to time my github for updates ;) !", end="\n\n")

try:
    latest_version = Github(GITHUB_TOKEN). \
        get_repo("nicolengo1/Python-youtube-downloader").get_latest_release().title

    VERSION_temp = VERSION[1:]
    VERSION_temp = VERSION_temp.replace('.', '')
    VERSION_temp = int(VERSION_temp)

    latest_version_temp = latest_version[1:]
    latest_version_temp = latest_version_temp.replace('.', '')
    latest_version_temp = int(latest_version_temp)

    if latest_version_temp != VERSION_temp and VERSION_temp < latest_version_temp:
        print("New version detected, go to my github and maybe download it :) !")
        print(f"Actual version = {VERSION}   Latest version = {latest_version}", end="\n\n")
except Exception as error:
    print("An error occured when trying to check for newer versions - ignore")

time.sleep(1)

if not os.path.exists(f"{absolute_path}\\settingsmp4.txt"):

    Download_directory_temp = \
        input("Where do you want to download the videos ?\n"
              "( Write the full path, you can paste it )\n"
              "(If nothing is provided or the directory does not exist,\n"
              "a folder will be created in the directory where the .exe file is )\n"
              " - > ")
    if not os.path.exists(Download_directory_temp):
        Download_directory_temp = os.path.join(absolute_path, "audio")

    os.system('cls')

    try:
        Skip_file_verification_temp = \
            int(input("Do you want to skip checking before downloading if the video was downloaded and it is in the "
                      "folder ?\n"
                      "( 0 for no, 1 for yes )\n"
                      " -> "))
        if Skip_file_verification_temp not in [0, 1]:
            Skip_file_verification_temp = 0
    except Exception:
        Skip_file_verification_temp = 0

    os.system('cls')

    try:
        Skip_log_verification_temp = \
            int(input("Do you want to skip checking before downloading if the video exists in the txt file log ?\n"
                      "( 0 for no, 1 for yes )\n"
                      " -> "))
        if Skip_log_verification_temp not in [0, 1]:
            Skip_log_verification_temp = 0
    except Exception:
        Skip_log_verification_temp = 0

    os.system('cls')

    try:
        Skip_log_writing_temp = int(input("Do you want to skip writing in the txt log ?\n"
                                          "( 0 for no, 1 for yes )\n"
                                          " -> "))
        if Skip_log_writing_temp not in [0, 1]:
            Skip_log_writing_temp = 0
    except Exception:
        Skip_log_writing_temp = 0

    os.system('cls')

    try:
        Audio_bitrate_temp = int(input("What bitrate do you want the audio to be ?\n"
                                       "( higher - better audio quality but consumes more memory )\n"
                                       "( write a number starting from 35 to 256, 128 is recommended and default )\n"
                                       " -> "))
        if Audio_bitrate_temp < 35 or Audio_bitrate_temp > 256:
            Audio_bitrate_temp = 128
    except Exception:
        Audio_bitrate_temp = 128

    os.system('cls')

    try:
        Video_max_resolution_temp = int(input("What is the highest resolution you want your video to be ?\n"
                                              "( higher - larger image per frame, do not confuse with video bitrate )\n"
                                              "( if the value is <0, you will get the highest resolution possible - up to 4k;\n"
                                              "if it is 0, you will get a video with a maximum resolution of 1080;\n"
                                              "if it is >0, you will get the video with the higheste resolution lower or equal to the value "
                                              "- value <= video resolution )\n"
                                              "( write a number starting from -1 up to 4000 )\n"
                                              " -> "))
        if Video_max_resolution_temp <= 0:
            Video_max_resolution_temp = -1
        if Video_max_resolution_temp > 4000:
            Video_max_resolution_temp = 0

    except Exception:
        Video_max_resolution_temp = 0

    os.system('cls')

    settings_file = open(f"{absolute_path}\\settingsmp4.txt", "w")
    settings_file.writelines(f"Download_directory = {Download_directory_temp}\n"
                             f"Skip_file_verification = {Skip_file_verification_temp}\n"
                             f"Skip_log_verification = {Skip_log_verification_temp}\n"
                             f"Skip_log_writing = {Skip_log_writing_temp}\n"
                             f"Audio_bitrate = {Audio_bitrate_temp}\n"
                             f"Video_resolution = {Video_max_resolution_temp}\n\n"
                             "Download directory = copy the full path for a folder where to download\n"
                             "Skip_... = 0 for don't skip and 1 for skip\n"
                             "The file verification checks if the video exists in the folder\n\n"
                             "The log verification checks if in the txt file exists the video title\n\n"
                             "The log writing appends in the txt file the video title\n\n"
                             "The audio bitrate is a value between 35 and 256 - 128 recomended;\n "
                             "the higher the better the audio quality will be but it will take more memory\n\n"
                             "The video resolution is a value between -1 and 4000 - 1080 recomended\n\n"
                             "For the changes to take action a restart of the app is needed\n"
                             "and the txt file needs to be saved")

    print("Settings file created!", end="\n\n")

    print("All the settings can be changed in the txt settings file where the .exe is.")
    time.sleep(4)

    DOWNLOAD_DIR = Download_directory_temp
    SKIP_FILE_VERIFICATION = Skip_file_verification_temp
    SKIP_LOG_VERIFICATION = Skip_log_verification_temp
    SKIP_LOG_WRITING = Skip_log_writing_temp
    AUDIO_BITRATE = f"{Audio_bitrate_temp}k"
    VIDEO_MAX_RESOLUTION = Video_max_resolution_temp

    settings_file.close()
else:
    settings_file = open(f"{absolute_path}\\settingsmp4.txt", "r")

    try:
        DOWNLOAD_DIR = settings_file.readline()

        if DOWNLOAD_DIR is not None and DOWNLOAD_DIR != '' and DOWNLOAD_DIR != '\n':
            if DOWNLOAD_DIR[len(DOWNLOAD_DIR) - 1] == '\n':
                DOWNLOAD_DIR = DOWNLOAD_DIR[:-1]
            DOWNLOAD_DIR = DOWNLOAD_DIR[21:]

            if DOWNLOAD_DIR == "None" or DOWNLOAD_DIR is None or not os.path.exists(DOWNLOAD_DIR):
                raise Exception("Download directory does not exist or isn't valid!")
        else:
            raise Exception("Download directory does not exist, isn't valid or isn't specified!")

    except Exception as error:
        print(f"Error with Download directory - {error} - defaulted to the .exe location")
        DOWNLOAD_DIR = os.path.join(absolute_path, "audio")

    try:
        SKIP_FILE_VERIFICATION = settings_file.readline()

        if SKIP_FILE_VERIFICATION is not None and SKIP_FILE_VERIFICATION != '' and SKIP_FILE_VERIFICATION != '\n':
            if SKIP_FILE_VERIFICATION[len(SKIP_FILE_VERIFICATION) - 1] == '\n':
                SKIP_FILE_VERIFICATION = SKIP_FILE_VERIFICATION[:-1]
            SKIP_FILE_VERIFICATION = SKIP_FILE_VERIFICATION[25:]

            if SKIP_FILE_VERIFICATION not in ['0', '1']:
                raise Exception("Skip file verification is not 0 or 1!")
            else:
                SKIP_FILE_VERIFICATION = int(SKIP_FILE_VERIFICATION)
        else:
            raise Exception("Skip file verification is not specified!")
    except Exception as error:
        print(f"Error with Skip file verification value - {error} - defaulted to 0")
        SKIP_FILE_VERIFICATION = 0

    try:
        SKIP_LOG_VERIFICATION = settings_file.readline()

        if SKIP_LOG_VERIFICATION is not None and SKIP_LOG_VERIFICATION != '' and SKIP_LOG_VERIFICATION != '\n':
            if SKIP_LOG_VERIFICATION[len(SKIP_LOG_VERIFICATION) - 1] == '\n':
                SKIP_LOG_VERIFICATION = SKIP_LOG_VERIFICATION[:-1]
            SKIP_LOG_VERIFICATION = SKIP_LOG_VERIFICATION[24:]

            if SKIP_LOG_VERIFICATION not in ['0', '1']:
                raise Exception("Skip log verification is not 0 or 1!")
            else:
                SKIP_LOG_VERIFICATION = int(SKIP_LOG_VERIFICATION)
        else:
            raise Exception("Skip log verification is not not specified!")

    except Exception as error:
        print(f"Error with Skip log verification value - {error} - defaulted to 0")
        SKIP_LOG_VERIFICATION = 0

    try:
        SKIP_LOG_WRITING = settings_file.readline()
        if SKIP_LOG_WRITING is not None and SKIP_LOG_WRITING != '' and SKIP_LOG_WRITING != '\n':
            if SKIP_LOG_WRITING[len(SKIP_LOG_WRITING) - 1] == '\n':
                SKIP_LOG_WRITING = SKIP_LOG_WRITING[:-1]
            SKIP_LOG_WRITING = SKIP_LOG_WRITING[19:]

            if SKIP_LOG_WRITING not in ['0', '1']:
                raise Exception("Skip log verification is not 0 or 1!")
            else:
                SKIP_LOG_WRITING = int(SKIP_LOG_WRITING)
        else:
            raise Exception("Skip log verification is not not specified!")

    except Exception as error:
        print(f"Error with Skip log writing value - {error} - defaulted to 0")
        SKIP_LOG_WRITING = 0

    try:
        AUDIO_BITRATE = settings_file.readline()
        if AUDIO_BITRATE is not None and AUDIO_BITRATE != '' and AUDIO_BITRATE != '\n':
            if AUDIO_BITRATE[len(AUDIO_BITRATE) - 1] == '\n':
                AUDIO_BITRATE = AUDIO_BITRATE[:-1]
            AUDIO_BITRATE = AUDIO_BITRATE[16:]

            AUDIO_BITRATE = int(AUDIO_BITRATE)

            if AUDIO_BITRATE < 35 or AUDIO_BITRATE > 256:
                raise Exception("Audio bitrate is not between 35 and 256!")

            AUDIO_BITRATE = f"{AUDIO_BITRATE}k"
        else:
            raise Exception("Audio bitrate is not specified!")

    except Exception as error:
        print(f"Error with Audio bitrate value - {error} - defaulted to 128")
        AUDIO_BITRATE = "128k"

    try:
        VIDEO_MAX_RESOLUTION = settings_file.readline()
        if VIDEO_MAX_RESOLUTION is not None and VIDEO_MAX_RESOLUTION != '' and VIDEO_MAX_RESOLUTION != '\n':
            if VIDEO_MAX_RESOLUTION[len(VIDEO_MAX_RESOLUTION) - 1] == '\n':
                VIDEO_MAX_RESOLUTION = VIDEO_MAX_RESOLUTION[:-1]
            VIDEO_MAX_RESOLUTION = VIDEO_MAX_RESOLUTION[19:]

            VIDEO_MAX_RESOLUTION = int(VIDEO_MAX_RESOLUTION)

            if VIDEO_MAX_RESOLUTION < 0:
                VIDEO_MAX_RESOLUTION = -1

            if VIDEO_MAX_RESOLUTION < -1 or VIDEO_MAX_RESOLUTION > 4000:
                raise Exception("Video resolution is not between -1 and 4000!")

        else:
            raise Exception("Video resolution is not specified!")

    except Exception as error:
        print(f"Error with Video resolution value - {error} - defaulted to 1080")
        VIDEO_MAX_RESOLUTION = -1

    settings_file.close()

DOWNLOAD_DIR_AUDIO_LOG = os.path.join(DOWNLOAD_DIR, "download_log_mp4.txt")

if not os.path.exists(f"{DOWNLOAD_DIR}"):
    os.mkdir(f"{DOWNLOAD_DIR}")

if not os.path.exists(f"{DOWNLOAD_DIR}\\mp4"):
    os.mkdir(f"{DOWNLOAD_DIR}\\mp4")

if not os.path.exists(DOWNLOAD_DIR_AUDIO_LOG):
    log = open(DOWNLOAD_DIR_AUDIO_LOG, "x")
    log.close()


def ReplaceTitle(title):
    """
    Replaces the invalid characters in "title" that cannot be used to name a file in windows.
    :param title: The character string.
    :return: Title with invalid characters erased.
    """
    title_length = len(title)
    i = 0
    while i < title_length:
        if title[i] in '\\/:*?"<>|':
            title = title[:i] + title[i + 1:]
            title_length = title_length - 1
        else:
            i = i + 1

    return title


def SuccesfullNotification():
    """
    Shows a notification in windows sidebar when the download is complete.
    :return: None
    """
    try:
        print('')
        os.chdir(absolute_path)

        print("All videos were downloaded \n")
        toaster.show_toast("YouTube Downloader", "All videos were downloaded!", duration=0,
                           icon_path=icon_path)

        time.sleep(3)

        os.system('cls')
    except Exception:
        pass


def DownloadMP4FromYouTube(video_url, folder_name="random", modify_volume=0):
    """
    Downloads the highest mp4 quality file from a YouTube video link and puts it in a "folder_name" folder.
    First it downloads the mp3 file and then the audio-less mp4 and merges both together into a mp4 file using ffmpeg.
    :param video_url: The YouTube video url.
    :param folder_name: The folder in which the video will be downloaded ( if it's a single video, the folder will
    be named "random", if it's a playlist, the folder will be named the playlist title ). The folder will be created in
    the "DOWNLOAD_DIR" path.
    :return:
    """
    i = 1
    audio_video_youtube = None
    video_youtube = None

    while i < 10:
        try:
            audio_video_youtube = YouTube(
                video_url).streams.filter(
                progressive=False, only_audio=True).get_audio_only()

            video_youtube = YouTube(video_url).streams.filter(progressive=False, type="video"). \
                get_highest_resolution(VIDEO_MAX_RESOLUTION)
        except Exception as error:
            i = i + 1
            print(error)
            continue
        break

    if audio_video_youtube is not None and video_youtube is not None:
        video_title = ReplaceTitle(video_youtube.title)
        print(video_title)

        if not os.path.exists(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}"):
            os.mkdir(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}")

        if SKIP_FILE_VERIFICATION == 0:
            os.chdir(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}")

            if f"{video_title}.mp4" in os.listdir():
                raise Exception("The video was already downloaded ( it is in the folder )")

        download_log = open(DOWNLOAD_DIR_AUDIO_LOG, "r", encoding="UTF-8")

        not_in_log = 0

        if SKIP_LOG_VERIFICATION == 0:

            for lines in download_log:
                if lines[:-1] == video_title:
                    download_log.close()
                    raise Exception("The video was already downloaded ( it is in the log )")

            not_in_log = 1

        download_log.close()

        audio_video_youtube.download(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}", filename=f"{video_title}_temp.mp3")

        video_youtube.download(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}", filename=f"{video_title}_temp.mp4")

        subprocess.call([f"{ffmpeg_path}", "-y", "-i",
                         f"{DOWNLOAD_DIR}\\mp4\\{folder_name}\\{video_title}_temp.mp4", "-i",
                         f"{DOWNLOAD_DIR}\\mp4\\{folder_name}\\{video_title}_temp.mp3", "-c:v", "copy", "-filter:a",
                         f"volume={modify_volume}dB", "-c:a", "libmp3lame", "-b:a", f"{AUDIO_BITRATE}",
                         f"{DOWNLOAD_DIR}\\mp4\\{folder_name}\\{video_title}.mp4"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

        try:
            os.remove(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}\\{video_title}_temp.mp3")
        except Exception:
            pass

        try:
            os.remove(f"{DOWNLOAD_DIR}\\mp4\\{folder_name}\\{video_title}_temp.mp4")
        except Exception:
            pass

        if not_in_log == 1 and SKIP_LOG_WRITING == 0:
            download_log = open(DOWNLOAD_DIR_AUDIO_LOG, "a", encoding="UTF-8")
            download_log.write(f"{video_title}\n")
            download_log.close()

        print("Video downloaded succesfully")

    else:
        raise Exception("The link is not valid!")


while True:
    url_to_download = input(
        "Write the link of the playlist or video ( to exit press only the enter key ) -> ")
    print('')

    if url_to_download != '':
        if "watch" in url_to_download or "short" in url_to_download:

            try:
                DownloadMP4FromYouTube(url_to_download)
            except Exception as error:
                print(f"Error - {error}")
            else:
                SuccesfullNotification()

            print('')

        elif "playlist" in url_to_download:
            try:
                playlist = Playlist(url_to_download)
                playlist_title = ReplaceTitle(playlist.title)

                start_or_end = int(input(
                    "Do you want to download the videos starting from the start or the end? ( 1 or 0 ) -> "))
                print('')

                if start_or_end == 1:
                    for video_url in playlist.video_urls:
                        try:
                            DownloadMP4FromYouTube(video_url, playlist_title)
                        except Exception as error:
                            print(f"Error - {error}")

                        print('')

                elif start_or_end == 0:
                    playlist_length = len(playlist) - 1

                    for i in range(playlist_length, 0, -1):

                        try:
                            video_url = playlist[i]
                            DownloadMP4FromYouTube(video_url, playlist_title)
                        except Exception as error:
                            print(f"Error - {error}")

                        print('')

            except Exception as error:
                print(f"Error - {error}")

            else:
                SuccesfullNotification()

        else:
            print("The link is not valid!")

    elif url_to_download == '':
        print("Bye bye :)")
        time.sleep(3)
        break
