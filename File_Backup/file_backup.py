__author__ = 'Craig'

import shutil
import os
import ctypes
from tkinter import *
from tkinter import filedialog, messagebox
import time


'''
-----------STILL TO DO----------
-convert to windows exec file

-maybe some other stuff???
'''

#make files if this is the first time running
try:
    file = open("All_Folders_To_Backup.txt")
except FileNotFoundError:
    file = open("All_Folders_To_Backup.txt", "w")
file.close()


#classes
class completeWindow():
    def __init__(self):
        self.win = Tk()
        self.win.wm_title("All Done")
        lbl = Label(self.win, text="Backup Complete!")
        lbl.grid(padx=5,pady=5,columnspan=2)
        ok = Button(self.win, text="Continue", command=self.destroyWindow,padx=5)
        ok.grid(row=1, pady=5, padx=5)
        exit = Button(self.win, text="Exit", command=self.exitAll,padx=15)
        exit.grid(row=1, column=1, pady=5, padx=5)
        self.win.mainloop()

    def exitAll(self):
        self.win.destroy()
        exit(window)

    def destroyWindow(self):
        self.win.destroy()


class errorWindow():
    def __init__(self, newFolder):
        self.newFolder = newFolder
        self.errWin = Tk()
        self.errWin.wm_title("Unexpected Folder")
        errLbl = Label(self.errWin, text="You are either adding a folder that already exists or one that includes a folder "
                               "that you are already backing up. Are you sure you want to do this?")
        errLbl.pack(side=TOP)
        yesButton = Button(self.errWin, text="Yes, Backup", command=self.backupAnyway)
        yesButton.pack()
        noButton = Button(self.errWin, text="No, Cancel", command=self.destroyWindow)
        noButton.pack()
        self.errWin.mainloop()

    def destroyWindow(self):
        self.errWin.destroy()

    def backupAnyway(self):
        file = open("All_Folders_To_Backup.txt", "a")
        file.write(self.newFolder + "\n")
        file.close()
        self.destroyWindow()

class warningWindow():
    def __init__(self, message="Something is Wrong! (Yell at Craig)"):
        self.warn = Tk()
        self.warn.wm_title("Spagetti Ohs!")
        lbl = Label(self.warn, text=message)
        lbl.grid(padx=5,pady=5)
        ok = Button(self.warn, text="OK", command=self.destroyWindow,padx=15)
        ok.grid(row=1, pady=5)
        self.warn.mainloop()

    def destroyWindow(self):
        self.warn.destroy()



class entryWindow():
    def __init__(self, is2backup, message="What would you like to call the backup folder?"):
        self.b2 = is2backup
        self.noBackup = 0

        self.win = Tk()
        self.win.wm_title("Backup Folder Name")

        self.sVar = StringVar(self.win)
        self.t = time.localtime()
        self.tString = "New Backup ("+str(self.t[1])+"_"+str(self.t[2])+"_"+str(self.t[0])+")"
        self.sVar.set(self.tString)

        lbl = Label(self.win, text=message)
        lbl.grid(padx=5,pady=5, columnspan=2)

        entry = Entry(self.win,textvariable=self.sVar)
        entry.grid(row=1,columnspan=2,ipadx=20, pady=5)

        ok = Button(self.win, text="OK", command=self.okay,padx=20)
        ok.grid(row=2, column=1, pady=5, padx=5)

        cancel = Button(self.win, text="Cancel", command=self.destroyWindow)
        cancel.grid(row=2, column=0, padx=5, ipadx=10)

        self.win.mainloop()

    def makeDirectory(self):
        f = open("Backup_Folder_Location.txt")
        startPath=f.readline()
        f.close()
        self.path = startPath + "/" + self.sVar.get()
        try:
            os.mkdir(self.path)
            if self.b2:
                dirList = os.listdir(startPath)
                for item in dirList:
                    if 'Old Backup' in item:
                        rmPath = startPath + '/' + item
                        shutil.rmtree(rmPath)
                    if 'New Backup' in item and item != self.sVar.get():
                        iPath = startPath + '/' + item
                        item = item.replace('New Backup','Old Backup')
                        nPath = startPath + '/' + item
                        os.rename(iPath,nPath)
        except FileExistsError:
            self.noBackup = 1
            self.win.destroy()
            warningWindow("Backup for today already exists.")

    def execBackup(self):
        rfile = open("All_Folders_To_Backup.txt")
        dneList = []
        for line in rfile:
            line = line[:-1]
            parsedLine = line.split('/')
            fname=parsedLine[-1]
            newPath = self.path + '/' + fname
            if os.path.exists(line):
                print("Backing up: ",line)
                try:
                    shutil.copytree(line,newPath)
                except PermissionError:
                    os.mkdir(newPath)
                    recursiveCopy(line,newPath)
            else:
                dneList.append(line)
        if len(dneList)>0:
            dneString = ''
            for item in dneList:
                dneString = dneString + item +', '
            dneString = dneString[:-2]
            messagebox.showwarning("Folders Not Found!", "No Folders titled '" + dneString + "' were found and will not be backed up.")
        self.win.destroy()
        completeWindow()

    def destroyWindow(self):
        self.win.destroy()

    def okay(self):
        self.makeDirectory()
        if not self.noBackup:
            self.execBackup()
        try:
            self.win.destroy()
        except:
            useless=1


