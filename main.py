import textwrap
import tkinter.messagebox
import DropboxOps
from DropboxOps import *
import dropbox
from tkinter import *
import sys


if __name__ == '__main__':
    try:
        dbx = dropbox.Dropbox('sl.BouwSdTVQ2TX-rkE0qcuig3z9NW6xBsaWUKgzfPTUw7gMwn2yDUoX94BtsyQXsSqmaZosYyLJbQPO8glZ7nyhYH4EjtSJHOiLwk6QfPgQwsrYw3ICmCKfDUxsdiYoHnjwPPfSwUKVNAF5Rs')
    except:
        tkinter.messagebox.showinfo(title="Ошибка!", message="Токен больше не актуален!")
        sys.exit()

    root = Tk()
    root.title("Dropbox Python Client")
    root.geometry("600x600")
    root.iconbitmap("icon.ico")

    current_directory = ""

    directory_list = Listbox(root, width=50, height=10)
    directory_list.grid(row=0, column=0, columnspan=6, pady=10)

    for entry in dbx.files_list_folder('').entries:
        directory_list.insert(END, entry.name)

    def changeDirectory():
        global directory_list
        global current_directory

        path = getSelection(directory_list)

        if path == "...":
            directory_back = current_directory.split("/")
            directory_back.pop()
            current_directory = "/".join(directory_back)
            path = ""

        if getFolderEntries(dbx, current_directory, path) != "no":
            directory_list.delete(0, END)
            if current_directory + "/" + path != "/":
                directory_list.insert(END, "...")
            for value in getFolderEntries(dbx, current_directory, path):
                directory_list.insert(END, value.name)
            current_directory += "/" + path
            if len(current_directory) > 0:
                if current_directory[-1] == "/":
                    current_directory = current_directory[:-1]


    def getSelection(list_box):
        values = list_box.curselection()
        if values:
            index = values[0]
            val = list_box.get(index)
            return val


    def preDownloading():
        global current_directory
        global directory_list
        global dbx

        if getSelection(directory_list):
            path = current_directory + "/" + getSelection(directory_list)
            DropboxOps.downloadFile(dbx, path, getSelection(directory_list))
        else:
            tkinter.messagebox.showinfo(title="Ошибка!", message="Не выбран файл!")


    def preUpload():
        global current_directory
        global dbx

        try:
            DropboxOps.uploadFile(dbx, current_directory)
            tkinter.messagebox.showinfo(title="Успешно!", message="Файл был успешно загружен!")
        except:
            tkinter.messagebox.showinfo(title="Ошибка!", message="Ошибка при загрузке файла!")


    def preDelete():
        global current_directory
        global directory_list
        global dbx

        if getSelection(directory_list):
            path = current_directory + "/" + getSelection(directory_list)
            DropboxOps.deleteFile(dbx, path)
            tkinter.messagebox.showinfo(title="Успешно!", message="Файл удалён!")
        else:
            tkinter.messagebox.showinfo(title="Ошибка!", message="Не выбран файл!")


    def Info():
        global current_directory
        global directory_list
        global dbx

        if getSelection(directory_list):
            path = current_directory + "/" + getSelection(directory_list)
            string = str(dbx.files_get_metadata(path))
            tkinter.messagebox.showinfo(title="Успешно!", message=string)
        else:
            tkinter.messagebox.showinfo(title="Ошибка!", message="Не выбран файл!")


    def refreshDirectory():
        global current_directory
        global dbx
        global directory_list

        directory_list.delete(0, END)
        for value in getFolderEntries(dbx, current_directory, current_directory):
            directory_list.insert(END, value.name)


    def share():
        global current_directory
        global dbx

        try:
            shared_link = dbx.sharing_create_shared_link(current_directory)
            tkinter.messagebox.showinfo(title="Успешно!", message="Вы поделились директорией " + current_directory +
                                                          "\n" + "Ссылка: " + shared_link.url)
        except:
            tkinter.messagebox.showinfo(title="Ошибка!", message="Не удалось поделиться директорией!")


    def showUserInfo():
        global dbx

        data = dbx.users_get_current_account()

        tkinter.messagebox.showinfo(title="Информация о пользователе", message="user_id: " + data.account_id + "\n"
                                                                               "email: " + data.email + "\n"
                                                                               "name: " + data.name.display_name + "\n"
                                                                                "country: " + data.country + "\n"
                                                                                "locale: " + data.locale)


    button_info = Button(root, text="Info", width=18, height=2, command=Info)
    button_info.grid(row=5, column=0, pady=10)

    button_folder = Button(root, text="Open folder", width=18, height=2,
                           command=changeDirectory)
    button_folder.grid(row=5, column=1, pady=10)

    button_folder = Button(root, text="Share directory", width=18, height=2, command=share)
    button_folder.grid(row=5, column=2, pady=10)

    button_folder = Button(root, text="Delete this file", width=18, height=2, command=preDelete)
    button_folder.grid(row=5, column=3, pady=10)

    button_folder = Button(root, text="Upload file to here", width=18, height=2, command=preUpload)
    button_folder.grid(row=6, column=0, pady=10)

    button_folder = Button(root, text="Download this file", width=18, height=2, command=preDownloading)
    button_folder.grid(row=6, column=1, pady=10)

    button_folder = Button(root, text="Refresh", width=18, height=2, command=refreshDirectory)
    button_folder.grid(row=7, column=0, pady=10)

    button_folder = Button(root, text="User info", width=18, height=2, command=showUserInfo)
    button_folder.grid(row=8, column=0, pady=10)

    # label_main = Label(text="User information: ", font=("Helvetica", 18, "bold"), width=18, height=2)
    # label_main.grid(row=8, column=0)
    # label_main = Label(text="Nickname: " + str(dbx.users_get_current_account().name))
    # label_main.grid(row=9, column=1)
    # label_nickname = Label(text= "Email: " + dbx.users_get_current_account().email)
    # label_nickname.grid(row=10, column=1)

    print(dbx.users_get_current_account())

    root.mainloop()
