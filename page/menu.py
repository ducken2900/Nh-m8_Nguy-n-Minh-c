import tkinter as tk
from common.button import CustomButton

class MenuPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def view(self):
        user = self.app_manager.current_user
        role = user[4]

        tk.Label(self.master, text="MENU HỆ THỐNG", font=("Arial", 22, "bold")).pack(pady=30)
        tk.Label(self.master, text=f"Chào: {user[2]} | Quyền: {role}", font=("Arial", 11, "italic"), fg="#e67e22").pack()

        body = tk.Frame(self.master)
        body.pack(expand=True, fill="both", pady=20)

        CustomButton(body, text="📦 QUẢN LÝ KHO GUNDAM",
                    command=self.app_manager.show_quanly_kho_page, style_type="success").pack(pady=10, ipadx=40)

        # Phân quyền: Chỉ Admin mới vào được Quản trị
        if role == "Quản lý tổng (Admin)" or user[0].lower() in ["admin", "a"]:
            CustomButton(body, text="🛠 QUẢN TRỊ TÀI KHOẢN",
                        command=self.app_manager.show_quanly_taikhoan_page, style_type="primary").pack(pady=10, ipadx=42)

        CustomButton(self.master, text="Đăng xuất",
                    command=self.app_manager.show_login_page, style_type="danger").pack(pady=30)