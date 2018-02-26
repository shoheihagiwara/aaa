#!/bin/python3 -*- encoding: utf-8 -*-

import re
import sqlite3

db_filename = 'aaa.db'
def execute_db_query(query, parameters=()):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result

line = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'

if __name__ == "__main__":

    filepath = "test.txt"
    with open(filepath, "r") as file:
        
        filestring= \
            re.sub(r"━━━━━+\n",
                line, file.read())
        
        stringlist = filestring.split(line)
        # sprint(stringlist)
    
    
    for i in range(0,len(stringlist)-1):
        title = stringlist[i].split("◆")[-1]
        try:
            content_title_list = stringlist[i+1].split("◆")
            if len(content_title_list) > 1:
                content = "◆".join(stringlist[i+1].split("◆")[:-1])
            else:
                content = "◆".join(stringlist[i+1].split("◆")[-1:])
        except IndexError:
            exit
        
        # print("title: [" + title + "]\n" + "content: [" + content + "]")
    
        query = "INSERT INTO aaa (title, content) VALUES(?,?);"
        parameters = (title, content)
        execute_db_query(query, parameters)
