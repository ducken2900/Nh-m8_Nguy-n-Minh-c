import tkinter as tk
from tkinter import messagebox, ttk
import csv, os
from common.button import CustomButton


class SuaTKPage:
    def __init__(self, master, app_manager, item_data):
        self.master = master
        self.app_manager = app_manager
        self.item_data = item_data
        self.old_id = item_data[0]
        self.ents = {}
        self.view()

    def view(self):
        tk.Label(self.master, text="CẬP NHẬT MÔ HÌNH", font=("Arial", 18, "bold")).pack(pady=20)
        grades = ["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"]
        status = ["Sẵn hàng", "Hết hàng", "Sắp về"]
        labels = ["Mã:", "Tên:", "Grade:", "SL:", "Pre:", "Giá:", "Ngày:", "Tình trạng:"]

        form = tk.Frame(self.master)
        form.pack(padx=40, fill="x")

        for i, txt in enumerate(labels):
            tk.Label(form, text=txt).grid(row=i, column=0, sticky="w", pady=10)
            val = self.item_data[i] if i < len(self.item_data) else ""

            if "Grade" in txt:
                e = ttk.Combobox(form, values=grades, state="readonly")
                e.grid(row=i, column=1, sticky="ew");
                e.set(val)
            elif "trạng" in txt:
                e = ttk.Combobox(form, values=status, state="readonly")
                e.grid(row=i, column=1, sticky="ew");
                e.set(val)
            else:
                e = tk.Entry(form);
                e.grid(row=i, column=1, sticky="ew");
                e.insert(0, val)
            self.ents[txt] = e

        form.columnconfigure(1, weight=1)
        CustomButton(self.master, text="CẬP NHẬT", command=self.update, style_type="warning").pack(pady=20)
        CustomButton(self.master, text="HỦY", command=self.app_manager.show_quanly_kho_page,
                     style_type="secondary").pack()

    def update(self):
        keys = ["Mã:", "Tên:", "Grade:", "SL:", "Pre:", "Giá:", "Ngày:", "Tình trạng:"]
        new_row = [self.ents[k].get().strip() for k in keys]
        rows = []
        with open("database/kho_hang.csv", "r", encoding="utf-8") as f:
            for r in csv.reader(f):
                rows.append(new_row if len(r) > 0 and r[0] == self.old_id else r)
        with open("database/kho_hang.csv", "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)
        self.app_manager.show_quanly_kho_page()