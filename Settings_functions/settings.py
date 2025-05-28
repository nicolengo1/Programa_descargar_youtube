import os
import sys
import json


class SettingsClass:
    def __init__(self):

        config = self.LoadConfig()

        try:
            download_directory_option = config["download_directory_option"]
            max_res_option = int(config["max_res_option"])
            overwrite_option = config["overwrite_option"]
            quiet_download_option = config["quiet_download_option"]
            quiet_info_option = config["quiet_info_option"]
            album_cover_option = config["album_cover_option"]
            reverse_option = config["reverse_option"]
            video_audio_option = config["video_audio_option"]
            last_playlist = config["last_playlist"]

        except Exception:
            config = {
                "download_directory_option": self.__download_dir,
                "max_res_option": 1080,
                "overwrite_option": False,
                "quiet_download_option": True,
                "quiet_info_option": True,
                "album_cover_option": False,
                "reverse_option": False,
                "video_audio_option": True,
                "last_playlist": ""
            }

            download_directory_option = config["download_directory_option"]
            max_res_option = int(config["max_res_option"])
            overwrite_option = config["overwrite_option"]
            quiet_download_option = config["quiet_download_option"]
            quiet_info_option = config["quiet_info_option"]
            album_cover_option = config["album_cover_option"]
            reverse_option = config["reverse_option"]
            video_audio_option = config["video_audio_option"]
            last_playlist = config["last_playlist"]


        self.__download_dir = None
        self.SetDownloadDir(download_directory_option)

        self.__max_res = max_res_option
        self.__overwrite = overwrite_option
        self.__quiet_download = quiet_download_option
        self.__quiet_info = quiet_info_option
        self.__album_cover = album_cover_option
        self.__reverse = reverse_option
        self.__video_audio = video_audio_option

        self.__last_playlist = last_playlist

        self.SaveConfig()


    def LoadConfig(self, route="config.json"):
        if os.path.exists(route):
            with open(route, "r") as f:
                return json.load(f)
        else:
            self.SetDownloadDir(None)

            return {
                "download_directory_option": self.__download_dir,
                "max_res_option": 1080,
                "overwrite_option": False,
                "quiet_download_option": True,
                "quiet_info_option": True,
                "album_cover_option": False,
                "reverse_option": False,
                "video_audio_option": True,
                "last_playlist": ""
            }


    def SaveConfig(self, route="config.json"):

        config = {"download_directory_option": self.__download_dir,
                "max_res_option": self.__max_res,
                "overwrite_option": self.__overwrite,
                "quiet_download_option": self.__quiet_download,
                "quiet_info_option":self.__quiet_info,
                "album_cover_option": self.__album_cover,
                "reverse_option": self.__reverse,
                "video_audio_option": self.__video_audio,
                "last_playlist": self.__last_playlist}

        with open(route, "w") as f:
            json.dump(config, f, indent=4)

    def SetDownloadDir(self, download_directory_option):

        if download_directory_option is None or download_directory_option in '/\\ ' or not os.path.exists(
                download_directory_option):

            if getattr(sys, 'frozen', False):
                download_directory_option = os.path.dirname(sys.executable)

            elif __file__:
                download_directory_option = os.path.dirname(__file__)
                download_directory_option = download_directory_option[:-19]

        if not download_directory_option.endswith('/') and not download_directory_option.endswith('\\'):
            download_directory_option += '\\'


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

    def SetLastPlaylist(self, playlist):
        self.__last_playlist = playlist

        self.SaveConfig()

    def GetLastPlaylist(self):
        return self.__last_playlist


