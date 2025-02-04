from enum import StrEnum


class Tags(StrEnum):
    DIARY_CARDS = "diary cards"
    EMOTIONS = "emotions"
    MEDICAMENTS = "medicaments"
    TARGETS = "targets"
    SKILLS = "skills"


class Prefix(StrEnum):
    ADMIN = "/admin"
    DIARY_CARDS = ""
    EMOTIONS = "/emotions"
    MEDICAMENTS = "/medicaments"
    TARGETS = "/targets"
    SKILLS = "/skills"
