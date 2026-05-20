import tkinter as tk
from common.button import CustomButton


class MenuPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def view(self):
        user = self.app_manager.current_user
        name = user[2]
        role = user[4]  # Cột Vai trò (Admin/Nhân viên)

        tk.Label(self.master, text="MENU QUẢN LÝ", font=("Arial", 24, "bold"), fg="#2c3e50").pack(pady=30)

        # Khung thông tin người dùng
        info_frame = tk.Frame(self.master, bg="#ecf0f1", padx=20, pady=10)
        info_frame.pack(fill="x", padx=50)
        tk.Label(info_frame, text=f"Nhân viên: {name}", font=("Arial", 11, "bold"), bg="#ecf0f1").pack()
        tk.Label(info_frame, text=f"Quyền hạn: {role}", font=("Arial", 10), fg="#e67e22", bg="#ecf0f1").pack()

        body = tk.Frame(self.master)
        body.pack(expand=True, fill="both", pady=20)

        # 1. NÚT KHO HÀNG: Tất cả mọi người đều thấy
        CustomButton(body, text="📦 QUẢN LÝ KHO GUNDAM",
                     command=self.app_manager.show_quanly_kho_page, style_type="success").pack(pady=10, ipadx=50)

        # 2. PHẦN DÀNH RIÊNG CHO QUẢN TRỊ (ADMIN)
        if role == "Quản lý tổng (Admin)" or user[0].lower() in ["admin", "a"]:
            # Nút Quản trị nhân viên
            CustomButton(body, text="🛠 QUẢN TRỊ NHÂN VIÊN",
                         command=self.app_manager.show_quanly_taikhoan_page, style_type="primary").pack(pady=10,
                                                                                                        ipadx=55)

            # Nút Báo cáo & Doanh thu (Mới thêm)
            CustomButton(body, text="📊 BÁO CÁO & DOANH THU",
                         command=self.app_manager.show_baocao_page, style_type="info").pack(pady=10, ipadx=52)
        else:
            # Nếu là nhân viên thường, hiện thông báo nhỏ
            tk.Label(body, text="(Tài khoản nhân viên - Chế độ hạn chế)",
                     font=("Arial", 9, "italic"), fg="gray").pack(pady=10)

        # 3. NÚT ĐĂNG XUẤT
        CustomButton(self.master, text="Đăng xuất",
                     command=self.app_manager.show_login_page, style_type="danger").pack(pady=30)