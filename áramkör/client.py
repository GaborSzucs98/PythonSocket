import sys
import json

with open(sys.argv[1]) as file:
    data = json.load(file)

links = data["links"]
routes = data["possible-circuits"]
sim = data["simulation"]["demands"]
duration = data["simulation"]["duration"]
demands = data["simulation"]["demands"]
events = 0
simtime = 0
usedpaths = []

def reachable(x,y):
    reach = bool(0)
    for route in routes:
        if x == route[0] and y ==route[len(route)-1]:
            reach = bool(1)
    return reach
        
def ways (x,y):
    n=0
    ways = []
    for route in routes:
        if x == route[0] and y ==route[len(route)-1]:
            ways.append(route)
            n+=1
    return ways
    
def needed (way):
    jumps = []
    for i,j in zip(way[:-1],way[1:]):
        link = [i,j]
        jumps.append(link)
    return jumps
    
def cap(jumps,d):
    cap = bool(1)
    for x in jumps:
        for link in links:
            if x == link["points"]:
                if link["capacity"] <d:
                    cap = bool(0)
    return cap
    
def demand(jumps,d):
    for x in jumps:
        for link in links:
            if x == link["points"]:
                link["capacity"] -= d
    
    
def start(x,y,d):
    global events
    if reachable(x,y):
        paths = ways(x,y)
        demanded = bool(0)
        nways = len(paths)
        i = 0
        while not demanded and i<nways:
            path = needed (paths[i])
            i+=1
            if cap(path,d):
                demand(path,d)
                demanded = bool(1)
                usedpaths.append({"ends": [x,y], "used" :path})
                
        if demanded:
            events += 1
            print (f"{events}. igény foglalás: {x} <-> {y} st:{simtime} – sikeres")
        else:
            events += 1
            print (f"{events}. igény foglalás: {x} <-> {y} st:{simtime} – sikertelen")         
    else:
        events += 1
        print (f"{events}. igény foglalás: {x} <-> {y} st:{simtime} – sikertelen")
        
def end (x,y,d):
    global events
    ends = [x,y]
    for path in usedpaths:
        if ends == path["ends"]:
            demand(path["used"],-d)
            usedpaths.remove(path)
            events += 1
            print (f"{events}. igény felszabadítás: {x} <-> {y} st:{simtime}")

def simulation (demands, t):
    global simtime
    for i in range(0,t):
        simtime = i
        for demand in demands:
            if i == demand["start-time"]:
                start(demand["end-points"][0],demand["end-points"][1],demand["demand"])
            if i == demand["end-time"]:
                end (demand["end-points"][0],demand["end-points"][1],demand["demand"])
                

simulation(demands, duration)
