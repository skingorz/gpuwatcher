import pynvml
import psutil

import requests

def seedMessage(url, availableGpus, memoryFree):
    message = "Gpu "
    if len(availableGpus) > 0:
        for i in availableGpus:
            message += "id: "
            message += str(i)
            message += "("
            message += str(int(memoryFree[i]))
            message += "MB) "
        message += " is avaliable"
        print(message)
    
    params = {
        "msg_type": "text",
        "content": {"text": message},
    }
    resp = requests.post(url=url, json=params)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") and result["code"] != 0:
        print(result["msg"])
        return
    print("notification sent")


def getGPU():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    memoryFree = []
    pids = set()
    pid_to_command = {}
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        memoryFree.append(meminfo.free/1024**2)
        info_list = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        for pidinfo in info_list:
            pid = pidinfo.pid
            pids.add(pid)
            s = psutil.Process(pid)
            command_text = ""
            for word in s.cmdline():
                command_text += word
                command_text += " "
            pid_to_command[pid] = command_text
    pynvml.nvmlShutdown()
    return memoryFree, pids, pid_to_command
