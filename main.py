import os
import pathlib
import requests
import urllib.request
from utils import FileTag, format_api_args

R34_API_URL = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&"
last_percent_reported = None


def download_progress_hook(count, blockSize, totalSize):
    global last_percent_reported
    percent = int(count * blockSize * 100 / totalSize)

    if last_percent_reported != percent and percent % 5 == 0:
        perfive = int(percent / 5)
        print(perfive * "█" + " " * (20 - perfive),
              str(percent) + "%", end="\r")
        last_percent_reported = percent


def download_r34_videos_by_tags(tags: str, limit: int):
    if tags.find("video") == -1:
        tags += " video"

    url = format_api_args(
        R34_API_URL,
        limit=limit,
        json=1,
        tags=tags,
    )

    response = requests.get(url).json()
    response = response[51:]
    file_directory = os.path.join(os.path.curdir, "downloaded")
    pathlib.Path(file_directory).mkdir(parents=True, exist_ok=True)
    for i in range(len(response)):
        while True: 
            try:
                data = response[i]
                file_url = data["file_url"]
                file_path = os.path.join(
                    file_directory, f'{i:03d}{os.path.splitext(data["image"])[1]}'
                )
                print(f"Started downloading video {i+1}/{len(response)}")
                urllib.request.urlretrieve(file_url, file_path, download_progress_hook)
                file_with_tag = FileTag(file_path)
                file_with_tag.clear()
                file_with_tag.add_tags(*str(data['tags']).split())
                file_with_tag.save()
                print()
                break
            except:
                continue
        


def main():
    tags = input("Tags: ")
    times = int(input("Limit: "))
    download_r34_videos_by_tags(tags, times)


# lazyprocrastinator video sound -atelier_(series)  -2d -absurdres -horns -horn -the_ring -extremely_large_filesize  -code_vein -werewolf -2boys -shiva_(final_fantasy)  -elezen score:>=100 -dark-skinned_male -2d_animation -yuffie_kisaragi  -tatsumaki -ranni_the_witch  -iroha -hoodie -dark-skinned_female -madam_m -christmas -scarlet_(ffvii) -lulu_(final_fantasy) height:<=2160 width:>=1280 width:<=1920
main()
