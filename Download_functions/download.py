import os
import subprocess
import yt_dlp as yt
import urllib.request
from tqdm import tqdm

from Settings_functions.settings import SettingsClass

absolute_path = os.path.dirname(__file__)
ffmpeg_path = os.path.join(absolute_path, "ffmpeg.exe")

yt.postprocessor.FFmpegPostProcessor._ffmpeg_location.set(ffmpeg_path)

pbar = None
total_size = 0

# playlist_url = "https://www.youtube.com/playlist?list=PLbxgqNDpPEDnRIK1ByzKuO_klbRmGWOOA"

# playlist_info = yt.YoutubeDL(playlist_info_options).extract_info(playlist_url, download=False)
#
# for entry in playlist_info['entries']:
#     video_title = entry['title']
#     video_url = entry['url']
#
#     print(entry)

# TESTING VALUES
# download_directory_option = "C:\\Users\\nicolas\\Desktop\\PythonProjects\\YTDownloader_YT_DLP\\Downloader\\"
#
# max_res_option = '1080'
#
# overwrite_option = True
#
# quiet_download_option = False
#
# quiet_info_option = True
#
# video_url = 'https://www.youtube.com/watch?v=yjNcXPtNQdE&list=PLbxgqNDpPEDnRIK1ByzKuO_klbRmGWOOA'
#
# audio_bitrate_option = '128'


