from typing import List


def city_raw_text(locale) -> List[str]:
    return [locale.brest]


def representation_raw_text(locale) -> List[str]:
    return [locale.text, locale.photo]


def number_of_posts_raw_text(locale) -> List[str]:
    return [str(text) for text in locale.number_of_posts]
