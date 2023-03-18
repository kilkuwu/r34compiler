import os
import pathlib
from time import perf_counter
import requests
import urllib.request
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.resize import resize

last_percent_reported = None

def download_progress_hook(count, blockSize, totalSize):
  global last_percent_reported
  percent = int(count * blockSize * 100 / totalSize)

  if last_percent_reported != percent and percent%5==0:
    perfive = int(percent/5)
    
    print(perfive*"█"+' '*(20-perfive), str(percent)+'%', end='\r')
    last_percent_reported = percent

def f_api_args(bef_url: str, **kwargs):
    res = bef_url
    for key, val in kwargs.items():
        res += f"{key}={val}&"
    return res.replace(' ', '%20')

def download_r34_videos_by_tags(tags, limit):
    yes = tags.find('video')
    if(yes == -1): 
        tags += ' video'
    url = f_api_args(
        "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&",
        limit=limit,
        json=1,
        tags=tags
    )
    response = requests.get(url).json()
    file_directory = os.path.join(os.path.curdir, 'downloaded')
    pathlib.Path(file_directory).mkdir(parents=True, exist_ok=True)
    filenames = []
    for i in range(len(response)):
        data = response[i]
        file_url = data['file_url']
        file_path = os.path.join(file_directory, f'{i}{os.path.splitext(data["image"])[1]}')
        print(f"Started downloading video {i+1}/{len(response)}")
        urllib.request.urlretrieve(file_url, file_path, download_progress_hook)
        print()
        filenames.append(file_path)
    return filenames

def concatenate_videoclips_same_res(width, height, filenames):
    videos = []
    for filename in filenames:
        video = VideoFileClip(filename)
        w, h = video.size
        if(w > h):
            video = video.fx(rotate, -90)
            w, h = h, w
        if(h == height or w == width):
            videos.append(video)
            continue
        if(w*height >= h*width):
            video = video.fx(resize, width=width)
        else:
            video = video.fx(resize, height=height)
        videos.append(video)
    return videos

def main():
    tags = input("Tags: ")
    times = int(input("Limit: "))
    filenames = download_r34_videos_by_tags(tags, times)
    videos = concatenate_videoclips_same_res(1080, 1920, filenames)
    final_videos = concatenate_videoclips(videos)
    timer = perf_counter()
    final_videos.write_videofile('merged.mp4')
    timer_end = perf_counter()
    time = timer_end - timer
    print('It took', time, 'seconds to render the video')

main()
