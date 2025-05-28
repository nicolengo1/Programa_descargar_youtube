import tkinter as tk
from tkinter import scrolledtext, ttk
# from PIL import Image, ImageTk

import threading

from Console_functions.console import ConsoleClass
from Download_functions.download import DownloaderClass


def OptionWindow(root, YTDownloader):

    def SaveOptions():
        YTDownloader.Settings.SetDownloadDir(dir_entry.get())
        YTDownloader.Settings.SetMaxRes(int(res_combo.get()))
        YTDownloader.Settings.SetOverwrite(overwrite_var.get())
        YTDownloader.Settings.SetQuietDownload(quiet_download_var.get())
        YTDownloader.Settings.SetQuietInfo(quiet_info_var.get())
        YTDownloader.Settings.SetAlbumCover(album_cover_var.get())
        YTDownloader.Settings.SetReverse(reverse_var.get())
        YTDownloader.Settings.SetVideoAudio(video_audio_var.get())

        YTDownloader.Settings.SaveConfig()

    def SaveAndClose():
        SaveOptions()
        options.destroy()


    # Crear ventana de configuración
    options = tk.Toplevel(root)
    options.title("Configuraciones")
    options.geometry("500x400")
    options.maxsize(600, 400)
    options.minsize(600, 400)

    options.protocol("WM_DELETE_WINDOW", SaveAndClose)

    # Hace que la ventana se mantenga encima
    options.transient(root)

    # Bloquea interacción con la principal (opcional)
    options.grab_set()

    # Botón volver (simplemente cierra esta ventana)
    volver_btn = tk.Button(options, text="←", command=SaveAndClose)
    volver_btn.place(x=10, y=10)

    # Etiqueta: Directorio de descarga
    tk.Label(options, text="Directorio de descarga:").place(x=50, y=60)
    dir_entry = tk.Entry(options, width=60)
    dir_entry.insert(0, YTDownloader.Settings.GetDownloadDir())
    dir_entry.place(x=200, y=60)

    # Resolución máxima
    tk.Label(options, text="Resolución máxima:").place(x=50, y=100)
    res_combo = ttk.Combobox(options, values=["144", "240", "360", "480", "720", "1080", "1440", "2160"],
                             state="readonly", width=10)
    res_combo.set(str(YTDownloader.Settings.GetMaxRes()))
    res_combo.place(x=200, y=100)


    # Función para crear checkboxes
    def create_check(label, var, y, text1, text2):
        tk.Label(options, text=label).place(x=50, y=y)
        yes = tk.Checkbutton(options, variable=var, onvalue=True, offvalue=False, text=text1)
        no = tk.Checkbutton(options, variable=var, onvalue=False, offvalue=True, text=text2)
        yes.place(x=200, y=y)
        no.place(x=260, y=y)


    # BooleanVars
    overwrite_var = tk.BooleanVar(value=YTDownloader.Settings.GetOverwrite())
    quiet_download_var = tk.BooleanVar(value=YTDownloader.Settings.GetQuietDownload())
    quiet_info_var = tk.BooleanVar(value=YTDownloader.Settings.GetQuietInfo())
    album_cover_var = tk.BooleanVar(value=YTDownloader.Settings.GetAlbumCover())
    reverse_var = tk.BooleanVar(value=YTDownloader.Settings.GetReverse())
    video_audio_var = tk.BooleanVar(value=YTDownloader.Settings.GetVideoAudio())

    # Crear checkboxes
    create_check("Sobrescribir archivos:", overwrite_var, 140, "Sí", "No")
    create_check("Descarga silenciosa:", quiet_download_var, 170, "Sí", "No")
    create_check("Info silenciosa:", quiet_info_var, 200, "Sí", "No")
    create_check("Incluir portada álbum:", album_cover_var, 230, "Sí", "No")
    create_check("Orden inverso:", reverse_var, 260, "Sí", "No")

    create_check("¿Video o solo audio?:", video_audio_var, 290, "Video", "Audio")

    # Botón guardar cambios
    save_btn = tk.Button(options, text="Guardar", command=SaveAndClose, bg="lightgreen")
    save_btn.place(relx=0.5, y=340, anchor="center")



def MainWindow():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Yt Downloader")
    root.geometry("600x400")
    root.minsize(400, 400)

    def __OnSubmit(event=None):
        link = link_entry.get()

        message = f"Enlace insertado: {link}"
        Console.ConsoleInfo(message)
        link_entry.delete(0, tk.END)

        # YTDownloader.DownloadFromYoutube(link)

        hilo = threading.Thread(target=lambda: YTDownloader.DownloadFromYoutube(link), daemon=True) # Por ahora sirve
        hilo.start()



    def __OnSubmitLastPlaylist(event=None):
        link_entry.delete(0, len(link_entry.get()))
        link_entry.insert(0, f"{YTDownloader.Settings.GetLastPlaylist()}")



    # Consola (Text + Scrollbar)
    console_frame = tk.Frame(root, bd=1, relief="solid")
    console_frame.pack(side=tk.BOTTOM, fill=tk.X)

    console = scrolledtext.ScrolledText(console_frame, height=12, wrap=tk.WORD, borderwidth=0, fg="white", bg="black")
    console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    console.configure(state=tk.DISABLED)

    Console = ConsoleClass(console)

    YTDownloader = DownloaderClass(console)


    # Botón de opciones (esquina superior izquierda)
    options_btn = tk.Button(root, text="⚙", command=lambda: OptionWindow(root, YTDownloader))
    options_btn.place(x=10, y=10)

    # Botón para reiniciar tamaño (esquina superior derecha)
    reset_btn = tk.Button(root, text="🔄", command=lambda: root.geometry("600x400"))
    reset_btn.place(relx=1.0, x=-10, y=10, anchor="ne")



    thumbnail_label = tk.Label(root, width=20, height=5)
    thumbnail_label.place(relx=0.5, rely=0.45, y=-100, anchor="center")


    # Entrada de texto para el link
    link_label = tk.Label(root, text="Introduce el enlace")
    link_label.place(relx=0.5, rely=0.45, anchor="s", y=-8)

    link_entry = tk.Entry(root, borderwidth=2, relief="solid")
    link_entry.place(relx=0.5, rely=0.45, anchor="center", width=300, height=25)
    link_entry.bind("<Return>", __OnSubmit)

    # Botón junto al campo de texto
    submit_btn = tk.Button(root, text="→", command=__OnSubmit, bg="lightblue")
    submit_btn.place(relx=0.5, rely=0.45, anchor="w", x=150, width=30, height=25)

    last_playlist_btn = tk.Button(root, text="Ultima lista",command=__OnSubmitLastPlaylist, borderwidth=2, relief="solid")
    last_playlist_btn.place(relx=0.5, rely=0.45, anchor="w", x=-230, height=25)



    # Iniciar bucle principal
    root.mainloop()