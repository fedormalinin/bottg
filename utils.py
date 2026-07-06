import re


def detect_platform(url: str):
    if re.search(r"youtube|youtu\.be", url):
        return "Это YouTube"

    if "instagram.com" in url:
        return "Это Instagram"

    if "vk.com" in url:
        return "Это VK"

    return "Ссылка не распознана"