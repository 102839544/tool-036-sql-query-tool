#!/usr/bin/env python3
"""
SQL查询工具 - 可视化SQL执行器（SQLite）
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import sqlite3

class App:
    def __init__(self, root):
        self.root = root
        root.title("SQL查询工具 v1.0")
        root.geometry("900x650")
        self.conn = None
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#5d4037", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🗃️ SQL查询工具", font=("Arial",14,"bold"),
                 fg="white", bg="#5d4037").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 数据库控制
        cf = tk.Frame(main)
        cf.pack(fill="x", pady=5)
        tk.Button(cf, text="打开SQLite数据库", command=self.open_db,
                  bg="#5d4037", fg="white", padx=12).pack(side="left", padx=5)
        tk.Button(cf, text="新建数据库", command=self.new_db,
                  padx=12).pack(side="left", padx=5)
        tk.Button(cf, text="执行SQL", command=self.execute_sql,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=15).pack(side="left", padx=20)
        
        self.db_label = tk.Label(cf, text="未加载数据库", fg="gray")
        self.db_label.pack(side="right")
        
        # 表列表
        lf = tk.Frame(main)
        lf.pack(fill="x", pady=5)
        tk.Label(lf, text="表：").pack(side="left")
        self.tables_lb = tk.Listbox(lf, height=3, width=40)
        self.tables_lb.pack(side="left", padx=5)
        self.tables_lb.bind("<<ListboxSelect>>", self.show_schema)
        
        # SQL输入
        tk.Label(main, text="SQL语句：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,2))
        self.sql_txt = tk.Text(main, height=5, font=("Consolas",11),
                               bg="#fff8e1", bd=2, relief="groove")
        self.sql_txt.pack(fill="x", pady=5)
        self.sql_txt.insert(1.0, "SELECT * FROM sqlite_master WHERE type='table'")
        
        # 结果表格
        tk.Label(main, text="查询结果：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,2))
        self.tree = ttk.Treeview(main, show="headings", height=12)
        self.tree.pack(fill="both", expand=True)
        
        sb = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        self.status = tk.Label(main, text="打开或新建SQLite数据库开始",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def open_db(self):
        f = filedialog.askopenfilename(title="选择SQLite数据库",
             filetypes=[("SQLite","*.db *.sqlite *.sqlite3")])
        if f:
            self.connect_db(f)
    
    def new_db(self):
        f = filedialog.asksaveasfilename(title="新建SQLite数据库",
             defaultextension=".db", filetypes=[("SQLite","*.db")])
        if f:
            self.connect_db(f)
    
    def connect_db(self, path):
        try:
            if self.conn:
                self.conn.close()
            self.conn = sqlite3.connect(path)
            self.db_path = path
            self.db_label.config(text=Path(path).name)
            # 加载表列表
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.tables_lb.delete(0, "end")
            for t in tables:
                self.tables_lb.insert("end", t)
            self.status.config(text=f"✅ 已连接：{Path(path).name}")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def show_schema(self, event=None):
        sel = self.tables_lb.curselection()
        if sel:
            table = self.tables_lb.get(sel[0])
            self.sql_txt.delete(1.0, "end")
            self.sql_txt.insert(1.0, f"SELECT * FROM {table} LIMIT 100")
    
    def execute_sql(self):
        if not self.conn:
            messagebox.showwarning("提示", "请先打开数据库")
            return
        sql = self.sql_txt.get(1.0, "end").strip()
        if not sql:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            
            # 清除旧数据
            for c in self.tree["columns"]:
                self.tree.heading(c, text="")
            self.tree.delete(*self.tree.get_children())
            
            if cursor.description:
                cols = [d[0] for d in cursor.description]
                self.tree["columns"] = cols
                for c in cols:
                    self.tree.heading(c, text=c)
                    self.tree.column(c, width=100)
                
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", "end", values=row)
                
                self.status.config(text=f"✅ 返回 {len(rows)} 行")
            else:
                self.conn.commit()
                self.status.config(text=f"✅ 执行成功（{cursor.rowcount} 行受影响）")
        except Exception as e:
            messagebox.showerror("SQL错误", str(e))
            self.status.config(text="❌ 执行失败")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
