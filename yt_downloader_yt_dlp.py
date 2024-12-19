from Download_functions.download import DownloaderClass

YtDownloader = DownloaderClass(reverse_option=False, video_audio_option='audio', overwrite_option=True, download_directory_option="D:\\audio", album_cover_option=True, quiet_info_option=True)

while True:
    link = input("link -> ")

    YtDownloader.DownloadFromYoutube(link)
