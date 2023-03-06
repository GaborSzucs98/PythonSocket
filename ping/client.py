import subprocess
import json
import sys
import os


with open(sys.argv[1]) as file:
    lines=file.readlines()
    sites = lines[:10]
    leng = len(lines)-10  
    sites.extend(lines[leng:])
    
    lista = []
    for x in sites:
        x = x.split(',')[1]
        x = x.strip()
        lista.append(x)
        
        G = ["google.com"]
    with open ("ping.json",'w') as p:
        pings = []
        for x in G:
            p1 = os.popen(f"ping -n 10 {x}").read()
            ping = {"target" : f"{x}",
            "output" : f"{p1}"}
            pings.append(ping)
        data = {"date" : "20220313",
        "system": "Windows",
        "pings" : pings
        }
        
        pingout = json.dumps(data)
        p.write(pingout)
        
    with open ("traceroute.json",'w') as t:
        traces = []
        for x in G:
            p1 = os.popen(f"tracert -h 30 {x}").read()
            trace = {"target" : f"{x}",
            "output" : f"{p1}"}
            traces.append(trace)
        data = {"date" : "20220313",
        "system": "Windows",
        "traces" : traces
        }
        traceout = json.dumps(data)
        t.write(traceout)