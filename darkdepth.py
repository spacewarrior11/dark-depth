from monsters import monsterlist
import random
import os
import keyboard
import copy
import passwordhanlder
import item


script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'gravestones.txt'
gravestonelocation = os.path.join(script_dir, file_name)

test = False
items = [{"name":"Old Sword", "attack":[1,6], "inflictedstatus":[], "itemtype":0}, {"name":"Rusted Ring", "points":0, "itemtype":1}, {"name":"Wood Buckler", "defence":1, "itemtype":2}]
health = 50
status = []
name = "T"
difficulty = 2

moveallowed = True

hint = 0
money = 0
level = 0

remmap = [[" " for j in range(64)] for i in range(30)]

soundverb = ["whisper", "mutter", "mumble", "speak", "say", "sing", "cough up", "yell", "scream", "howl", "gasp", "exclaim"]

screen = "start"
features = [{"name":"hint", "character":"~"}, {"name":"money", "character":"$"}, {"name":"gravestone", "character":"+"}, {"name":"sword", "character":"/"}, {"name":"ring", "character":"0"}, {"name":"wand", "character":"!"}, {"name":"sheild", "character":"]"}]

newmovetrail = [[0 for j in range(64)] for i in range(30)]

os.system("mode con cols=128 lines=32")
os.system("TITLE DarkDepth")

numrooms = 30
esc = False

def createdungeon():
    while True:
        dungeon, entities = generatedungeon()
        xp=random.randint(1, 61)
        yp=random.randint(1, 23)
        heatmap = heatmapgenerator(dungeon, 400, xp, yp)
        breakout = False
        for i in range(len(dungeon)):
            for j in range(len(dungeon[0])):
                if dungeon[i][j] != "#" and heatmap[i][j] == 500:
                    breakout = True
                    break
            if breakout == True:
                break
        else:
            break
    return dungeon, entities
                


