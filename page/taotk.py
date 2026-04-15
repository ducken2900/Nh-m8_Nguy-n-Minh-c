import tkinter as tk
from tkinter import messagebox, ttk
import csv
from common.button import CustomButton


class TaoTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.ents = {}
        self.view()

    def view(self):
        tk.Label(self.master, text="NHẬP HÀNG GUNDAM", font=("Arial", 18, "bold")).pack(pady=20)

        grades = ["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"]
        status = ["Sẵn hàng", "Hết hàng", "Sắp về"]
        labels = ["Mã Gundam:", "Tên mô hình:", "Grade:", "Số lượng:", "PreOrder:", "Giá bán:", "Số ngày nhập:",
                  "Tình trạng:"]

        form = tk.Frame(self.master)
        form.pack(padx=40, fill="x")

        for i, txt in enumerate(labels):
            tk.Label(form, text=txt).grid(row=i, column=0, sticky="w", pady=10)
            if txt == "Grade:":
                e = ttk.Combobox(form, values=grades, state="readonly")
                e.grid(row=i, column=1, sticky="ew");
                e.current(2)
            elif txt == "Tình trạng:":
                e = ttk.Combobox(form, values=status, state="readonly")
                e.grid(row=i, column=1, sticky="ew");
                e.current(0)
            else:
                e = tk.Entry(form)
                e.grid(row=i, column=1, sticky="ew")
                if any(x in txt for x in ["lượng", "Pre", "Giá", "ngày"]): e.insert(0, "0")
            self.ents[txt] = e

        form.columnconfigure(1, weight=1)
        CustomButton(self.master, text="LƯU KHO", command=self.save, style_type="primary").pack(pady=20)
        CustomButton(self.master, text="HỦY", command=self.app_manager.show_quanly_kho_page,
                     style_type="secondary").pack()

    def save(self):
        keys = ["Mã Gundam:", "Tên mô hình:", "Grade:", "Số lượng:", "PreOrder:", "Giá bán:", "Số ngày nhập:",
                "Tình trạng:"]
        d = [self.ents[k].get().strip() for k in keys]
        if not d[0] or not d[1]: return messagebox.showerror("!", "Thiếu Mã/Tên")
        with open("database/kho_hang.csv", "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(d)
        self.app_manager.show_quanly_kho_page()