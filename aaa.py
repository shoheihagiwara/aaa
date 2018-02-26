#!/bin/python3 -*- encoding: utf-8 -*-

#import tkinter
from tkinter import *
from tkinter import ttk   # 「from tkinter import *」はモジュールはインポートしないみたい。なのでこの行がないとttkモジュール内のクラスなどは使えなくない。

import sqlite3
import random
import re


db_filename = 'aaa.db'
def execute_db_query(query, parameters=()):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result


'''仕事に必要な情報を簡単に探し出せるアプリケーション
'''
class aaa:

    
    def __init__(self, root):
        self.root = root
        self.create_gui()

    def configure(self, event):
        
        self.result_area.config(scrollregion=self.innerFrame.bbox(ALL))


    def create_gui(self):
        
        # ウィンドウサイズに合わせてリサイズするようにする。
        # このアプリは2つの部分からなる。
        #
        #      column=0
        #┌───────┐
        #│┌─────┐│
        #││  検索部  ││ row=0
        #│└─────┘│上下には伸縮しない。左右にはする
        #│              │
        #│┌─────┐│
        #││          ││
        #││  結果部  ││ row=1
        #││          ││上下左右に伸縮する。
        #│└─────┘│
        #└───────┘
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=3)
        
        # 検索部を作成
        self.create_search_area()
        
        # 結果部を作成
        self.create_search_result_area()

    def create_search_area(self):
        
        # 検索部の構造は以下のとおり。
        #
        #    column=0      column=1        column=2       column=3
        # ┌──────────────────────────────┐
        # │┌───┐┌────────┐┌───┐┌────────┐│
        # ││ラベル││テキスト        ││ラベル││スクロールバー  ││ row=0
        # │└───┘└────────┘└───┘└────────┘│
        # └─────────────↑───────────│────┘
        #   ↑                        └───────────┘
        #   これはLabelFrame           スクロールバーは
        #                              テキストに連動する。
        
        # LabelFrame
        labelframe = LabelFrame(self.root, text="検索条件")
        labelframe.grid(row=0, column=0, padx=8, pady=8, sticky=W+E+N+S)

        # ラベル
        Label(labelframe, text='キーワード:').grid(row=0, column=0, sticky=N, pady=2)

        # スクロールバー
        scrollbar = Scrollbar(labelframe)
        scrollbar.grid(row=0, column=3, sticky=N+S+E)

        # キーワードのテキストボックス
        self.keywordfield = Text(labelframe, yscrollcommand = scrollbar.set, height=10)
        self.keywordfield.grid(row=0, column=1, sticky=W+E+S+N, padx=5, pady=2)

        
        #スクロールバーでテキストが動くようにする設定
        scrollbar.config(command=self.keywordfield.yview)
        
        # 検索ボタン
        ttk.Button(labelframe, text='検索', command=self.on_search_button_clicked).grid(
            row=0, column=2, sticky=S, padx=5, pady=2)
        
        # キーワードのテキストボックスをウィンドウサイズに合わせてリサイズするようにする。
        Grid.columnconfigure(labelframe, 1, weight=1)
        Grid.rowconfigure(labelframe, 0, weight=1)

    def setupInnerFrame(self, canvas):
        
        innerFrame = LabelFrame(canvas, text="インナーフレーム", bg="green")
        return innerFrame


    def create_search_result_area(self):
        
        # 検索部の一番の親を設定。ここにテキストとスクロールをつけていく。
        self.outerFrame = LabelFrame(self.root, text="結果部")
        self.outerFrame.grid(row=1, column=0, padx=8, pady=8, sticky=N+E+W+S)
        
        # テキスト部分
        self.text = Text(self.outerFrame)
        self.text.grid(row=0, column=0, sticky=N+E+W+S)

        # スクロールバー
        scrollbar = Scrollbar(self.outerFrame)
        scrollbar.grid(row=0, column=1, sticky=N+S+E)

        # スクロールの連携の設定
        scrollbar.config(command = self.text.yview)
        self.text.config(yscrollcommand =  scrollbar.set)
        
        Grid.columnconfigure( self.outerFrame, 0, weight=10000)
        Grid.columnconfigure( self.outerFrame, 1, weight=1)
        Grid.rowconfigure(    self.outerFrame, 0, weight=1)



        
        ## 検索部の一番の親を設定。ここにキャンバスとスクロールをつけていく。名前をアウターフレームとする。
        #self.outerFrame = LabelFrame(self.root, text="アウターフレーム")
        #self.outerFrame.grid(row=1, column=0, padx=8, pady=8, sticky=N+E+W+S)
        #
        ##キャンバス。ここに結果のラベルを足していく。
        #self.result_area = Canvas(self.outerFrame, bg='red',)
        #self.result_area.grid(row=0, column=0, sticky=N+E+W+S)
        #self.result_area.bind("<Configure>", self.configure)
        #
        ## インナーフレーム
        #self.innerFrame = self.setupInnerFrame(self.result_area)
        #self.innerFrame.grid(row=0, column=0, sticky=N+E+W+S)
        #
        ## キャンバスにフレームを足す
        #print(self.outerFrame.winfo_rootx())
        #print(self.outerFrame.winfo_rooty())
        #self.result_area.create_window(50, 1200, window=self.innerFrame)
        #
        ## スクロールバー
        #scrollbar = Scrollbar(self.outerFrame)
        #scrollbar.grid(row=0, column=1, sticky=N+S+E)
        #
        ## スクロールの連携の設定
        #scrollbar.config(command = self.result_area.yview)
        #self.result_area.config(yscrollcommand =  scrollbar.set)
        #
        #Grid.columnconfigure( self.outerFrame, 0, weight=10000)
        #Grid.columnconfigure( self.outerFrame, 1, weight=1)
        #Grid.rowconfigure(    self.outerFrame, 0, weight=1)
        #
        #Grid.columnconfigure( self.result_area, 0, weight=1)
        #Grid.rowconfigure(    self.result_area, 0, weight=1)
        #
        #self.result_area.config(scrollregion=self.innerFrame.bbox(ALL))



        
        #self.result_area = LabelFrame(self.root)
        #self.result_area.grid(row=1, padx=8, sticky=W+E+S+N)
        #Grid.columnconfigure(self.result_area, 0, weight=1)
        #
        ## リストボックス
        #self.listbox = Listbox(self.result_area)
        #self.listbox.grid(row=0, column=0, sticky=N+E+W+S)
        #
        ## スクロールバー
        #scrollbar = Scrollbar(self.result_area)
        #scrollbar.grid(row=0, column=1, sticky=N+S+E)
        #scrollbar.config(command=self.listbox.yview)
        #
        #self.listbox.config(yscrollcommand =  scrollbar.set)
        #
        ##self.result_area = LabelFrame(self.root)
        ##self.result_area.grid(row=1, padx=8, sticky=W+E+S+N)
        ##Grid.columnconfigure(self.result_area, 0, weight=1)
        ### self.tree.bind("<Double-1>", self.on_title_double_clicked)
        ##
        ### スクロールバーの設定
        ##scrollbar = Scrollbar(self.result_area)
        ##scrollbar.grid(row=0, column=1, sticky=N+S+E)
        ##scrollbar.config(command=self.result_area.yview)
        ##self.result_area.config(yscrollcommand=scrollbar.set)


    def on_title_double_clicked(self, event):
        sub_win = Toplevel()
        # print(values)
        aaa_add(sub_win, event.widget.id)

    def on_search_button_clicked(self):
        self.view_records()

    def view_records(self):

        self.create_search_result_area()
        
        query = 'SELECT title, content, id FROM aaa ORDER BY title'
        entries = execute_db_query(query)
        entries = self.order_by_fit_value(entries)
        row_index = 0
        for row in reversed(entries):
            title, content, id = row[0], row[1], row[3]
            
            # そのまま表示すると見にくいので、改行はスペースに置き換える。
            title   = re.sub('\r\n|\n', '  ', title)
            content = re.sub('\r\n|\n', '  ', content)
            
            self.text.insert(END, "◆" + title + "\n")
            self.text.insert(END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            self.text.insert(END, content)
            self.text.insert(END, "\n\n\n")
            
            
            #Label(self.result_area, text=title).grid()
            #Label(self.result_area, text=content).grid()

            #self.innerFrame.insert(END, title)
            #self.listbox.insert(END, content[:100])
            #self.listbox.insert(END, "")
            
            
            
            
            #title_label = Label(self.result_area, text=title, anchor=W)
            #title_label.grid(row=row_index, column = 0, sticky=E+W+S+N)
            #title_label.config(font=('Verdana', 16, 'underline'), fg="blue", justify="left", )
            #title_label.id = row[3]
            #print(row)
            #title_label.bind("<Double-1>", self.on_title_double_clicked)
            ## Grid.rowconfigure(self.result_area, row_index, weight=1)
            #
            #content_label = Label(self.result_area, text=content[:80], anchor=W)
            #content_label.grid(row=row_index+1, column=0, sticky=E+W+S+N, pady=10)
            #content_label.config(justify="left")
            #
            ## Grid.rowconfigure(self.result_area, row_index+1, weight=1)
            #
            #row_index = row_index + 2
            
    
        # items = self.tree.get_children()
        # for item in items:
        #     self.tree.delete(item)
        # query = 'SELECT title, content, id FROM aaa ORDER BY title'
        # entries = execute_db_query(query)
        # entries = self.order_by_fit_value(entries)
        # for row in entries[:20]:
        #     self.tree.insert('', 0, text=row[0], values=(row[1],row[2], row[3]))



    def order_by_fit_value(self, entries):
        
        new_entries = []
        for row in entries:
            element = []
            element.append(row[0])
            element.append(row[1])
            element.append(self.get_fitvalue(row[0], row[1]))
            element.append(row[2])
            new_entries.append(element)
        
        new_entries = sorted(new_entries, key=lambda element: element[2])
        
        return new_entries
        

    def get_fitvalue(self, title, content):
        
        fvalue_title   = self.calc_fvalue_title(title)
        fvalue_content = self.calc_fvalue_content(content)
        fvalue = fvalue_title + fvalue_content
        
        return fvalue
        
    def calc_fvalue_title(self, title):
        return 20 * self.calc_fvalue(title)
    
    def calc_fvalue_content(self, title):
        return self.calc_fvalue(title)

    def calc_fvalue(self, string):
        
        count = 0
        keywords = re.sub(" +", " ", self.keywordfield.get("0.0"))
        keywords = re.sub("\n", " ", keywords)

        for keyword in keywords.split(" "):
            count += string.count(keyword)

        return count

class aaa_add:
    
    def __init__(self, sub_root, id):
        self.sub_root = sub_root
        self.create_gui()
        self.set_values_to_gui(id)
    
    def set_values_to_gui(self, id):
        query = 'SELECT title, content, id FROM aaa WHERE id = ? ORDER BY title'
        print(id)
        entries = execute_db_query(query, [id])
        for entry in entries:
            self.title.insert(END, entry[0])
            self.content.insert(END, entry[1])
            self.id = entry[2]
    
    def create_gui(self):
        
        # ウィンドウサイズに合わせてリサイズするようにする。
        Grid.columnconfigure(self.sub_root, 0, weight=1)
        Grid.rowconfigure(self.sub_root, 3, weight=1)
        
        Label(self.sub_root, text="タイトル").grid(row=0, sticky=W, pady=2)
        
        self.title = Entry(self.sub_root)
        self.title.grid(row=1, sticky=E+W+N)
        
        Label(self.sub_root, text="内容").grid(row=2, sticky=W, pady=2)
        
        self.content = Text(self.sub_root)
        self.content.grid(row=3, sticky=E+W+N+S)
        
        ttk.Button(self.sub_root, text="保存", command=self.on_save_clicked).grid(
            row=4)
        
    def on_save_clicked(self):
        if hasattr(self, "id"):
            query = 'UPDATE `aaa` SET title = ?, content = ? WHERE id = ?;'
            parameters = (self.title.get(), self.content.get(1.0, END), self.id)
        else:
            query = 'INSERT INTO `aaa` (title, content) VALUES (?,?);'
            parameters = (self.title.get(), self.content.get(1.0, END))
        try:
            execute_db_query(query, parameters)
        except Exception as e:
            messagebox.showinfo("error", e)
            return
        messagebox.showinfo("info", "saved!")
        self.sub_root.focus()
        self.sub_root.destroy()
        return

class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return





if __name__ == '__main__':
    root = Tk()
    aaa(root)
    root.mainloop()


