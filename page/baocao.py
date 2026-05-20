import tkinter as tk
from tkinter import ttk
import csv
import os
from common.button import CustomButton


class BaoCaoPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def view(self):
        tk.Label(self.master, text="BÁO CÁO CHI TIẾT CỬA HÀNG", font=("Arial", 20, "bold"), fg="#2c3e50").pack(pady=20)

        # Container chứa các con số tổng quát
        stat_frame = tk.LabelFrame(self.master, text=" Tổng quan tài chính (Ước tính) ", font=("Arial", 10, "bold"),
                                   padx=20, pady=20)
        stat_frame.pack(fill="x", padx=40)

        # Tính toán dữ liệu
        total_qty, total_value, total_pre, grade_count = self.calculate_stats()

        # Hiển thị các con số
        tk.Label(stat_frame, text=f"📦 Tổng số lượng Gundam trong kho: {total_qty} hộp", font=("Arial", 11)).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky="w",
                                                                                                                 pady=5)
        tk.Label(stat_frame, text=f"💰 Tổng giá trị vốn hàng hóa: {total_value:,.0f} VNĐ", font=("Arial", 11, "bold"),
                 fg="red").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(stat_frame, text=f"📝 Tổng lượt khách Pre-order: {total_pre} đơn", font=("Arial", 11)).grid(row=2,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=5)

        # Container chứa bảng thống kê dòng sản phẩm
        grade_frame = tk.LabelFrame(self.master, text=" Thống kê theo Dòng (Grade) ", font=("Arial", 10, "bold"),
                                    padx=20, pady=20)
        grade_frame.pack(fill="both", expand=True, padx=40, pady=20)

        cols = ("Grade", "SoLuong")
        tree = ttk.Treeview(grade_frame, columns=cols, show="headings", height=5)
        tree.heading("Grade", text="Dòng sản phẩm")
        tree.heading("SoLuong", text="Số mẫu đang có")
        tree.column("Grade", anchor="center")
        tree.column("SoLuong", anchor="center")
        tree.pack(fill="both", expand=True)

        for g, count in grade_count.items():
            tree.insert("", "end", values=(g, count))

        # Nút quay về
        CustomButton(self.master, text="Về Menu chính", command=self.app_manager.show_menu_page,
                     style_type="secondary").pack(pady=20)

    def calculate_stats(self):
        """Đọc file csv và tính toán con số"""
        total_qty = 0
        total_value = 0
        total_pre = 0
        grade_count = {}

        path = "database/kho_hang.csv"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for r in reader:
                    if len(r) >= 8:
                        try:
                            # r[3]: Số lượng, r[4]: Pre-order, r[5]: Giá bán, r[2]: Grade
                            qty = int(r[3])
                            pre = int(r[4])
                            price = float(r[5])
                            grade = r[2]

                            total_qty += qty
                            total_value += (qty * price)
                            total_pre += pre

                            grade_count[grade] = grade_count.get(grade, 0) + 1
                        except:
                            continue
        return total_qty, total_value, total_pre, grade_count