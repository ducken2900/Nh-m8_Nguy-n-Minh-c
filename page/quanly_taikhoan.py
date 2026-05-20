import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from common.button import CustomButton


class QuanLyTaiKhoanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.tree1 = None
        self.tree2 = None
        self.search_user_entry = None  # Biến lưu ô nhập tìm kiếm nhân viên
        self.view()

    def view(self):
        # Tiêu đề chính
        tk.Label(self.master, text="QUẢN TRỊ TÀI KHOẢN & HỆ THỐNG", font=("Arial", 18, "bold"), fg="#2980b9").pack(
            pady=10)

        nb = ttk.Notebook(self.master)
        nb.pack(expand=True, fill="both", padx=10, pady=10)

        # --- TAB 1: DANH SÁCH NHÂN VIÊN ---
        tab_nv = tk.Frame(nb)
        nb.add(tab_nv, text=" 👥 Danh sách nhân viên ")

        # 1.1 Thanh tìm kiếm nhân viên (Mới thêm)
        search_f = tk.Frame(tab_nv, pady=10)
        search_f.pack(fill="x", padx=10)

        tk.Label(search_f, text="🔍 Tìm nhân viên:", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.search_user_entry = tk.Entry(search_f, font=("Arial", 11), bd=1, relief="solid")
        self.search_user_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)

        # Nhấn Enter để tìm ngay
        self.search_user_entry.bind('<Return>', lambda e: self.load_users())

        CustomButton(search_f, text=" Tìm kiếm ", command=self.load_users, style_type="primary").pack(side="left",
                                                                                                      padx=5)

        # 1.2 Thanh công cụ (Nút bấm)
        btn_f = tk.Frame(tab_nv)
        btn_f.pack(pady=5)

        CustomButton(btn_f, text="+ Thêm mới", command=self.app_manager.show_register_page, style_type="success").pack(
            side="left", padx=5)
        CustomButton(btn_f, text="Sửa thông tin", command=self.edit_user, style_type="warning").pack(side="left",
                                                                                                     padx=5)
        CustomButton(btn_f, text="Xóa tài khoản", command=self.delete_user, style_type="danger").pack(side="left",
                                                                                                      padx=5)
        CustomButton(btn_f, text="Làm mới", command=self.refresh_users, style_type="info").pack(side="left", padx=5)

        # 1.3 Bảng nhân viên
        cols1 = ("STT", "User", "HoTen", "SDT", "VaiTro")
        self.tree1 = ttk.Treeview(tab_nv, columns=cols1, show="headings")

        heads1 = ["STT", "Username", "Tên nhân viên", "Số điện thoại", "Vai trò"]
        for c, h in zip(cols1, heads1):
            self.tree1.heading(c, text=h)
            w = 150 if c == "VaiTro" or c == "HoTen" else 100
            self.tree1.column(c, width=w, anchor="center")

        self.tree1.pack(expand=True, fill="both", padx=5, pady=5)
        self.load_users()

        # --- TAB 2: LỊCH SỬ ĐĂNG NHẬP ---
        tab_ls = tk.Frame(nb)
        nb.add(tab_ls, text=" 📜 Lịch sử truy cập ")

        btn_ls_f = tk.Frame(tab_ls)
        btn_ls_f.pack(pady=5)
        CustomButton(btn_ls_f, text="Làm mới lịch sử", command=self.load_history, style_type="info").pack()

        cols2 = ("STT", "User", "Time", "Action")
        self.tree2 = ttk.Treeview(tab_ls, columns=cols2, show="headings")
        for c, h in zip(cols2, ["STT", "Tài khoản", "Thời gian truy cập", "Hành động"]):
            self.tree2.heading(c, text=h)
            self.tree2.column(c, width=180, anchor="center")
        self.tree2.pack(expand=True, fill="both", padx=5, pady=5)
        self.load_history()

        # Nút quay về Menu
        CustomButton(self.master, text="Về Menu chính", command=self.app_manager.show_menu_page,
                     style_type="secondary").pack(pady=10)

    def refresh_users(self):
        """Xóa ô tìm kiếm và nạp lại toàn bộ nhân viên"""
        if self.search_user_entry:
            self.search_user_entry.delete(0, tk.END)
        self.load_users()

    def load_users(self):
        """Tải dữ liệu nhân viên (Có lọc theo tìm kiếm)"""
        if self.tree1 is None: return
        for i in self.tree1.get_children(): self.tree1.delete(i)

        # Lấy từ khóa tìm kiếm
        term = self.search_user_entry.get().lower().strip() if self.search_user_entry else ""

        path = "database/tk.csv"
        if not os.path.exists(path): return

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            count = 1
            for r in reader:
                if len(r) >= 5:
                    # Lọc theo Username (r[0]) hoặc Tên nhân viên (r[2])
                    if not term or (term in r[0].lower() or term in r[2].lower()):
                        self.tree1.insert("", "end", values=(count, r[0], r[2], r[3], r[4]))
                        count += 1

    def load_history(self):
        if self.tree2 is None: return
        for i in self.tree2.get_children(): self.tree2.delete(i)
        path = "database/login_history.csv"
        if not os.path.exists(path): return
        with open(path, "r", encoding="utf-8") as f:
            data = list(csv.reader(f))
            for idx, r in enumerate(reversed(data), 1):
                if len(r) >= 3:
                    self.tree2.insert("", "end", values=(idx, r[0], r[1], r[2]))

    def edit_user(self):
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("!", "Vui lòng chọn nhân viên cần sửa")
            return
        v = self.tree1.item(sel[0], "values")[1]  # Username
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
        if uid.lower() in ["admin", "a"]:
            messagebox.showerror("Lỗi", "Không thể xóa Admin hệ thống")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa tài khoản '{uid}'?"):
            rows = []
            with open("database/tk.csv", "r", encoding="utf-8") as f:
                rows = [r for r in csv.reader(f) if r[0] != uid]
            with open("database/tk.csv", "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
            self.load_users()