class DownloaderClass:

    def __init__(self, download_directory_option='/', max_res_option=1080, overwrite_option=False,
                 quiet_download_option=True, quiet_info_option=True, album_cover_option=False, reverse_option=False,
                 video_audio_option=True):

        self.Settings = SettingsClass(download_directory_option, max_res_option, overwrite_option,
                                      quiet_download_option, quiet_info_option, album_cover_option, reverse_option,
                                      video_audio_option)

        self.__info_options = {
            'extract_flat': True,
            'skip_download': True,
            'quiet': self.Settings.GetQuietInfo(),
            'no_warnings': True,
            # 'no_check_certificate': True,
            'nocache': True,
            'no_verify_id': True,
            'proxy': '',
        }

    @staticmethod
    def __ReplaceTitle(title):
        """
        Replaces the invalid characters in "title" that cannot be used to name a file in windows.
        :param title: A string.
        :return: Valid title.
        """
        title_length = len(title)
        i = 0

        while i < title_length:
            if title[i] in '''\\/:*?"<>|''':
                title = title[:i] + title[i + 1:]
                title_length -= 1

            else:
                i += 1

        return title

    @staticmethod
    def __progress_hook(d):
        global pbar, total_size

        if d['status'] == 'downloading':
            if not pbar:
                total_size = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total_size:
                    pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')
                else:
                    print("Couldn't get file size.")

            if pbar:
                pbar.update(d['downloaded_bytes'] - pbar.n)

        elif d['status'] == 'finished':
            if pbar:
                pbar.close()

    def __DownloadYtVideo(self, video_url, folder_name=""):

        if '&list=' in video_url:
            video_url = video_url[:-(len(video_url) - video_url.find('list'))]

        if folder_name != "":
            folder_name = self.__ReplaceTitle(folder_name)
            folder_name = "/" + folder_name + "/"

        try:

            try:
                video_info = yt.YoutubeDL(self.__info_options).extract_info(video_url, download=False)

                # for f in video_info['formats']:
                #     if 'height' in f and f['height'] is not None and f['height'] ==1080 and f['vbr'] is not None:
                #         print(f)

                best_format = max(
                    (f for f in video_info['formats'] if 'height' in f and f['height'] is not None and f['height'] ==1080 and f['vbr'] is not None ) ,
                    key=lambda x: x.get('vbr', 0)
                )

                # print(best_format['vbr'])

            except Exception as error:
                print(f"Link is not valid! - {error}")

                return

            video_title = self.__ReplaceTitle(video_info['title'])

            path_to_file = os.path.join(self.Settings.GetDownloadDir() + folder_name, f"Video\\{video_title}.mp4")

            if os.path.exists(path_to_file):
                if self.Settings.GetOverwrite() is True:
                    os.remove(path_to_file)
                else:
                    raise Exception("The video already exists in the download folder ( overwrite option is off )")

            video_download_options = {
                'outtmpl': self.Settings.GetDownloadDir() + "Video/" + folder_name + f'{video_title}.%(ext)s',
                'quiet': self.Settings.GetQuietDownload(),
                'merge_output_format': 'mp4',
                'format': f'bestvideo[height<={self.Settings.GetMaxRes()}][vbr>={best_format['vbr']-1}]+bestaudio[ext=m4a]/best[height<={self.Settings.GetMaxRes()}]',
                'nooverwrites': self.Settings.GetOverwrite(),
                # 'extract_flat': True,
                'updatetime': True,
                # 'progress_hooks': [self.__progress_hook],
                # 'concurrent-fragments': 4,
                'no_fragment': True,
                'ratelimit': None,
                # 'write_thumbnail': True,
            }

            print(f"Now downloading video for - {video_title}")

            yt.YoutubeDL(video_download_options).download([video_url])

            print(f"Video downloaded")

            os.utime(self.Settings.GetDownloadDir() + "Video/" + folder_name + f'{video_title}.mp4')

        except Exception as error:
            raise Exception(f"Error while downloading video - {error}")


    def __DownloadYtAudio(self, video_url, folder_name=""):  # Falta , audio_bitrate_option

        if '&list=' in video_url and 'playlist?' not in video_url:
            video_url = video_url[:-(len(video_url) - video_url.find('list'))]

        if folder_name != "":
            folder_name = self.__ReplaceTitle(folder_name)
            folder_name = "/" + folder_name + "/"

        try:

            try:

                audio_info = yt.YoutubeDL(self.__info_options).extract_info(video_url, download=False)

                # for f in audio_info['formats']:
                #     if  f['abr'] is not None:
                #         print(f)

                best_format = max(
                    (f for f in audio_info['formats'] if
                     'abr' in f and f['abr'] is not None),
                    key=lambda x: x.get('abr', 0)
                )

                # print(best_format['abr'])

            except Exception as error:
                print(f"Link is not valid! - {error}")

                return

            audio_title = self.__ReplaceTitle(audio_info['title'])

            path_to_file = os.path.join(self.Settings.GetDownloadDir() + folder_name, f"Audio\\{audio_title}.mp3")

            if os.path.exists(path_to_file):
                if self.Settings.GetOverwrite() is True:
                    os.remove(path_to_file)
                else:
                    raise Exception("The audio already exists in the download folder ( overwrite option is off )")

            print(f"Now downloading audio for - {audio_title}")

            if self.Settings.GetAlbumCover():
                audio_title += '_temp'

            audio_download_options = {
                'outtmpl': self.Settings.GetDownloadDir() + "Audio/" + folder_name + f'{audio_title}.%(ext)s',
                'quiet': self.Settings.GetQuietDownload(),
                'format': f'bestaudio/best[abr>={best_format['abr']-1}]',
                'nooverwrites': self.Settings.GetOverwrite(),
                # 'extract_flat': True,
                'extractaudio': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    # 'preferredquality': audio_bitrate_option,
                }],
                'updatetime': True,
                'progress_hooks': [self.__progress_hook],
                # 'concurrent-fragments': 4,
                'no_fragment': True,
                'ratelimit': None,
            }

            yt.YoutubeDL(audio_download_options).download([video_url])

            print(f"Audio downloaded")

            os.utime(self.Settings.GetDownloadDir() + "Audio/" + folder_name + f'{audio_title}.mp3')

            if self.Settings.GetAlbumCover():

                thumbnail = None

                for item in audio_info['thumbnails']:
                    if 'resolution' in item and 'jpg' in item['url'] and '480x360' in item['resolution']:
                        thumbnail = item
                        break

                if thumbnail is not None:

                    url = thumbnail['url']

                    thumbnail = urllib.request.urlretrieve(url, f"{self.Settings.GetDownloadDir()}thumbnail_temp.jpg")

                    subprocess.call(
                        ['ffmpeg', '-y', '-i',
                         f"{self.Settings.GetDownloadDir()+ "Audio/" + folder_name + audio_title}.mp3", '-i',
                         thumbnail[0], '-map', '0:a', '-map', '1', '-c',
                         'copy',
                         '-id3v2_version', '3', '-metadata:s:v', 'title="Album cover"', '-metadata:s:v',
                         'comment="Cover (front)"',
                         f"{self.Settings.GetDownloadDir() + "Audio/" + folder_name + audio_title[:-5]}.mp3"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

                    os.remove(f"{self.Settings.GetDownloadDir() + "Audio/" + folder_name + audio_title[:-5]}_temp.mp3")
                    os.remove(thumbnail[0])

                else:
                    print("Couldn't find a '480x360' thumbnail in the video ! ( so no album cover broski )")

        except Exception as error:
            raise Exception(f"Error while downloading audio - {error}")


    def __DownloadYtPlaylist(self, playlist_url):

        try:

            playlist_info = yt.YoutubeDL(self.__info_options).extract_info(playlist_url, download=False)

        except Exception as error:
            print(f"Link is not valid! - {error}")

            return

        print(f"Now downloading from playlist - {playlist_info['title']}")

        playlist_length = len(playlist_info['entries'])

        if self.Settings.GetVideoAudio() is True:

            if self.Settings.GetReverse() is True:

                for item_num in range(playlist_length - 1, 0, -1):
                    item = playlist_info['entries'][item_num]

                    try:
                        self.__DownloadYtVideo(item['url'], playlist_info['title'])

                    except Exception as error:
                        print(f"Error while downloading playlist item - {error}")

            else:

                for item in playlist_info['entries']:

                    try:
                        self.__DownloadYtVideo(item['url'], playlist_info['title'])

                    except Exception as error:
                        print(f"Error while downloading playlist item - {error}")

        else:

            if self.Settings.GetReverse() is True:

                for item_num in range(playlist_length - 1, 0, -1):
                    item = playlist_info['entries'][item_num]

                    try:
                        self.__DownloadYtAudio(item['url'], playlist_info['title'])

                    except Exception as error:
                        print(f"Error while downloading playlist item - {error}")

            else:

                for item in playlist_info['entries']:

                    try:
                        self.__DownloadYtAudio(item['url'], playlist_info['title'])

                    except Exception as error:
                        print(f"Error while downloading playlist item - {error}")

        print("Done downloading!")

    def DownloadFromYoutube(self, url):

        try:

            if 'playlist?list=' in url:
                print("The link is a playlist")

                self.__DownloadYtPlaylist(url)
            elif 'watch?v=' in url or '/shorts/' in url:
                print("The link is a video")

                if self.Settings.GetVideoAudio() is True:
                    self.__DownloadYtVideo(url)

                else:
                    self.__DownloadYtAudio(url)
            else:
                print("Link is not valid!")
        except Exception as error:
            print(error)
