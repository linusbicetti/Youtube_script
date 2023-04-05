from pytube import YouTube
from tqdm import tqdm
import PySimpleGUI as sg

sg.theme('LightGrey1')

layout = [
    [sg.Text('Enter YouTube URL: '), sg.InputText(key='url')],
    [sg.Text('Choose download folder: '), sg.InputText(key='folder'), sg.FolderBrowse()],
    [sg.Button('Download'), sg.Button('Cancel')],
    [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar', visible=False)]

]

window = sg.Window('YouTube Downloader', layout)

def download_video(url, folder,progress_bar):
    youtube = YouTube(url)

    # Select the highest quality video
    video = youtube.streams.get_highest_resolution()

    # Get the file size in bytes
    file_size = video.filesize

    # Use tqdm to show progress bar
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=video.title) as pbar:
        video.download(output_path=folder)
        pbar.update(file_size)
    sg.popup(f'Download completed successfully!\nFile saved to:\n{folder}/{video.title}')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Download':
        url = values['url']
        folder = values['folder']
        progress_bar = window['progressbar']
        progress_bar.Update(visible=True)
        download_video(url, folder, progress_bar)

window.close()
