import re

def removePunct(address):
    punct = "`؛;_ـ،/:.-'|"
    address = re.sub(f"[{re.escape(punct)}]", "", address)
    
    return address

def changeEnglishToArabic(address):
    mapping = {
        "floor":"دور",
        "st":"شارع",
        "street":"شارع",
        "apartment":"شقه",
        "apt":"شقه",
    }
    for eng, arb in mapping.items():
        address = re.sub(rf"\b{eng}\b", arb, address, flags=re.IGNORECASE)

    return address


def changeNumEngToArabic(address):
    arbNum = "٠١٢٣٤٥٦٧٨٩"
    engNum = "0123456789"
    
    return address.translate(str.maketrans(engNum, arbNum))

def convertCharToWord(address):
    mapping = {
        "ش":"شارع",
        "د":"دور"
    }
    for char, word in mapping.items():
        address = re.sub(rf"\b{char}\b", word, address)

    return address


def normalizeSomeChar(address):
    src = "اأإآيىگكؤوةه"
    dst = "ااااييككووهه"
    
    return address.translate(str.maketrans(src, dst))


def dropDuplicateSafeChars(address):
  
    return re.sub(r"(.)\1+", r"\1", address)


def numArabicApt(address):
    wordToNum = {
        "واحد":"١", 
        "الاولي": "١",

        "اثنين": "٢", 
        "الثانيه": "٢",
        "اتنين": "٢", 
        "التانيه": "٢",
        
        "ثلاثه": "٣",
        "تلاته": "٣",
        "الثالثه": "٣", 
        "التالته": "٣",

        "اربعه": "٤", 
        "الرابعه": "٤",

        "خمسه": "٥", 
        "سته":"٦", 
        "سبعه":"٧",

        "ثمانيه": "٨", 
        "تمانيه": "٨",

        "تسعه": "٩",
        "عشره":"١٠",
    }
    for word, num in wordToNum.items():
        address = re.sub(rf"\b{word}\b", num, address)
        
    return address


def numArabicFloor(address):
    wordToNum = {
        "الاول": "١",

        "التاني": "٢", 
        "الثاني":"٢",

        "الثالث": "٣", 
        "التالت":"٣",

        "الرابع": "٤", 
        "الخامس": "٥", 
        "السادس":"٦", 
        "السابع": "٧",

        "الثامن": "٨", 
        "التامن":"٨",

        "التاسع": "٩", 
        "العاشر":"١٠",
    }
    for word, num in wordToNum.items():
        address = re.sub(rf"\b{word}\b", num, address)
        
    return address


def preprocessing(address):
    address = str(address)
    address = changeEnglishToArabic(address)
    address = removePunct(address)
    address = convertCharToWord(address)
    address = changeNumEngToArabic(address)
    address = normalizeSomeChar(address)
    address = dropDuplicateSafeChars(address)
    address = numArabicApt(address)
    address = numArabicFloor(address)
    
    return address.strip()