def generatedungeon():
    dungeon = [["#" for j in range(64)] for i in range(30)]
    rooms = []
    while len(rooms) < numrooms:
        overlap = False
        x1 = random.randint(1, 56)
        y1 = random.randint(1, 23)
        x2 = x1 + random.randint(2, 5)
        y2 = y1 + random.randint(2, 5) 
        for i in range(y1 - 1, y2 +1):
            for j in range(x1 - 1, x2 + 1):
                if dungeon[i][j] == "_":
                    overlap = True
        if overlap == False:
            for i in range(y1, y2):
                for j in range(x1, x2):
                    dungeon[i][j] = "_"
            rooms.append([(x1+y1)//2, (x1 + x2)//2, (y1+y2)//2])
    for room in rooms:
        mindifference = 1000000
        for i in range(len(rooms)):
            difference = abs(room[0] - rooms[i][0])
            if difference < mindifference and difference != 0:
                mindifference = difference
                mindifx = rooms[i][1]
                mindify = rooms[i][2]
        if room[1] < mindifx :
            x1 = room[1]
            x2 = mindifx +1
        else:
            x1 = mindifx
            x2 = room[1] +1
        if room[2] < mindify:
            y1 = room[2]
            y2 = mindify
        else:
            y1 = mindify
            y2 = room[2]
        try: 
            if random.randint(1,2) == 1:
                for i in range(x1, x2):
                    if dungeon[room[2]][i] == "#":
                        dungeon[room[2]][i] = "."
                for i in range(y1, y2):
                    if dungeon[i][mindifx] == "#":
                        dungeon[i][mindifx] = "."
            else: 
                for i in range(x1, x2):
                    if dungeon[mindify][i] == "#":
                        dungeon[mindify][i] = "."
                for i in range(y1, y2):
                    if dungeon[i][room[1]] == "#":
                        dungeon[i][room[1]] = "."
        except:
            input("error")
    entities = dungeondressing(dungeon)

            
    return dungeon, entities

def dungeondressing(dungeon):
    takenpos = []
    entities = []
    for i in range(random.randint(numrooms//3,numrooms//2)):
        dressing = copy.deepcopy(random.choice(features))
        x=random.randint(1, 61)
        y=random.randint(1, 23)
        while dungeon[y][x] != "_" and not [x, y] in takenpos:
            x=random.randint(1, 61)
            y=random.randint(1, 23)
        takenpos.append([x, y])
        entities.append({"character":dressing["character"], "name":dressing["name"], "x":x, "y":y})
    for i in range(4):
        x=random.randint(1, 61)
        y=random.randint(1, 23)
        while dungeon[y][x] != "_" and not [x, y] in takenpos:
            x=random.randint(1, 61)
            y=random.randint(1, 23)
        takenpos.append([x, y])
        entities.append({"character":"~", "name":"hint", "x":x, "y":y})
    
    return entities

def monsterspawn(dungeon):
    monsters = []
    monsterlocations = [[0 for j in range(64)] for i in range(30)]
    for i in range(random.randint(numrooms//5,numrooms//4)):
        monstertype = random.choice(monsterlist)
        while monstertype["level"] > level:
            monstertype = random.choice(monsterlist)
        x=random.randint(1, 61)
        y=random.randint(1, 23)
        while dungeon[y][x] != "_":
            x=random.randint(1, 61)
            y=random.randint(1, 23)
        for j in range(random.randint(monstertype["number"][0], monstertype["number"][1])):
            monster = copy.deepcopy(monstertype)
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            for i in range(25):
                try: 
                    if dungeon[y][x] != "_" and monsterlocations[y][x] == 0:
                        x += random.randint (-1, 1)
                        y += random.randint(-1, 1)
                except:
                    break
            monster["x"] = x
            monster["y"] = y
            monster["status"] = []
            try:
                if dungeon[y][x] == "_" and monsterlocations[y][x] == 0: 
                    monsters.append(monster)
                    monsterlocations[y][x] = 1 
            except:
                pass
    return monsters




def playerxy(dungeon):
    x=random.randint(1, 61)
    y=random.randint(1, 23)
    while dungeon[y][x] != "_":
        x=random.randint(1, 61)
        y=random.randint(1, 23)
    return x,y

def newlevel():
    global dungeon, entities, password, x, y, screen, monsters, hint, level, remmap
    hint = 0
    remmap = [[" " for j in range(64)] for i in range(30)]
    level += 1
    dungeon, entities = createdungeon()
    password = passwordhanlder.passwordgenerator()
    monsters = monsterspawn(dungeon)
    x, y = playerxy(dungeon)
    if screen != "start":
        screen = "dungeon"

def heatmapgenerator(dungeon, dist, x, y):
    heatmap = [[500 for j in range(64)] for i in range(30)]
    heatmap[y][x] = 0
    checkedsquares = [[x,y]]
    newlychecked = []
    for i in range(dist):
        
        for square in checkedsquares:
            if dungeon[square[1]][square[0] +1] != "#" and heatmap[square[1]][square[0] +1] == 500:
                heatmap[square[1]][square[0] +1] = (i +1) * 2
                newlychecked.append([square[0] +1, square[1]])
            if dungeon[square[1]][square[0] -1] != "#" and heatmap[square[1]][square[0] -1] == 500:
                heatmap[square[1]][square[0] -1] =(i +1) * 2
                newlychecked.append([square[0] -1, square[1]])
            if dungeon[square[1] +1][square[0]] != "#" and heatmap[square[1]+1][square[0]] == 500:
                heatmap[square[1]+1][square[0] ] =(i +1) * 2
                newlychecked.append([square[0], square[1] +1])
            if dungeon[square[1] -1][square[0] ] != "#" and heatmap[square[1] -1][square[0] ] == 500:
                heatmap[square[1] -1][square[0] ] =(i +1) * 2
                newlychecked.append([square[0], square[1] -1])
        checkedsquares = newlychecked
        newlychecked = []
    return heatmap
         

def monsterai(monster):
    global movetrail, newmovetrail
    closest = [100,0, 0]
    if monster["activeai"] == "hoard":
        myheatmap = copy.deepcopy(heatmap)
        for _ in range(4):
            closest = [100,0, 0]

            if myheatmap[monster["y"]][monster["x"]] + movetrail[monster["y"]][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]] + movetrail[monster["y"]][monster["x"]], 0, 0]
            if myheatmap[monster["y"]-1][monster["x"]] + movetrail[monster["y"]-1][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]-1][monster["x"]] + movetrail[monster["y"]-1][monster["x"]], 0, -1]
            if myheatmap[monster["y"]+1][monster["x"]] + movetrail[monster["y"]+1][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]+1][monster["x"]] + movetrail[monster["y"]+1][monster["x"]], 0, +1]
            if myheatmap[monster["y"]][monster["x"]-1] + movetrail[monster["y"]][monster["x"]-1] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]-1] + movetrail[monster["y"]][monster["x"]-1], -1, 0]
            if myheatmap[monster["y"]][monster["x"]+1] + movetrail[monster["y"]][monster["x"]+1] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]+1] + movetrail[monster["y"]][monster["x"]+1], +1, 0]
            
            if closest[1] != 0 or closest[2] != 0:
                
                for mon in monsters:
                    if mon["x"] == monster["x"] + closest[1] and mon["y"] == monster["y"] + closest[2]:
                        myheatmap[monster["y"] + closest[2]][monster["x"] + closest[1]] = 500
                        myheatmap[monster["y"]][monster["x"]] += 3
                        newmovetrail[monster["y"]][monster["x"]] = 1
                        break
                else:
                    break
                        
                
        monster["x"], monster["y"] = move(monster["x"], monster["y"], closest[1], closest[2], False, monster["attack"], monster["inflictedstatus"])

    if monster["activeai"] == "mad":
        if monster["y"] - 1 == y:
            move(monster["x"], monster["y"], 0, -1, False, monster["attack"])
        if monster["y"] + 1 == y:
            move(monster["x"], monster["y"], 0, +1, False, monster["attack"])
        if monster["x"] - 1 == x:
            move(monster["x"], monster["y"], -1, 0, False, monster["attack"])
        if monster["x"] + 1 == x:
            move(monster["x"], monster["y"], +1, 0, False, monster["attack"])
        monster["x"], monster["y"] = move(monster["x"], monster["y"], random.randint(-1, 1), random.randint(-1, 1), False, monster["attack"], monster["inflictedstatus"])
    
    if monster["activeai"] == "charge":
        myheatmap = copy.deepcopy(heatmap)
        for _ in range(4):
            closest = [100,0, 0]

            if myheatmap[monster["y"]][monster["x"]] + movetrail[monster["y"]][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]] + movetrail[monster["y"]][monster["x"]], 0, 0]
            if myheatmap[monster["y"]-2][monster["x"]] + movetrail[monster["y"]-2][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]-2][monster["x"]] + movetrail[monster["y"]-2][monster["x"]], 0, -2]
            if myheatmap[monster["y"]+2][monster["x"]] + movetrail[monster["y"]+2][monster["x"]] < closest[0]:
                closest = [myheatmap[monster["y"]+2][monster["x"]] + movetrail[monster["y"]+2][monster["x"]], 0, +2]
            if myheatmap[monster["y"]][monster["x"]-2] + movetrail[monster["y"]][monster["x"]-2] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]-2] + movetrail[monster["y"]][monster["x"]-2], -2, 0]
            if myheatmap[monster["y"]][monster["x"]+2] + movetrail[monster["y"]][monster["x"]+2] < closest[0]:
                closest = [myheatmap[monster["y"]][monster["x"]+2] + movetrail[monster["y"]][monster["x"]+2], +2, 0]
            
            if closest[1] != 0 or closest[2] != 0:
                
                for mon in monsters:
                    if mon["x"] == monster["x"] + closest[1] and mon["y"] == monster["y"] + closest[2]:
                        myheatmap[monster["y"] + closest[2]][monster["x"] + closest[1]] = 500
                        myheatmap[monster["y"]][monster["x"]] += 3
                        newmovetrail[monster["y"]][monster["x"]] = 1
                        break
                else:
                    break
   
    
    
    
    return monster
        
        
        
        

    
