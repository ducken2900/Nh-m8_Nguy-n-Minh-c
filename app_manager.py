import tkinter as tk
from tkinter import ttk
from page.login import LoginPage
from page.menu import MenuPage
from page.register import RegisterPage
from page.taotk import TaoTKPage
from page.quanly_kho import QuanLyKhoPage
from page.quanly_taikhoan import QuanLyTaiKhoanPage
from page.suatk import SuaTKPage
from page.sua_nhanvien import SuaNhanVienPage


class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HỆ THỐNG QUẢN LÝ GUNDAM STORE")
        self.current_page = None
        self.current_user = None

        self.setup_style()
        self.show_login_page()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[('selected', '#3498db')])

    def clear_current_page(self):
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        self.clear_current_page()
        self.root.geometry("450x350")
        self.current_page = LoginPage(self.root, self)

    def show_menu_page(self):
        self.clear_current_page()
        self.root.geometry("450x450")
        self.current_page = MenuPage(self.root, self)

    def show_register_page(self):
        self.clear_current_page()
        self.root.geometry("500x550")
        self.current_page = RegisterPage(self.root, self)

    def show_quanly_kho_page(self):
        self.clear_current_page()
        self.root.geometry("1150x650")
        self.current_page = QuanLyKhoPage(self.root, self)

    def show_quanly_taikhoan_page(self):
        self.clear_current_page()
        self.root.geometry("900x600")
        self.current_page = QuanLyTaiKhoanPage(self.root, self)

    def show_taotk_page(self):
        self.clear_current_page()
        self.root.geometry("500x650")
        self.current_page = TaoTKPage(self.root, self)

    def show_suatk_page(self, data):
        self.clear_current_page()
        self.root.geometry("500x650")
        self.current_page = SuaTKPage(self.root, self, data)

    def show_sua_nhanvien_page(self, data):
        self.clear_current_page()
        self.root.geometry("500x550")
        self.current_page = SuaNhanVienPage(self.root, self, data)

    def run(self):
        self.root.mainloop()