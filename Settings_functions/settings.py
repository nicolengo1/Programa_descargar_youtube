import os
import sys


class SettingsClass:
    def __init__(self, download_directory_option='/', max_res_option=1080, overwrite_option=False,
                 quiet_download_option=True, quiet_info_option=True, album_cover_option=False, reverse_option=False,
                 video_audio_option=True):


        if download_directory_option is None or download_directory_option in '/\\ ' or not os.path.exists(
                download_directory_option):

            if getattr(sys, 'frozen', False):
                download_directory_option = os.path.dirname(sys.executable)

            elif __file__:
                download_directory_option = os.path.dirname(__file__)
                download_directory_option = download_directory_option[:-19]

            download_directory_option += '/Downloads/'

        if not download_directory_option.endswith('/') or not download_directory_option.endswith('\\'):
            download_directory_option += '\\'

        if video_audio_option == "video":
            video_audio_option = True
        elif video_audio_option == "audio":
            video_audio_option = False

        self.__download_dir = download_directory_option
        self.__max_res = max_res_option
        self.__overwrite = overwrite_option
        self.__quiet_download = quiet_download_option
        self.__quiet_info = quiet_info_option
        self.__album_cover = album_cover_option
        self.__reverse = reverse_option
        self.__video_audio = video_audio_option

    def SetDownloadDir(self, download_directory_option):

        if download_directory_option is not None:

            if download_directory_option is None or download_directory_option in '/\\ ' or not os.path.exists(
                    download_directory_option):

                if getattr(sys, 'frozen', False):
                    download_directory_option = os.path.dirname(sys.executable)

                elif __file__:
                    download_directory_option = os.path.dirname(__file__)
                    download_directory_option = download_directory_option[:-19]

                download_directory_option += '/Downloads/'

            if not download_directory_option.endswith('/'):
                download_directory_option += '/'

            self.__download_dir = download_directory_option

    def GetDownloadDir(self):
        return self.__download_dir

    def SetMaxRes(self, max_res_option):
        self.__max_res = max_res_option
        
    def GetMaxRes(self):
        return self.__max_res

    def SetOverwrite(self, overwrite_option):
        self.__overwrite = overwrite_option
        
    def GetOverwrite(self):
        return self.__overwrite

    def SetQuietDownload(self, quiet_download_option):
        self.__quiet_download = quiet_download_option

    def GetQuietDownload(self):
        return self.__quiet_download

    def SetQuietInfo(self, quiet_info_option):
        self.__quiet_info = quiet_info_option
        
    def GetQuietInfo(self):
        return self.__quiet_info

    def SetAlbumCover(self, album_cover_option):
        self.__album_cover = album_cover_option
        
    def GetAlbumCover(self):
        return self.__album_cover

    def SetReverse(self, reverse_option):
        self.__reverse = reverse_option
        
    def GetReverse(self):
        return self.__reverse

    def SetVideoAudio(self, video_audio_option):
        self.__video_audio = video_audio_option
        
    def GetVideoAudio(self):
        return self.__video_audio