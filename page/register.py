import tkinter as tk
from tkinter import messagebox
import csv
import os


class RegisterPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.ents = {}
        self.view()

    def view(self):
        # Kiểm tra tiêu đề dựa trên việc có ai đang đăng nhập hay không
        is_admin_logged_in = self.app_manager.current_user is not None
        title = "THÊM TÀI KHOẢN MỚI" if is_admin_logged_in else "ĐĂNG KÝ THÀNH VIÊN"

        tk.Label(self.master, text=title, font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=25)

        # BỎ HOÀN TOÀN Ô "QUYỀN" HOẶC "VAI TRÒ"
        labels = ["User:", "Pass:", "Tên nhân viên:", "SĐT:"]

        form = tk.Frame(self.master)
        form.pack(padx=50, fill="x")

        for i, txt in enumerate(labels):
            tk.Label(form, text=txt, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=12)

            # Ô nhập mật khẩu thì che dấu *
            show_char = "*" if "Pass" in txt else ""
            e = tk.Entry(form, show=show_char, font=("Arial", 11), bd=1, relief="solid")
            e.grid(row=i, column=1, sticky="ew", padx=(10, 0))
            self.ents[txt] = e

        form.columnconfigure(1, weight=1)

        # Nút xác nhận
        btn_confirm = tk.Button(self.master, text="XÁC NHẬN ĐĂNG KÝ", command=self.save,
                                bg="#27ae60", fg="white", font=("Arial", 10, "bold"), height=2)
        btn_confirm.pack(pady=30, fill="x", padx=100)

        # Nút quay lại
        tk.Button(self.master, text="QUAY LẠI", command=self.back, bd=0, fg="gray", cursor="hand2").pack()

    def back(self):
        """Quay lại trang phù hợp"""
        if self.app_manager.current_user:
            self.app_manager.show_quanly_taikhoan_page()
        else:
            self.app_manager.show_login_page()

    def save(self):
        # Lấy dữ liệu từ các ô
        u = self.ents["User:"].get().strip()
        p = self.ents["Pass:"].get().strip()
        name = self.ents["Tên nhân viên:"].get().strip()
        phone = self.ents["SĐT:"].get().strip()

        # KHI ĐĂNG KÝ MỚI, MẶC ĐỊNH LUÔN LÀ "Nhân viên"
        role = "Nhân viên"

        if not u or not p or not name:
            messagebox.showerror("Lỗi", "Vui lòng không để trống các ô thông tin!")
            return

        # Kiểm tra trùng tên đăng nhập
        path = "database/tk.csv"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for r in reader:
                    if len(r) > 0 and r[0] == u:
                        messagebox.showerror("Lỗi", "Tên đăng nhập này đã tồn tại!")
                        return

        # Lưu vào file
        try:
            with open(path, "a", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow([u, p, name, phone, role])

            messagebox.showinfo("Thành công", f"Tài khoản '{u}' đã được tạo.\nVai trò mặc định: Nhân viên")
            self.back()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")