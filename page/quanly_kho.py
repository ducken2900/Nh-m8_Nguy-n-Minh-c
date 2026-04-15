import tkinter as tk
from tkinter import messagebox, ttk
import csv, os
from common.button import CustomButton

class QuanLyKhoPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.tree = None
        self.search_entry = None
        self.view()
        self.load_data()

    def view(self):
        header = tk.Frame(self.master, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="DANH MỤC KHO GUNDAM", font=("Arial", 18, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=20, pady=15)

        toolbar = tk.Frame(self.master, bg="white", bd=1, relief="ridge")
        toolbar.pack(fill="x", padx=20, pady=10)

        CustomButton(toolbar, text="🔄 Làm mới", command=self.refresh, style_type="info").pack(side="left", padx=5, pady=5)
        CustomButton(toolbar, text="➕ Nhập hàng", command=self.app_manager.show_taotk_page, style_type="success").pack(side="left", padx=5)
        CustomButton(toolbar, text="📝 Sửa thông tin", command=self.edit_item, style_type="warning").pack(side="left", padx=5)

        # Chỉ Admin mới thấy nút Xóa hàng
        user = self.app_manager.current_user
        if user[0].lower() in ["admin", "a"] or user[4] == "Quản lý tổng (Admin)":
            CustomButton(toolbar, text="🗑 Xóa sản phẩm", command=self.delete_item, style_type="danger").pack(side="left", padx=5)

        CustomButton(toolbar, text="⬅ Về Menu", command=self.app_manager.show_menu_page, style_type="secondary").pack(side="right", padx=10)

        # Search
        search_f = tk.Frame(self.master)
        search_f.pack(fill="x", padx=20, pady=5)
        tk.Label(search_f, text="🔍 Tìm kiếm:").pack(side="left")
        self.search_entry = tk.Entry(search_f, font=("Arial", 11))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.search_entry.bind('<Return>', lambda e: self.load_data())
        CustomButton(search_f, text=" Tìm ", command=self.load_data, style_type="primary").pack(side="left")

        # Table
        tree_f = tk.Frame(self.master)
        tree_f.pack(fill="both", expand=True, padx=20, pady=10)
        cols = ("STT", "Ma", "Ten", "Grade", "SL", "Pre", "Gia", "Ngay", "Status")
        self.tree = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["STT", "Mã", "Tên Gundam", "Grade", "Tồn", "Pre-Order", "Giá", "Ngày", "Tình trạng"]
        for col, h in zip(cols, heads):
            self.tree.heading(col, text=h)
            w = 180 if col == "Ten" else 90
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_f, command=self.tree.yview).pack(side="right", fill="y")

    def refresh(self):
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        term = self.search_entry.get().lower()
        path = "database/kho_hang.csv"
        if not os.path.exists(path): return
        with open(path, "r", encoding="utf-8") as f:
            idx = 1
            for r in csv.reader(f):
                if len(r) >= 8 and (not term or term in r[0].lower() or term in r[1].lower()):
                    self.tree.insert("", "end", values=(idx, *r))
                    idx += 1

    def delete_item(self):
        sel = self.tree.selection()
        if not sel: return
        mid = self.tree.item(sel[0], "values")[1]
        if messagebox.askyesno("?", f"Xóa {mid}?"):
            rows = []
            with open("database/kho_hang.csv", "r", encoding="utf-8") as f:
                rows = [r for r in csv.reader(f) if r[0] != mid]
            with open("database/kho_hang.csv", "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
            self.load_data()

    def edit_item(self):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        self.app_manager.show_suatk_page(v[1:])