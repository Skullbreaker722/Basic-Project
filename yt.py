import yt_dlp

# def yt(url):
#     ydl_opts = {
#         'format': 'bestvideo[height<=1080]+bestaudio/best',  # Download best video + best audio
#         'noplaylists': True,
#         'merge_output_format': 'mp4',  # Ensures the final file is MP4
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# if __name__ == '__main__':
#     video_url = input('Enter video URL: ')
#     yt(video_url)

def download_yt_video(url):
    ydl_opts = {
        #'format': 'bestvideo[height<=1080]',
        'format' : 'best[ext=mp4]',
        'noplaylist': True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("Enter the YouTube Video URL: ")
    download_yt_video(video_url)