def runai():
    global heatmap, monsters, movetrail, newmovetrail
    movetrail = newmovetrail
    newmovetrail = [[0 for j in range(64)] for i in range(30)]
    heatmap = heatmapgenerator(dungeon, 8, x, y)
    for monster in monsters:
        monster["activeai"] = monster["brain"]
        if "frozen" in monster["status"]:
            if "flaming" in monster["status"]:
                monster["status"].remove("frozen")
                monster["status"].remove("flaming")
        if "asleep" in monster["status"]:
            if random.randint(1,6) == 1:
                monster["status"].remove("asleep")
        if "flaming" in monster["status"]:
            monster["health"] += random.randint(-5, -1)
            if random.randint(1,6) == 1:
                monster["status"].remove("flaming")
        if "poison" in monster["status"]:
            monster["health"] += random.randint(-3, -1)
        if "mad" in monster["status"]:
            monster["activeai"] = "mad"
        if not "frozen" in monster["status"] and not "asleep" in monster["status"] and not "stunned" in monster["status"]:
            monster = monsterai(monster)
        if "stunned" in monster["status"]:
            monster["status"].remove("stunned")
    
    

        




def printscreen():
    global screen, hint, items, money, name, test, toprint, remmap, difficulty
    toprint = []
   
    os.system("cls")
    if screen == "dungeon":
        toprint = copy.deepcopy(dungeon)
        for entity in entities:
            toprint[entity["y"]][entity["x"]] = entity["character"]
        for monster in monsters:
            toprint[monster["y"]][monster["x"]] = monster["character"]
        toprint[y][x] = "@"
        if test == False:
            if dungeon[y][x] == "_":
                uppery = y
                lowery = y
                leftx = x
                rightx = x
                while dungeon[uppery][x] == "_":
                    uppery += -1
                while dungeon[lowery][x] == "_":
                    lowery += 1
                while dungeon[y][leftx] == "_":
                    leftx += -1
                while dungeon[y][rightx] == "_":
                    rightx += 1
            if dungeon[y][x] == ".":
                uppery = y - 1
                lowery = y + 1
                leftx = x - 1
                rightx = x + 1
        else:
            uppery = -1
            lowery = 300
            leftx = -1
            rightx = 300
        for i in range(len(toprint)):
            for j in range(len(toprint[0])):
                if i <= lowery and i >= uppery and j <= rightx and j >= leftx:
                    pass
                else:
                    
                    toprint[i][j] = " "
        if difficulty == 1:
            for i in range(len(remmap)):
                for j in range(len(remmap[0])):
                    if remmap[i][j] != ' ' and toprint[i][j] == " ":
                        toprint[i][j] = remmap[i][j]
        for line in toprint:
            for char in line:
                print(char, end="")
                print(" ", end="")
            print()
        for i in range(len(toprint)):
            for j in range(len(toprint[0])):
                #if toprint[i][j] != " ":
                if toprint[i][j] != " " and toprint[i][j] != "#":
                    remmap[i][j] = dungeon[i][j]
                    #remmap[i][j] = "?"

        statusstring = ""
        if len(status) > 0:
            statusstring = status[0]
            for i in range(len(status) -1):
                statusstring = f"{statusstring}, {status[i+1]}"
        if test == True:    
            print(f"{x}, {y}, health: {health}, password {password}, difficulty: {difficulty}, score: {money + ((level)*25*difficulty) + items[1]['points']},  status: {statusstring}")
        else:
            print(f"health: {health}, difficulty: {difficulty}, score: {money + ((level)*25*difficulty) + items[1]['points']},  status: {statusstring}")
    if screen == "password":
        print("***WHAT IS THE PASSWORD?***")
        inputedpassword = ""
        for i in range(4):
            inputedpassword = inputedpassword + readkey()
            os.system("cls")
            print("***WHAT IS THE PASSWORD?***")
            print(inputedpassword)
        if inputedpassword == password:
            print(f"You {random.choice(soundverb)} {password}! The dungeon morphs around you.")
            print("press any key to continue")
            
            newlevel()
        else: 
            screen = "dungeon"
    if screen == "death":
        saying = ""
        while True:
            os.system("cls")
            print("***YOU HAVE FALLEN***")
            print(f"Money: {money}$")
            print(f"Level: {level}")
            print(f"Score: {money + ((level)*25*difficulty) + items[1]['points']}")
            print("What to write on your stone? (Press enter to continue to the afterlife...) ")
            print(saying)
            key = readkey()
            if key == "enter":
                break
            elif len(key) == 1:
                saying = saying + key
        gravestone = f"{name}~{money + (level)*25*difficulty}~{level}~{saying}"
        with open(gravestonelocation, "a") as file:
          
            file.write(f"{gravestone}\n")
        quit()
    if screen == "hint":
        riddle = passwordhanlder.generateriddle(list(password)[hint], hint +1)
        hint += 1
        if hint > 3:
            hint = 0
        print("***YOU READ THE PIECE OF PARCHMENT***")
        print("It says:")
        print(riddle)
        print("press any key to continue")
        
        screen = "dungeon"
    if screen == "item":
        for i in range(len(entities)):
            if entities[i]["y"] == y and entities[i]["x"] == x:
                
                try: 
                    entities[i]["itemtype"]
                    pickedupitem = entities[i]
                except:
                    pickedupitem = item.itempicker(entities[i]["name"])
                if pickedupitem["itemtype"] != 3:
                    droppeditem = items[pickedupitem["itemtype"]] 
                    entities[i] = copy.deepcopy(droppeditem)
                    entities[i]["x"] = x
                    entities[i]["y"] = y
                    if entities[i]["itemtype"] == 0:
                        entities[i]["character"] = "/"
                    if entities[i]["itemtype"] == 1:
                        entities[i]["character"] = "0"
                    if entities[i]["itemtype"] == 2:
                        entities[i]["character"] = "]"
                    
                else:
                    entities.pop(i) 
                if pickedupitem["itemtype"] == 3:
                    items.append(pickedupitem)
                else:
                    items[pickedupitem["itemtype"]] = pickedupitem
                break
        print(f"***YOU PICK UP A {pickedupitem['name'].upper()}***")
        if pickedupitem["itemtype"] != 3:
            print(f"You drop the {droppeditem['name']}")
        print("press any key to continue")
        screen = "dungeon"
    if screen == "inventory":
        print("***YOU LOOK AT YOURSELF AND FIND THE FOLLOWING***")
        print(f"{money}$")
        for thing in items:
            print(thing["name"])
        print("press any key to continue")
        screen = "dungeon"
    if screen == "money":
        collectedmoney = random.randint(1, 100)
        money += collectedmoney
        print(f"***YOU PICK UP {collectedmoney}$***")
        print(f"You now have {money}$")
        print("press any key to continue")
        screen = "dungeon"
    if screen == "gravestone":
        with open(gravestonelocation, "r+") as file:
            content = file.readlines()
            for i in range(len(content)):
                if int(content[i].split("~")[2].strip()) == level:
                    gravestone = content[i].split("~")
                    file.seek(0)
                    for j in range(len(content)):
                        if j != i:
                            file.write(content[j])
                    file.truncate()
                    break
            else:
                gravestone = ["Unreadable", "0", 0, "The saying is destroyed.\n"]
        print("***YOU READ THE GRAVESTONE***")
        print("It says the following: ")
        print(f"Name: {gravestone[0]}")
        print(f"Score: {gravestone[1]}")
        print(gravestone[3], end="")
        print("press any key to continue")
        screen = "dungeon"
        
    if screen == "start":
        name = ""
        while True:
            os.system("cls")
            print("***YOU PREPARE TO DECEND INTO THE DUNGEON OF POINTLESS DEATH***")
            print("What is your name?")
            print(name)
            key = readkey()
            if key == "enter":
                break
            else:
                name = name + key
        if name == "test":
            test = True
        print("Do you want to play in easy (1), or normal (2) mode?")
        key = readkey()
        if key == "1":
            difficulty = 1
        elif key == "2":
            difficulty = 2
        else:
            difficulty = 2
        print("press any key to continue, while in the game press 'h' for the help menu.")
        screen = "dungeon"
    if screen == "help":
        print("***YOU ARE IN THE DUNGEON OF POINTLESS DEATH***")
        print("Your goal is to decend as far and collect as much money as possible.")
        print("You start with 50 health and basic items.")
        print("Collect other items, money, read graves and read hints with 'g'.")
        print("Move around with the arrow keys. Use wands with 'z'.")
        print("Look in your inventory with 'i'.")
        print("To decend into deeper levels you must figure out the four letter password.")
        print("You can find hints around the dungeon. Once you have the password press 'p'.")
        print("If the screen confuses you, press 'l' for the legend.")
        print("abcdefghijklmnopqrstuvwxyz")
        print("12345678901234567890123456")
        print("Good luck and try not to die.")
        print("press any key to continue")
        screen = "dungeon"
    if screen == "legend":
        print("***HERE IS THE LEGEND FOR WHAT YOU SEE***")
        print("You are the '@'.")
        print("'_' is the floor of a room while '.' is the floor of a corridor.")
        print("'#' is a wall.")
        print("'/' is a sword, '0' is a ring, ']' is a sheild, '!' is a wand, '+' is a gravestone, '~' is a hint.")
        print("The letters are monsters:")
        print("'A' is an ant, 'B' is a bat, 'D' is a dragon, 'E' is an elephant, 'F' is a falcon, 'G' is a giant,")
        print("'H' is a hobgoblin, 'O' is an orc, 'S' is a sleep inducing snake, 'T' is a troll, 'L' is a laza lizard.")
        print("press any key to continue")
        screen = "dungeon"
        






