import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
import os
from dropbox.files import WriteMode

import dropbox
from tkinter import *




def downloadFile(dbx, path_file, name):
    try:
        path_on_pc = str(tkinter.filedialog.asksaveasfilename(initialfile=name))
        dbx.files_download_to_file(path_on_pc, path_file)
    except:
        print('ne skachalos')
        return False


def uploadFile(dbx, path):
    try:
        path_on_pc = str(tkinter.filedialog.askopenfilename())
        name = path_on_pc.split("/")[-1]

        with open(path_on_pc, "rb") as f:
            dbx.files_upload(f.read(), path + "/" + name, mode=WriteMode('overwrite'))
    except:
        return False


def deleteFile(dbx, path):
    try:
        dbx.files_delete(path)
    except:
        print('ne skachalos')
        return False


def getFolderEntries(dbx, current_path, name):
    try:
        if name != "":
            path = current_path + '/' + name
        else:
            path = current_path
        if "/" in path:
            path = "/" + path

        return dbx.files_list_folder(path).entries
    except:
        print("slomalos")
        return "no"


    