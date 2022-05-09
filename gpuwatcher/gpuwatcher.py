import os
import argparse
import configparser
import time
from gpuwatcher.utils import getGPU, seedMessage

def main():
    parser = argparse.ArgumentParser()
    config = configparser.ConfigParser()
    if os.path.isfile("config.ini"):
        config.read("config.ini")
        hook_url = config["default"]["url"]
    else:
        print("please set url:")
        hook_url = input()
        config["default"] = {"url": hook_url}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    # parser.add_argument("email")
    parser.add_argument('--t', help="The Required memory size(G)")
    args = parser.parse_args()
    memoryFree, pids, pid_to_command = getGPU()
    # start check
    needmemory = float(args.t)
    availableGpus = []
    lastPid = []
    cuurpid = []
    for i in range(len(memoryFree)):
        if memoryFree[i] > 1024 * needmemory:
            availableGpus.append(i)
    if len(availableGpus) > 0:
        seedMessage(hook_url, availableGpus, memoryFree)

    for pid in pids:
        lastPid.append(pid)
    
    while True:

        availableGpus = []
        checkflag = False
        memoryFree, pids, pid_to_command = getGPU()

        for pid in pids:
            cuurpid.append(pid)
        
        for pid in lastPid:
            if pid not in cuurpid:
                checkflag = True
                break
        if checkflag:
            for i in range(len(memoryFree)):
                if memoryFree[i] > 1024 * needmemory:
                    availableGpus.append(i)
        lastPid = cuurpid
        
        if len(availableGpus) > 0:
            seedMessage(hook_url, availableGpus, memoryFree)
        
        time.sleep(30)

if __name__ == "__main__":
    main()