def readkey():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name != "space" and event.name != "backspace":
                return event.name
            else:
                return " "
    
def processkey():
    key = readkey()
    if moveallowed == False:
        return
    global x, y, esc, screen, dungeon
    if key == "up":
        x, y = move(x, y, 0, -1)
    if key == "down":
        x, y = move(x, y, 0, 1)
    if key == "right":
        x, y = move(x, y, 1, 0)
    if key == "left":
        x, y = move(x, y, -1, 0)
    if key == "esc":
        esc = True 
    if key == "p":
        screen = "password"
    if key == "g":
        for i in range(len(entities)):
            if entities[i]["y"] == y and entities[i]["x"] == x:
                if entities[i]["name"] == "hint": 
                    screen = "hint"
                    entities.pop(i)
                    break
                elif entities[i]["name"] == "money":
                    screen = "money"
                    entities.pop(i)
                    break
                elif entities[i]["name"] == "gravestone":
                    screen = "gravestone"
                    break
                else:
                    screen = "item"
                    
                    break
    if key == "i":
        screen = "inventory"
    if key == "h":
        screen = "help"
    if key == "l":
        screen = "legend"
    if key == "z":
        os.system("cls")
        print("***WHICH WAND SHALL YOU USE***")
        index = 0
        wands = []
        for thing in items:
            if thing["itemtype"] == 3:
                index += 1
                print(f"{index}, {thing['name']}")
                wands.append(thing)
        if index > 0:
            
            print("Which wand do you wish to zap?")
            area = [[0 for j in range(64)] for i in range(30)]
            wand = {}
            key = readkey()
            try:
                if int(key) <= index and int(key) > 0:
                    wand = wands[int(key) -1]
                    items.remove(wand)
                
            except:
                pass
            if wand == {}:
                return
            if wand["area"] == "around":
                for i in range(len(area)):
                    for j in range(len(area[1])):
                       
                        if abs(i - y) < 3 and abs(j - x) < 3:
                            area[i][j] = 1
            if wand["area"] == "ray":
                print("In which direction will you zap this wand?")
                key = readkey()
                if key == "up":
                    for i in range(len(area)):
                        if i < y:
                            area[i][x] = 1
                if key == "down":
                    for i in range(len(area)):
                        if i > y:
                            area[i][x] = 1
                if key == "right":
                    for i in range(len(area[1])):
                        if i > x:
                            area[y][i] = 1
                if key == "left":
                    for i in range(len(area[1])):
                        if i < x:
                            area[y][i] = 1

            



            if wand["wandtype"] == "effect":
                for monster in monsters:
                    if area[monster["y"]][monster["x"]] == 1:
                        for status in wand["inflictedstatus"]:
                            if not status in monster["status"]:
                                monster["status"].append(status)
            if wand["wandtype"] == "destroy":
                for i in range(len(area)):
                    for j in range(len(area[1])):
                        if area[i][j] == 1:
                            dungeon[i][j] = "."
                            



            

                

