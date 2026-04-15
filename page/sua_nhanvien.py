import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from common.button import CustomButton


class SuaNhanVienPage:
    def __init__(self, master, app_manager, data):
        self.master = master
        self.app_manager = app_manager
        # data chứa: [User, Pass, Name, Phone, Mission]
        self.data = data
        self.old_username = data[0]  # Giữ lại User cũ để tìm dòng trong file
        self.ents = {}
        self.view()

    def view(self):
        # Tiêu đề trang
        tk.Label(self.master, text="SỬA NHÂN VIÊN", font=("Arial", 22, "bold"), fg="#e67e22").pack(pady=20)

        # Danh sách nhiệm vụ cụ thể trong Shop Gundam
        self.mission_list = [
            "Nhân viên",  # Quyền mặc định
            "Quản lý tổng (Admin)",
            "Tư vấn bán hàng (Am hiểu HG/MG/PG)",
            "Kỹ thuật viên (Ráp mẫu trưng bày)",
            "Nhân viên kho (Kiểm hàng & Nhập hàng)",
            "Thu ngân"
        ]

        labels = ["User:", "Pass:", "Tên:", "SĐT:", "Quyền:"]

        form = tk.Frame(self.master)
        form.pack(padx=40, fill="x")

        for i, txt in enumerate(labels):
            tk.Label(form, text=txt, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=10)

            # Lấy giá trị cũ từ dữ liệu được truyền vào
            old_val = self.data[i] if i < len(self.data) else ""

            if txt == "Quyền:":
                # Ô chọn nhiệm vụ (Combobox)
                self.ents[txt] = ttk.Combobox(form, values=self.mission_list, state="readonly", font=("Arial", 10))
                self.ents[txt].grid(row=i, column=1, sticky="ew", padx=10)

                # Nếu nhiệm vụ cũ có trong danh sách thì chọn nó, nếu không thì hiện đúng chữ đó
                if old_val in self.mission_list:
                    self.ents[txt].set(old_val)
                else:
                    # Trường hợp dữ liệu cũ là "Tư vấn bán hàng..." như trong ảnh của bạn
                    self.ents[txt].set(old_val)
            else:
                # Các ô nhập text
                e = tk.Entry(form, font=("Arial", 10), bd=1, relief="solid")
                e.grid(row=i, column=1, sticky="ew", padx=10)
                e.insert(0, old_val)
                self.ents[txt] = e

        form.columnconfigure(1, weight=1)

        # Nút Cập nhật màu cam như trong ảnh
        btn_update = tk.Button(self.master, text="CẬP NHẬT", command=self.update,
                               bg="#ffa500", fg="black", font=("Arial", 10, "bold"), height=2)
        btn_update.pack(pady=20, fill="x", padx=100)

        # Nút Hủy
        btn_cancel = tk.Button(self.master, text="HỦY", command=self.app_manager.show_quanly_taikhoan_page,
                               bg="#f0f0f0", fg="black", font=("Arial", 9))
        btn_cancel.pack()

    def update(self):
        """Hàm lưu thông tin nhân viên đã sửa vào database/tk.csv"""
        # Thu thập dữ liệu mới
        new_row = [
            self.ents["User:"].get().strip(),
            self.ents["Pass:"].get().strip(),
            self.ents["Tên:"].get().strip(),
            self.ents["SĐT:"].get().strip(),
            self.ents["Quyền:"].get()
        ]

        if not new_row[0] or not new_row[1]:
            messagebox.showerror("Lỗi", "Tài khoản và Mật khẩu không được để trống!")
            return

        rows = []
        path = "database/tk.csv"
        try:
            if not os.path.exists(path):
                messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu nhân viên!")
                return

            # Đọc file và thay thế dòng cũ bằng dòng mới
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for r in reader:
                    if len(r) > 0 and r[0] == self.old_username:
                        rows.append(new_row)  # Thay bằng dữ liệu mới
                    else:
                        rows.append(r)  # Giữ nguyên các dòng khác

            # Ghi lại toàn bộ danh sách vào file
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin cho nhân viên: {new_row[2]}")
            # Quay lại trang Quản lý tài khoản
            self.app_manager.show_quanly_taikhoan_page()

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể lưu dữ liệu: {str(e)}")