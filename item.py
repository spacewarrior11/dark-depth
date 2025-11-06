import random


rings = [{"name":"Jeweled Ring", "points":50, "itemtype":1}, {"name":"False Gold Ring", "points":10, "itemtype":1}, {"name":"Gold Ring", "points":80, "itemtype":1}, {"name":"Brilliant Ring", "points":25, "itemtype":1}, {"name":"Ring of Gems", "points":75, "itemtype":1}, {"name":"Emerald Ring", "points":60, "itemtype":1}, {"name":"Blue Ring", "points":20, "itemtype":1}, {"name":"Misty Ring", "points":35, "itemtype":1}, {"name":"Ring of the Overmaster", "points":500, "itemtype":1}]
swords = [{"name":"Blade of Frost", "attack":[1-3], "inflictedstatus":["frozen"], "itemtype":0}, {"name":"Sword of Dozing Off", "attack":[1-4], "inflictedstatus":["asleep"],  "itemtype":0}, {"name":"Flame Smiter", "attack":[1-8], "inflictedstatus":["flaming"],  "itemtype":0}, {"name":"Bronze Sword", "attack":[3-10], "inflictedstatus":[],  "itemtype":0}, {"name":"Grand Sword", "attack":[4-12], "inflictedstatus":[],  "itemtype":0},  ] 

sheilds = [{"name":"Grand Sheild", "defence":5, "itemtype":2}, {"name":"Bronze Sheild", "defence":3, "itemtype":2}, {"name":"Metal Gloves", "defence":2, "itemtype":2}]
wands = [{"name":"Staff of Cold", "inflictedstatus":["frozen"], "area":"around", "wandtype":"effect", "itemtype":3}, {"name":"Staff of Destruction", "inflictedstatus":[], "area":"around", "wandtype":"destroy", "itemtype":3}, {"name":"Wand of Demolition", "inflictedstatus":[], "area":"ray", "wandtype":"destroy", "itemtype":3}, {"name":"Wand of Heat", "inflictedstatus":["Flaming"], "area":"ray", "wandtype":"effect", "itemtype":3}, {"name":"Wand of Cold", "inflictedstatus":["frozen"], "area":"ray", "wandtype":"effect", "itemtype":3}, {"name":"Staff of Fire", "inflictedstatus":["flaming"], "area":"around", "wandtype":"effect", "itemtype":3}, {"name":"Staff of Firey Sleep", "inflictedstatus":["flaming", "asleep"], "area":"around", "wandtype":"effect", "itemtype":3}]


def itempicker(itemtype):
    if itemtype == "sword":
        item = random.choice(swords)
    if itemtype == "ring":
        item = random.choice(rings)
    if itemtype == "wand":
        item = random.choice(wands)
    if itemtype == "sheild":
        item = random.choice(sheilds)
    return item
        