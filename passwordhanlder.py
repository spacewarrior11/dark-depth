import random

passwordpieces = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
piecessynonyms = [["one", "1", "first place"], ["pollenator", "to __ or not to __", "honey"], ["ocean", "sea", "vision"], ["4th", "backwards bee"], ["aliens first name", "most common"], ["only one that makes you find out", "voiceless v"], 
                  ["the missing tail of juman", "shortest gangster"], ["number one element", "water-gen"], ["me", "vision makers", "reason for glasses"], ["bird", "one whos walk is not allowed", "blue flyer"], ["short for okay", "letter that you say once or twice, never thrice"],
                ["loser", "__avator"], ["rapper and wrapper", "slang for the third person plural pronoun"], ["middle of MO", "&"], ["realisation onomatopia", "precurser to NO!!!"], ["urine", "180ed d"],["line of people", "wrong way pee"], ["pirates noised", "us be toys"], ["pluralafier", "snake"], 
                ["hot water", "tea"], ["not me", "second person pronoun", "w / 2"], ["first letter of the second planet", "11 x 2nd"], ["treasure marker", "multiplier"], ["question", "opposite of N"], ["comic sleep", "back", "end"]]
positionsynonyms = [["first place", "front", "first", "leftmost"], ["silver medal", "second place", "middle left", "third from the end"], ["bronze medal", "third place", "middle right", "before last"], ["end", "last", "butt", "back"]]

def passwordgenerator():
    password = ""
    for i in range(4):
        passwordpart = random.choice(passwordpieces)
        password = password + passwordpart
    return password

def generateriddle(passwordpart, position):
    riddleformat = random.randint(1, 3)
    riddle = ""
    if riddleformat == 1:
        riddle = f"The {position}th place is the {passwordpieces.index(passwordpart) +1}th letter"
    if riddleformat == 2 or riddleformat == 3:
        riddle = f"The {random.choice(positionsynonyms[position - 1])} place is the {random.choice(piecessynonyms[passwordpieces.index(passwordpart)])}  "
    if riddleformat == 4:
        riddle = f"The {position}th place is the {random.choice(piecessynonyms[position - 1])}"
    
    return riddle
'''
password = passwordgenerator()
for i in range(4):
    print(generateriddle(list(password)[i], i +1))

input()
'''