def move(startx, starty, xchange, ychange, player=True, attack = items[0]["attack"], inflictedstatus = []):
    global monsters, health, status
    for monster in monsters:
        if monster["x"] == startx + xchange and monster["y"] ==starty + ychange:
            if player==True:
                monster["health"] += -1 * (random.randint(attack[0], attack[1]) - monster["defence"])
                for s in items[0]["inflictedstatus"]:
                    if not s in monster["status"]:
                        monster["status"].append(s)
            break
    else:
        if startx + xchange != x or starty + ychange != y:
            if dungeon[starty+ychange][startx + xchange] != "#":
                if player == False:
                    startx += xchange
                    starty += ychange
                if player == True and moveallowed == True:
                    startx += xchange
                    starty += ychange
        elif player == False:
            health += -1 * max((random.randint(attack[0], attack[1]) - items[2]["defence"]), 0)
            for s in inflictedstatus:
                if not s in status:
                    status.append(s)

    
    return startx, starty
    
def checkdead():
    global monsters, screen
    survivors = []
    nummonsters = len(monsters) 
    for i in range(nummonsters):
        if monsters[i]["health"] > 0:
            survivors.append(monsters[i])
        elif random.randint(1, 3) == 1:
            entities.append({"name":"money", "character":"$", "x":monsters[i]["x"], "y":monsters[i]["y"]})
    monsters = survivors
    if health <= 0:
        screen = "death"

def checkstatus():
        global health, status, moveallowed
        if "frozen" in status:
            if "flaming" in status:
                status.remove("frozen")
                status.remove("flaming")
        if "asleep" in status:
            if random.randint(1,6) == 1:
                status.remove("asleep")
        if "flaming" in status:
            health += random.randint(-5, -1)
            if random.randint(1,6) == 1:
                status.remove("flaming")
        if "poison" in status:
            health += random.randint(-3, -1)
        if "stunned" in status and random.randint(1, 3) == 1:
            status.remove("stunned")
        if "frozen" in status or "asleep" in status or "stunned" in status:
           moveallowed = False 
        if "stunned" in status:
            status.remove("stunned")

def main():
    while esc == False:
        moveallowed = True
        printscreen()
        checkstatus()
        processkey()
        runai()
        checkdead()


newlevel()

main()

input()
    
