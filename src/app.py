#!/usr/bin/env python3
"""
sql-query-tool - SQL查询工具
工具编号: tool-036
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class App:
    def __init__(self, root):
        self.root = root
        root.title("SQL查询工具 v1.0")
        root.geometry("900x700")
        self.data_file = None
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#FF9800", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="📊 SQL查询工具", font=("Arial", 18, "bold"),
                 fg="white", bg="#FF9800").pack(pady=15)
        
        # 主区域
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        
        # 文件选择
        file_frame = tk.Frame(main)
        file_frame.pack(fill="x", pady=10)
        
        tk.Label(file_frame, text="📁 数据文件:", font=("Arial", 10, "bold")).pack(side="left")
        self.file_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_var, width=40).pack(side="left", padx=10)
        tk.Button(file_frame, text="浏览", command=self.browse_file,
                  bg="#FF9800", fg="white").pack(side="left")
        
        # 数据预览区
        preview_frame = tk.LabelFrame(main, text="📋 数据预览", font=("Arial", 10, "bold"))
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        # 创建表格
        columns = ("col1", "col2", "col3", "col4", "col5")
        self.tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=120)
        
        scrollbar_y = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # 操作按钮
        btn_frame = tk.Frame(main)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="🔄 刷新数据", command=self.load_data,
                  bg="#2196F3", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💾 导出结果", command=self.export_data,
                  bg="#4CAF50", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🧹 清洗数据", command=self.clean_data,
                  bg="#9C27B0", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        
        # 状态
        self.status_var = tk.StringVar(value="就绪 - 请选择数据文件")
        tk.Label(main, textvariable=self.status_var, fg="gray").pack(fill="x")
    
    def browse_file(self):
        file = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[("所有数据文件", "*.csv *.xlsx *.xls *.json *.xml"),
                       ("CSV文件", "*.csv"),
                       ("Excel文件", "*.xlsx *.xls"),
                       ("JSON文件", "*.json")]
        )
        if file:
            self.file_var.set(file)
            self.data_file = file
            self.load_data()
    
    def load_data(self):
        if not self.data_file:
            return
        
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 模拟加载数据
        sample_data = [
            ("数据1", "数据2", "数据3", "数据4", "数据5"),
            ("A1", "B1", "C1", "D1", "E1"),
            ("A2", "B2", "C2", "D2", "E2"),
        ]
        
        for row in sample_data:
            self.tree.insert("", tk.END, values=row)
        
        self.status_var.set(f"✅ 已加载: {Path(self.data_file).name}")
    
    def export_data(self):
        messagebox.showinfo("提示", "数据导出功能")
    
    def clean_data(self):
        messagebox.showinfo("提示", "数据清洗功能")

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
