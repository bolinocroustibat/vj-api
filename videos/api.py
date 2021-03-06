import json
import random
from typing import Optional

import requests
from django.http import Http404
from ninja import NinjaAPI

from videos.models import Theme, Video
from vj_api.settings import logger, YOUTUBE_API_KEY

api = NinjaAPI()

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_DOCS_URL = "https://www.googleapis.com/youtube/v3/videos"
DICTIONNARIES: dict = {
	"en": "vj_api/dictionaries/dict_EN.txt",
	"fr": "vj_api/dictionaries/dictionary_FR.txt",
	"jp": "vj_api/dictionaries/44492-japanese-words-latin-lines-removed.txt",
}


@api.get("/{theme_name}")
def get_video_from_theme(request, theme_name: str):
	theme, created = Theme.objects.get_or_create(name=theme_name)
	videos: Optional[list[Video]] = get_videos_from_youtube(theme=theme)
	if videos and len(videos):
		populate_db(videos)
		update_video_duration_from_youtube(videos=videos)
		video = random.choice(videos)
	else:
		try:
			videos = Video.objects.all()
			video = random.choice(videos)
		except:
			raise Http404
	return {
		"theme": theme.name,
		"youtubeId": video.youtube_id,
		"videoDuration": video.duration,
		"bestStart": video.best_start,
	}


@api.get("/")
def get_video(request):
	videos: Optional[list[Video]] = get_videos_from_youtube()
	if videos and len(videos):
		populate_db(videos)
		update_video_duration_from_youtube(videos=videos)
		video = random.choice(videos)
	else:
		try:
			videos = Video.objects.all()
			video = random.choice(videos)
		except:
			raise Http404
	return {
		"theme": None,
		"youtubeId": video.youtube_id,
		"videoDuration": video.duration,
		"bestStart": video.best_start,
	}


def update_video_duration_from_youtube(videos: list[Video]) -> None:
	youtube_ids: list = [v.youtube_id for v in videos if not v.duration][:49]
	response_content = requests.get(
		YOUTUBE_DOCS_URL,
		params={
			"key": YOUTUBE_API_KEY,
			"part": "contentDetails",
			"type": "video",
			"id": ",".join(youtube_ids),
		},
	).content

	content: dict = json.loads(response_content)
	if content.get("error", None):
		if content["error"].get("code", None) == 403:
			logger.error(
				'Forbidden by YouTube: "{}"'.format(content["error"]["message"])
			)
		else:
			logger.error('Error: "{}"'.format(content["error"]))
	else:
		for v in content["items"]:
			try:
				duration_yt: str = v["contentDetails"]["duration"][2:]
				hours = 0
				if "H" in duration_yt:
					hours = int(duration_yt.split("H")[0])
					duration_yt = duration_yt.split("H")[1]
				minutes = 0
				if "M" in duration_yt:
					minutes = int(duration_yt.split("M")[0])
					duration_yt = duration_yt.split("M")[1]
				seconds = 0
				if "S" in duration_yt:
					seconds = int(duration_yt.split("S")[0])
				duration: int = hours * 3600 + minutes * 60 + seconds
				video = Video.objects.get(youtube_id=v["id"])
				video.duration = duration
				video.save()
			except Exception as e:
				logger.error(str(e))


def get_videos_from_youtube(theme: Optional[Theme] = None) -> Optional[list[Video]]:
	search_string: str = get_random_word()
	if theme:
		search_string = f"{theme.name} {search_string}"
	response_content = requests.get(
		YOUTUBE_SEARCH_URL,
		params={
			"key": YOUTUBE_API_KEY,
			"part": "snippet",
			"type": "video",
			"q": search_string,
		},
	).content
	content: dict = json.loads(response_content)
	if content.get("error", None):
		if content["error"].get("code", None) == 403:
			logger.error(
				'Forbidden by YouTube: "{}"'.format(content["error"]["message"])
			)
		else:
			logger.error('Error: "{}"'.format(content["error"]))
	else:
		videos: list = []
		for v in content["items"]:
			try:
				if theme:
					video = Video(
						youtube_id=v["id"]["videoId"],
						title=v["snippet"]["title"],
						thumbnail=v["snippet"]["thumbnails"]["high"]["url"],
						theme=theme,
						search_string=search_string,
					)
				else:
					video = Video(
						youtube_id=v["id"]["videoId"],
						title=v["snippet"]["title"],
						thumbnail=v["snippet"]["thumbnails"]["high"]["url"],
						search_string=search_string,
					)
				videos.append(video)
				logger.info(f'Geo a new video ID "{video.title}" from YouTube')
			except Exception as e:
				logger.error(str(e))
		return videos


def populate_db(videos: list[Video]) -> None:
	for v in videos:
		try:
			v.save()
			logger.info(f'Saved a new video ID "{v.title}" in DB')
		except Exception as e:
			logger.error(str(e))


def get_random_word(lang: str = None) -> str:
	if not lang:
		lang: str = random.choice(list(DICTIONNARIES.keys()))
	lines = open(DICTIONNARIES[lang]).read().splitlines()
	return random.choice(lines)
