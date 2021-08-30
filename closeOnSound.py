import sounddevice as sd
import numpy as np
import win32gui, win32con
import os
import keyboard

def windowEnumHandler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def getAppList(handles=[]):
    mlst=[]
    win32gui.EnumWindows(windowEnumHandler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst

def minimizeWindow():
    #buggin inside vscode but working fine as standalone py?! -.-
    win32gui.SetForegroundWindow(windowHandle)
    win32gui.ShowWindow(windowHandle, win32con.SW_MINIMIZE)

def printSound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    volume = int(volume_norm)
    if(volume > volumeThreshold):
        print('Volume level:',volume)
        minimizeWindow()

volumeThreshold = 20
applicationName = input("Enter application name(must be open): ").lower()
volumeThreshold = int(input("Set volume threshold(default at 20): "))
userSavedVolume = volumeThreshold
os.system("cls")
print("\t\tListening.......")
print("You can now minimize this window or close to quit")
print("Press any key to pause/resume\n")
openWindows = getAppList()
paused = False
for i in openWindows:
    if applicationName in i[1].lower():
        windowHandle = i[0]
        windowName = i[1]
        break
with sd.Stream(callback=printSound):
    while(True):
        if keyboard.read_key() and paused == False:
            volumeThreshold = 10000
            paused = True
            print("\tPaused")
        elif keyboard.read_key() and paused == True:
            volumeThreshold = userSavedVolume
            paused = False
            print("\tResuming")
        sd.sleep(1000)