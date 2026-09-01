"""Bin-pack ordered LOs into lesson-sized understand chapters."""

import copy

from outline.rules.naming import chapter_base_name, uniquify_chapter_names

MAX_LOS_PER_CHAPTER = 4


def _close(bucket: list[dict], words: int, mins: int) -> dict:
    los = copy.deepcopy(bucket)
    for i, lo in enumerate(los, start=1):
        lo["module_number"] = i
    return {
        "chapter_name": chapter_base_name(bucket),
        "chapter_estimated_word_count": words,
        "chapter_estimated_time_minutes": mins,
        "learning_objectives": los,
    }


def pack_chapters(los: list[dict], word_limit: int, minute_limit: int) -> list[dict]:
    chapters: list[dict] = []
    bucket: list[dict] = []
    words = mins = 0
    for lo in los:
        over_words = words + lo["estimated_word_count"] > word_limit
        over_time = mins + lo["estimated_time_minutes"] > minute_limit
        over_density = len(bucket) >= MAX_LOS_PER_CHAPTER
        if bucket and (over_words or over_time or over_density):
            chapters.append(_close(bucket, words, mins))
            bucket, words, mins = [], 0, 0
        bucket.append(lo)
        words += lo["estimated_word_count"]
        mins += lo["estimated_time_minutes"]
    if bucket:
        chapters.append(_close(bucket, words, mins))
    return uniquify_chapter_names(chapters)
