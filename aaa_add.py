#!/bin/python3 -*- encoding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class aaa_add:
    
    db_filename = 'aaa.db'
    
    def __init__(self, sub_root):
        self.sub_root = sub_root
        self.create_gui()
    
    def create_gui(self):
        
        # ウィンドウサイズに合わせてリサイズするようにする。
        Grid.columnconfigure(self.sub_root, 0, weight=1)
        Grid.columnconfigure(self.sub_root, 0, weight=1)
        Grid.rowconfigure(self.sub_root, 3, weight=1)
        
        Label(sub_root, text="タイトル").grid(row=0, sticky=W, pady=2)
        
        self.title = Entry(sub_root)
        self.title.grid(row=1, sticky=E+W+N)
        
        Label(sub_root, text="内容").grid(row=2, sticky=W, pady=2)
        
        self.content = Text(sub_root)
        self.content.grid(row=3, sticky=E+W+N+S)
        
        ttk.Button(self.sub_root, text="保存", command=self.on_save_clicked).grid(
            row=4)
        
    def on_save_clicked(self):
        query = 'INSERT INTO `aaa` (title, content) VALUES (?,?);'
        parameters = (self.title.get(), self.content.get(1.0, END))
        try:
            self.execute_db_query(query, parameters)
        except Exception as e:
            messagebox.showinfo("error", e)
            return
        messagebox.showinfo("info", "saved!")
        return

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

if __name__ == "__main__":
    sub_root = Tk()
    aaa_add(sub_root)
    sub_root.mainloop()


