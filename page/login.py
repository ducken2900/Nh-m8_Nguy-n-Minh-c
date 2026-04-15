import tkinter as tk
from tkinter import messagebox
import csv, os
from datetime import datetime
from common.button import CustomButton


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def view(self):
        header = tk.Frame(self.master, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="GUNDAM STORE", font=("Arial", 22, "bold"), fg="white", bg="#2c3e50").pack(pady=20)

        form = tk.Frame(self.master)
        form.pack(pady=20, padx=50, fill="both")

        tk.Label(form, text="Tên đăng nhập").pack(anchor="w")
        self.e_u = tk.Entry(form, font=("Arial", 12))
        self.e_u.pack(fill="x", pady=5)
        self.e_u.focus()

        tk.Label(form, text="Mật khẩu").pack(anchor="w")
        self.e_p = tk.Entry(form, font=("Arial", 12), show="*")
        self.e_p.pack(fill="x", pady=5)

        # Sửa lỗi Enter (Bind vào Entry)
        self.e_u.bind('<Return>', lambda e: self.login())
        self.e_p.bind('<Return>', lambda e: self.login())

        self.var_show = tk.IntVar()
        tk.Checkbutton(form, text="Hiện mật khẩu", variable=self.var_show, command=self.toggle).pack(anchor="w")

        btn_f = tk.Frame(self.master)
        btn_f.pack(pady=10)
        CustomButton(btn_f, text=" ĐĂNG NHẬP ", command=self.login, style_type="success").pack(side="left", padx=10)
        CustomButton(btn_f, text=" ĐĂNG KÝ ", command=self.app_manager.show_register_page, style_type="primary").pack(
            side="left")

    def toggle(self):
        if self.e_p.winfo_exists():
            self.e_p.config(show="" if self.var_show.get() == 1 else "*")

    def login(self):
        if not self.e_u.winfo_exists(): return
        u, p = self.e_u.get().strip(), self.e_p.get().strip()
        path = "database/tk.csv"
        if not os.path.exists(path): return messagebox.showerror("Lỗi", "Chưa có file tk.csv")

        try:
            with open(path, "r", encoding="utf-8") as f:
                for r in csv.reader(f):
                    if len(r) >= 2 and u == r[0] and p == r[1]:
                        while len(r) < 5: r.append("Nhân viên")
                        self.app_manager.current_user = r
                        with open("database/login_history.csv", "a", encoding="utf-8", newline="") as h:
                            csv.writer(h).writerow([u, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Thành công"])
                        self.app_manager.show_menu_page()
                        return
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))