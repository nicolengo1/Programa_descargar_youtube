import os
import subprocess
import yt_dlp as yt
import sys
import urllib.request
# import tqdm

from Settings_functions.settings import SettingsClass
from Console_functions.console import ConsoleClass


# pbar = None
# total_size = 0

# def __progress_hook(self, d):
    #     global pbar, total_size
    #
    #     if d['status'] == 'downloading':
    #         if not pbar:
    #             total_size = d.get('total_bytes') or d.get('total_bytes_estimate')
    #             if total_size:
    #                 pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')
    #             else:
    #                 self.Console.PrintInConsole("Couldn't get file size.")
    #
    #         if pbar:
    #             pbar.update(d['downloaded_bytes'] - pbar.n)
    #
    #     elif d['status'] == 'finished':
    #         if pbar:
    #             pbar.close()

# playlist_url = "https://www.youtube.com/playlist?list=PLbxgqNDpPEDnRIK1ByzKuO_klbRmGWOOA"


class DownloaderClass:

    def __init__(self, console):

        self.__ffmpeg_path = None

        self.Console = ConsoleClass(console)

        self.Settings = SettingsClass()

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

    # Download from a video
    def DownloadFromYoutube(self, url):

        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        self.__ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")

        yt.postprocessor.FFmpegPostProcessor._ffmpeg_location.set(self.__ffmpeg_path)

        try:
            if 'playlist?list=' in url:
                self.Console.ConsoleNormal("El enlace es una lista")

                self.Settings.SetLastPlaylist(url)

                self.__DownloadYtPlaylist(url)


            elif '/watch?v=' in url or '/shorts/' in url or '/youtu.be/' in url:
                self.Console.ConsoleNormal("El enlace es un video")

                if '&list=' in url:
                    url = url[:-(len(url) - url.find('list'))]

                if self.Settings.GetVideoAudio() is True:
                    self.__DownloadYtVideo(url)

                else:
                    self.__DownloadYtAudio(url)

            else:
                self.Console.ConsoleError("Enlace no valido! \n")

        except Exception as error:
            self.Console.ConsoleError(f"Fatal error - {error}")


    # Download Playlist
    def __DownloadYtPlaylist(self, playlist_url):

        try:

            playlist_info = yt.YoutubeDL(self.__info_options).extract_info(playlist_url, download=False)

        except Exception as error:
            raise f"Enlace no valido! - {error} \n\n {playlist_url} \n"

        playlist_name = self.__ReplaceTitle(playlist_info['title'])

        self.Console.ConsoleInfo(f"Descargando lista - {playlist_name}")

        playlist_name = playlist_name + "/"


        if self.Settings.GetReverse() is True:
            playlist_info['entries'].reverse()


        if self.Settings.GetVideoAudio() is True: # Video

            for item in playlist_info['entries']:

                try:
                    self.__DownloadYtVideo(item['url'], playlist_name)

                except Exception as error:
                    self.Console.ConsoleError(f"Error descargando en lista - {error} \n\n {playlist_url} \n")

        else: # Audio

            for item in playlist_info['entries']:

                try:
                    self.__DownloadYtAudio(item['url'], playlist_name)

                except Exception as error:
                    self.Console.ConsoleError(f"Error descargando en lista - {error} \n\n {playlist_url} \n")


        self.Console.ConsoleOK("Descarga finalizada! \n")


    #Download Video
    def __DownloadYtVideo(self, video_url, folder_name=""):

        try:
            ok = 0

            for i in range(1,4) :

                if ok == 0:

                    try:

                        video_info = yt.YoutubeDL(self.__info_options).extract_info(video_url, download=False)

                        video_title = self.__ReplaceTitle(video_info['title'])

                        self.Console.ConsoleInfo(f"Ahora descargando - {video_title}")

                        path_to_file = self.Settings.GetDownloadDir() + "Audio/" + folder_name + f'{video_title}.mp4'

                        if os.path.exists(path_to_file):
                            if self.Settings.GetOverwrite() is True:
                                os.remove(path_to_file)
                            else:
                                ok = 1
                                i = 5
                                self.Console.ConsoleWarning(
                                    "El audio ya existe en la carpeta ( la opcion de sobreescribir no esta activada )\n")

                                break

                        formats = []

                        for f in video_info['formats']:
                            if 'height' in f and f['height'] is not None and f[
                                'height'] <= self.Settings.GetMaxRes() and f['vbr'] is not None:
                                formats.append(f)

                        formats.sort(
                            key=lambda x: x.get('height', 0)
                        )

                        best_format = max(
                            formats,
                            key=lambda x: x.get('vbr', 0)
                        )


                        video_download_options = {
                            'outtmpl': self.Settings.GetDownloadDir() + "Video/" + folder_name + f'{video_title}.%(ext)s',
                            'quiet': self.Settings.GetQuietDownload(),
                            'merge_output_format': 'mp4',
                            'format': f'bestvideo[height<={self.Settings.GetMaxRes()}][vbr>={best_format['vbr']-1}]+bestaudio[ext=m4a]/best[height<={self.Settings.GetMaxRes()}]',
                            'nooverwrites': self.Settings.GetOverwrite(),
                            # 'extract_flat': True,
                            # 'progress_hooks': [self.__progress_hook],
                            # 'concurrent-fragments': 4,
                            'no_fragment': True,
                            'ratelimit': None,
                        }


                        yt.YoutubeDL(video_download_options).download(video_url)

                        os.utime(self.Settings.GetDownloadDir() + "Video/" + folder_name + f'{video_title}.mp4')

                        self.Console.ConsoleOK("Video descargado \n")

                        ok = 1

                    except Exception as error:
                        if i == 3:
                            raise f"Error downloading video \n\n {video_url} \n"

                        self.Console.ConsoleWarning(f"Retrying download - {i + 1}, {error}")

        except Exception as error:
            raise Exception(f"Error descargando video - {error}")



    #Download Audio
    def __DownloadYtAudio(self, video_url, folder_name=""):

        try:
            ok = 0

            for i in range(1, 4):

                if ok == 0:

                    try:

                        audio_info = yt.YoutubeDL(self.__info_options).extract_info(video_url, download=False)

                        audio_title = self.__ReplaceTitle(audio_info['title'])

                        self.Console.ConsoleInfo(f"Ahora descargando - {audio_title}")

                        path_to_file = self.Settings.GetDownloadDir() + "Audio/" + folder_name + f'{audio_title}.mp3'

                        if os.path.exists(path_to_file):
                            if self.Settings.GetOverwrite() is True:
                                os.remove(path_to_file)

                            else:
                                ok = 1
                                i = 5
                                self.Console.ConsoleWarning(
                                    "El audio ya existe en la carpeta ( la opcion de sobreescribir no esta activada )\n")

                                break

                        best_format = max(
                            (f for f in audio_info['formats'] if
                             'abr' in f and f['abr'] is not None),
                            key=lambda x: x.get('abr', 0)
                        )



                        if self.Settings.GetAlbumCover():
                            audio_title += '_temp'

                        audio_download_options = {
                            'outtmpl': self.Settings.GetDownloadDir() + "Audio/" + folder_name + f'{audio_title}.%(ext)s',
                            'quiet': self.Settings.GetQuietDownload(),
                            'format': f'bestaudio/best[abr>={best_format['abr'] - 1}]',
                            'nooverwrites': self.Settings.GetOverwrite(),
                            # 'extract_flat': True,
                            'extractaudio': True,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                # 'preferredquality': audio_bitrate_option,
                            }],
                            'updatetime': True,
                            # 'progress_hooks': [self.__progress_hook],
                            # 'concurrent-fragments': 4,
                            'no_fragment': True,
                            'ratelimit': None,
                        }


                        yt.YoutubeDL(audio_download_options).download(video_url)

                        if self.Settings.GetAlbumCover():
                            self.__DownloadThumbnail(audio_info, folder_name, audio_title)
                            # pass

                        self.Console.ConsoleOK("Audio descargado \n")

                        ok = 1

                    except Exception as error:
                        if i == 3:
                            raise f"Error downloading audio \n\n {video_url} \n"

                        self.Console.ConsoleWarning(f"Retrying download - {i+1}, {error}")

        except Exception as error:
            raise Exception(f"Error descargando audio - {error}")



    def __DownloadThumbnail(self, audio_info, folder_name, audio_title):

        thumbnail = None

        for item in audio_info['thumbnails'] :
            if thumbnail is None:
                if 'resolution' in item and 'jpg' in item['url'] and '480x360' in item['resolution']:
                    thumbnail = item

        if thumbnail is not None:
            url = thumbnail['url']

            thumbnail = urllib.request.urlretrieve(url, f"{self.Settings.GetDownloadDir()}thumbnail_temp.jpg")

            subprocess.call(
                [f'{self.__ffmpeg_path}', '-y', '-i',
                 f"{self.Settings.GetDownloadDir() + "Audio/" + folder_name + audio_title}.mp3", '-i',
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
            self.Console.ConsoleWarning("Couldn't find a Thumbnail! \n")

