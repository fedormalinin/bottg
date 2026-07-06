import re


def detect_platform(url):

    if re.search(r"(youtube\.com|youtu\.be)", url):
        return "YouTube"

    if re.search(r"instagram\.com", url):
        return "Instagram"

    if re.search(r"(vk\.com|vkvideo\.ru)", url):
        return "VK"

    return "Unknown"