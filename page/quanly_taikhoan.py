import tkinter as tk
from tkinter import messagebox, ttk
import csv, os
from common.button import CustomButton


class QuanLyTaiKhoanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.tree1 = None
        self.tree2 = None
        self.view()

    def view(self):
        tk.Label(self.master, text="QUẢN TRỊ HỆ THỐNG", font=("Arial", 18, "bold"), fg="#2980b9").pack(pady=10)
        nb = ttk.Notebook(self.master)
        nb.pack(expand=True, fill="both", padx=10, pady=5)
        toolbar = tk.Frame(self.master, bg="white", bd=1, relief="ridge")
        toolbar.pack(fill="x", padx=20, pady=10)

        # Tab Nhân viên
        t1 = tk.Frame(nb);
        nb.add(t1, text=" Danh sách nhân viên ")
        btn_f = tk.Frame(t1, bg="#f8f9fa", bd=1, relief="ridge");
        btn_f.pack(fill="x", padx=10, pady=(10, 0))
        CustomButton(btn_f, text="+ Thêm NV mới", command=self.app_manager.show_register_page,style_type="success").pack(side="left",
                                                                                                                         padx=5,pady=5)
        CustomButton(btn_f, text="📝 Sửa thông tin", command=self.edit_user, style_type="warning").pack(side="left",
                                                                                                      padx=5, pady=5)
        CustomButton(btn_f, text="🗑 Xóa tài khoản", command=self.delete_user, style_type="danger").pack(side="left",
                                                                                                      padx=5, pady=5)
        CustomButton(self.master, text="⬅ Về Menu", command=self.app_manager.show_menu_page, style_type="secondary").pack(side="right", padx=10,
                                                                                                      pady=5,)

        tree_container = tk.Frame(t1)
        tree_container.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        cols1 = ("STT", "User", "HoTen", "SDT", "VaiTro")
        self.tree1 = ttk.Treeview(t1, columns=cols1, show="headings")
        for c, h in zip(cols1, ["STT", "User", "Họ tên", "SĐT", "Vai trò"]):
            self.tree1.heading(c, text=h);
            self.tree1.column(c, width=150, anchor="center")
        self.tree1.pack(expand=True, fill="both", padx=5);
        self.load_users()

        # Tab Lịch sử
        t2 = tk.Frame(nb);
        nb.add(t2, text=" Lịch sử đăng nhập ")
        self.tree2 = ttk.Treeview(t2, columns=("STT", "User", "Time", "Action"), show="headings")
        for c, h in zip(("STT", "User", "Time", "Action"), ["STT", "Tài khoản", "Thời gian", "Hành động"]):
            self.tree2.heading(c, text=h);
            self.tree2.column(c, width=200, anchor="center")
        self.tree2.pack(expand=True, fill="both", padx=5);
        self.load_history()


    def load_users(self):
        for i in self.tree1.get_children(): self.tree1.delete(i)
        if not os.path.exists("database/tk.csv"): return
        with open("database/tk.csv", "r", encoding="utf-8") as f:
            for idx, r in enumerate(csv.reader(f), 1):
                if len(r) >= 5: self.tree1.insert("", "end", values=(idx, r[0], r[2], r[3], r[4]))

    def load_history(self):
        for i in self.tree2.get_children(): self.tree2.delete(i)
        if not os.path.exists("database/login_history.csv"): return
        with open("database/login_history.csv", "r", encoding="utf-8") as f:
            for idx, r in enumerate(reversed(list(csv.reader(f))), 1):
                self.tree2.insert("", "end", values=(idx, *r))

    def edit_user(self):
        sel = self.tree1.selection()
        if not sel: return
        v = self.tree1.item(sel[0], "values")[1]
        path = "database/tk.csv"
        with open(path, "r", encoding="utf-8") as f:
            for r in csv.reader(f):
                if r[0] == v:
                    self.app_manager.show_sua_nhanvien_page(r)
                    return

    def delete_user(self):
        sel = self.tree1.selection()
        if not sel: return
        uid = self.tree1.item(sel[0], "values")[1]
        if uid.lower() in ["admin", "a"]: return
        if messagebox.askyesno("?", f"Xóa {uid}?"):
            rows = []
            with open("database/tk.csv", "r", encoding="utf-8") as f:
                rows = [r for r in csv.reader(f) if r[0] != uid]
            with open("database/tk.csv", "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
            self.load_users()