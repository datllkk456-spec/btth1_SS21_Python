import logging
from datetime import datetime

logging.basicConfig(
    filename="momo_transactions.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def menu():
    """Hiển thị Menu giao diện CLI."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("===============================================")


def deposit(user_money):
    print("\n--- NẠP TIỀN VÀO VÍ ---")
    try:
        # Ép kiểu int vì tiền VND không dùng số thập phân (float)
        input_money = int(input("Nhập số tiền cần nạp: "))

        if input_money <= 0:
            logging.error(
                f"InvalidAmountError: Attempted to process {input_money} VND."
            )
            # Dùng raise để ép chương trình nhảy xuống khối except xử lý
            raise ValueError("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

        # Nạp thành công
        user_money += input_money
        print(f"\nNạp tiền thành công: +{input_money:,} VND")
        print(f"Số dư hiện tại: {user_money:,} VND")

        logging.info(
            f"Deposit successful: +{input_money} VND. "
            f"Current Balance: {user_money}"
        )

    except ValueError as e:
        error_msg = str(e)
        # Nếu lỗi do người dùng nhập chữ thay vì nhập số
        if "invalid literal for int()" in error_msg:
            logging.error("ValueError: Invalid numeric input for deposit.")
            print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
        else:
            # Nếu lỗi do ta chủ động raise (số tiền âm/bằng 0)
            print(f"\n{error_msg}")

    return user_money  # Bắt buộc phải return để cập nhật lại số dư ở main


def transfer(user_money):
    print("\n--- CHUYỂN TIỀN ---")
    phone_number = input("Nhập số điện thoại người nhận: ")

    # Kiểm tra định dạng số điện thoại
    if not phone_number.isdigit() or len(phone_number) != 10:
        print("Lỗi: Số điện thoại không hợp lệ (Phải đúng 10 số).")
        return user_money

    try:
        payment = int(input("Nhập số tiền cần chuyển: "))

        # Bẫy lỗi tiền âm hoặc bằng 0
        if payment <= 0:
            logging.error(
                f"InvalidAmountError: Attempted to process {payment} VND."
            )
            raise ValueError("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

        # Bẫy lỗi không đủ số dư
        if payment > user_money:
            logging.error(
                f"InsufficientBalanceError: Attempted to transfer {payment} "
                f"VND with balance {user_money} VND."
            )
            raise ValueError("Giao dịch thất bại: Số dư của bạn không đủ.")

        # Bẫy lỗi giao dịch giá trị cao (Cảnh báo nhưng vẫn thực hiện)
        if payment >= 10000000:
            logging.warning(
                f"High value transaction detected: {payment} "
                f"VND to {phone_number}"
            )

        # Chuyển tiền thành công
        user_money -= payment
        print(f"\nChuyển tiền thành công tới số điện thoại {phone_number}.")
        print(f"Số tiền đã chuyển: {payment:,} VND")
        print(f"Số dư còn lại: {user_money:,} VND")

        logging.info(
            f"Transfer successful: -{payment} VND to {phone_number}. "
            f"Current Balance: {user_money}"
        )

    except ValueError as e:
        error_msg = str(e)
        if "invalid literal for int()" in error_msg:
            print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
        else:
            print(f"\n{error_msg}")

    return user_money  # Bắt buộc phải return để cập nhật lại số dư ở main


def check_balance(user_money):
    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(f"Số dư hiện tại: {user_money:,} VND")
    logging.info(f"Balance checked. Current Balance: {user_money}")



def main():
    # Số dư mặc định khi khởi chạy là 0 VNĐ theo đúng yêu cầu đề bài
    user_money = 0

    while True:
        menu()
        choice = input("Chọn chức năng (1-4): ")

        match choice:
            case "1":
                user_money = deposit(user_money)
            case "2":
                user_money = transfer(user_money)
            case "3":
                check_balance(user_money)
            case "4":
                print("\nCảm ơn bạn đã sử dụng dịch vụ.")
                logging.info("System shutdown")
                break
            case _:
                print("Lựa chọn không hợp lệ, vui lòng chọn lại từ 1 đến 4.")


if __name__ == "__main__":
    main()