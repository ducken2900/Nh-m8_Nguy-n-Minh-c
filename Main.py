from app_manager import AppManager

def main():
    print("-" * 30)
    print("HỆ THỐNG QUẢN LÝ GUNDAM STORE")
    print("Trạng thái: Đang khởi chạy...")
    print("-" * 30)
    app = AppManager()
    app.run()

if __name__ == "__main__":
    main()