class removeWindow():
    def __init__(self):
        self.rem = Tk()
        self.rem.wm_title("Remove a Folder")
        file = open("All_Folders_To_Backup.txt")
        self.flist = []
        for line in file:
            line = line[:-1]
            self.flist.append(line)
        file.close()
        if len(self.flist) > 0:
            lbl = Label(self.rem, text="Select a folder to remove")
            lbl.grid(columnspan=2,padx=50)
            self.var = StringVar(self.rem)
            self.dropdown = OptionMenu(self.rem,self.var,*self.flist)
            self.var.set('-Select-')
            self.dropdown["width"] = 40
            self.dropdown.grid(row=1,columnspan=2,padx=5)
        else:
            self.lbl2 = Label(self.rem,text="No folders are currently set to be backed up.")
            self.lbl2.grid(row=1,columnspan=2)
        self.ok = Button(self.rem,text="OK", command=self.deleteFolder)
        self.ok.grid(row=2,padx=5,pady=5,ipadx=53)
        self.cancel = Button(self.rem,text="Cancel", command=self.destroyWindow)
        self.cancel.grid(row=2,column=1,padx=5,pady=5,ipadx=43)
        self.rem.mainloop()

    def destroyWindow(self):
        self.rem.destroy()

    def deleteFolder(self):
        if len(self.flist)>0:
            remLine = self.var.get()
            if(os.path.isfile("All_Folders_To_Backup.txt")):
                os.remove("All_Folders_To_Backup.txt")
            file = open("All_Folders_To_Backup.txt", "w")
            for line in self.flist:
                if line != remLine:
                    line = line + "\n"
                    file.write(line)
            file.close()
        self.rem.destroy()





#functions
def recursiveCopy(srcFolderPath,dst):
    flist = os.listdir(srcFolderPath)
    for item in flist:
        lineName = srcFolderPath + '/' + item
        if os.path.isfile(lineName):
            try:
                shutil.copy(lineName,dst)
            except PermissionError:
                printLine = lineName + ' does not have permission to be copied'
                print(printLine)
        elif os.path.isdir(lineName):
            dstname = dst + '/' + item
            try:
                shutil.copytree(lineName,dstname)
            except PermissionError:
                os.mkdir(dstname)
                recursiveCopy(lineName,dstname)

def pickFolder():
    newFolder = filedialog.askdirectory()
    if newFolder not in open("All_Folders_To_Backup.txt").read():
        hidden_file = open("All_Folders_To_Backup.txt", "a")
        hidden_file.write(newFolder + "\n")
        hidden_file.close()
    elif newFolder:
        err = errorWindow(newFolder)

def setBackupLocation():
    backupfolder = filedialog.askdirectory()
    if backupfolder:
        if(os.path.isfile("Backup_Folder_Location.txt")):
            os.remove("Backup_Folder_Location.txt")
        backup = open("Backup_Folder_Location.txt", "w")
        backup.write(backupfolder)
        backup.close()

def copy(src, dst):
    if dst == 200000000000:
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.copyfile(src, dst)

def callBackupWindow(is2backup):
    if(not os.path.isfile("Backup_Folder_Location.txt")):
        w = warningWindow("Please select a backup location")
    else:
        rfile = open("All_Folders_To_Backup.txt")
        nolines = 1
        for line in rfile:
            nolines = 0
            break
        if nolines:
            warningWindow("You are not currently backing up any files!")
        else:
            entryWindow(is2backup)



def removeFolder():
    rf = removeWindow()


def exit(tkWindow):
    tkWindow.destroy()



#GUI
window = Tk()
window.wm_title("Backup Wizard")

#make frames - useless right now
# topframe = Frame(window)
# topframe.pack()
# bottomframe = Frame(window)
# bottomframe.pack(side=BOTTOM)

#label
label = Label(window, text="Backup Wizard", fg = "purple")
label.grid(columnspan=2)

#checkbox variable
iVar = IntVar(window)
iVar.set(1)

#buttons
addFolder = Button(window,text="Add Folder to Backup",command=pickFolder)
addFolder.grid(row=1,padx=5,pady=5)
setBackup = Button(window, text="Set Backup Location", command=setBackupLocation)
setBackup.grid(row=2,padx=5,pady=5,ipadx=3)
runBackup = Button(window, text="Backup Files", command=lambda iVar=iVar: callBackupWindow(iVar))
runBackup.grid(row=2,column=1,padx=5,pady=5,ipadx=21)
removeF = Button(window, text="Remove a Folder", command=removeFolder)
removeF.grid(row=1,column=1,padx=5,pady=5,ipadx=10)

#checkbox
cbox = Checkbutton(window,text="Remove backups prior to last backup?",variable=iVar)
cbox.grid(row=3, columnspan=2)


window.mainloop()





#hide both files
pathname = os.path.abspath("All_Folders_To_Backup.txt")
f = ctypes.windll.kernel32.SetFileAttributesW(pathname,0x02)
pathname = os.path.abspath("Backup_Folder_Location.txt")
b = ctypes.windll.kernel32.SetFileAttributesW(pathname,0x02)


