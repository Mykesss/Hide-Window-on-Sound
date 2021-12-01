import sounddevice as sd
import numpy as np
import win32gui, win32con
import os
import keyboard
from sound import Sound

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
        try:
            Sound.mute()
            minimizeWindow()
            print("\tPaused. F4 to resume")
            keyboard.wait('F4')
            print("\tResuming")
            Sound.volume_up()
        except: 
            pass

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
        focusedWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if keyboard.is_pressed('F4') and paused == False: #hating this function with passion
            focusedWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if "py.exe" in focusedWindow:
                volumeThreshold = 10000
                paused = True
                print("\Paused. F4 to resume")
        elif keyboard.is_pressed('F4') and paused == True:
            focusedWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if "py.exe" in focusedWindow:
                volumeThreshold = userSavedVolume
                paused = False
                print("\tResuming")
                Sound.volume_up()
        sd.sleep(500)
