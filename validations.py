import re
from textblob import TextBlob

JEWELRY_KEYWORDS = [
    "ring", "necklace", "bracelet", "jewelry", "jewel", "diamond", 
    "gem", "pendant", "earring", "stone", "gold", "silver", "platinum"
]

NEGATIVE_WORDS = [
    "dead", "blood", "gore", "hate", "kill", "weapon", "nudity", "violence", 
    "gun", "explicit", "death", "war" ,"nude","naked","topless","bottomless","undress","unclothed","exposed","erotic","sensual","sexual","sexy","lewd","NSFW","porn","pornography","xxx","adult","mature","lingerie","risqué","scantily clad","strip","stripping","stripper","fetish","breasts","boobs","nipples","areola","butt","buttocks","ass","anus","vagina","pussy","clit","clitoris","cock","penis","dick","erection","balls","testicles","genital","groin","nude body","private parts ","intercourse","sex","blowjob","handjob","oral","anal","doggy","missionary","gangbang","cum","ejaculation","squirt","fingering","groping","masturbation","moaning","orgasm","threesome","hardcore","softcore","bdsm","bondage","deepthroat","dominance","submission","intercourse","sex","blowjob","handjob","oral","anal","doggy","missionary","gangbang","cum","ejaculation","squirt","fingering","groping","masturbation","moaning","orgasm","threesome","hardcore","softcore","bdsm","bondage","deepthroat","dominance","submission ","pornstar","onlyfans","camgirl","webcam","amateur","erotic model","adult star","adult actress","NSFW artist ","lingerie","thong","panties","fishnet","see-through","transparent clothing","latex suit","dominatrix outfit","BDSM gear ","Negative prompt ","nude","porn","sexual","erotic","nipples","vagina","cock","ass","bondage","NSFW","topless","blowjob","orgasm" , "hot women", "women","hot women model","men","man","hot man"
]

def correct_spelling(prompt: str) -> str:
    words = prompt.strip().lower().split()
    corrected_words = []

    for word in words:
        if any(word == kw or word.rstrip('.,!?') == kw for kw in JEWELRY_KEYWORDS):
            corrected_words.append(word)
        else:
            corrected = str(TextBlob(word).correct())
            corrected_words.append(corrected)

    return ' '.join(corrected_words)

def is_valid_prompt(prompt: str):
    corrected = correct_spelling(prompt)
    cleaned = corrected.lower()
    
    has_jewelry = any(word in cleaned for word in JEWELRY_KEYWORDS)
    has_negative = any(neg in cleaned for neg in NEGATIVE_WORDS)

    is_valid = has_jewelry and not has_negative
    if not is_valid:
        return False
    return is_valid, corrected
