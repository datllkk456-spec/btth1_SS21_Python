import logging
import re


logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InvalidAmountError(Exception):
    """
    Raised when amount <= 0.
    """
    pass


class InsufficientBalanceError(Exception):
    """
    Raised when balance is not enough.
    """
    pass


class Wallet:
    """
    MoMo wallet.
    """

    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        """
        Deposit money into wallet.
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        self.balance += amount

        logging.info(
            f"Deposit successful: +{amount} VND. "
            f"Current Balance: {self.balance}"
        )

    def transfer(self, phone_number, amount):
        """
        Transfer money.
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Attempted to transfer {amount} VND "
                f"with balance {self.balance} VND."
            )

        if amount >= 10000000:
            logging.warning(
                f"High value transaction detected: "
                f"{amount} VND to {phone_number}"
            )

        self.balance -= amount

        logging.info(
            f"Transfer successful: -{amount} VND "
            f"to {phone_number}. "
            f"Current Balance: {self.balance}"
        )

    def get_balance(self):
        """
        Return current balance.
        """
        logging.info(
            f"Balance checked. Current Balance: {self.balance}"
        )

        return self.balance


def display_menu():
    """
    Display menu.
    """
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("=" * 40)


def deposit_money(wallet):
    """
    Handle deposit.
    """
    print("\n--- NẠP TIỀN VÀO VÍ ---")

    while True:
        try:
            amount = int(
                input("Nhập số tiền cần nạp: ")
            )

            wallet.deposit(amount)

            print(
                f"\nNạp tiền thành công: "
                f"+{amount:,} VND"
            )

            print(
                f"Số dư hiện tại: "
                f"{wallet.get_balance():,} VND"
            )

            break

        except ValueError:
            print(
                "Lỗi: Vui lòng nhập số tiền hợp lệ."
            )

            logging.error(
                "ValueError: Invalid numeric input "
                "for deposit."
            )

        except InvalidAmountError as error:
            print(
                "Lỗi: Số tiền giao dịch "
                "phải lớn hơn 0."
            )

            logging.error(
                f"InvalidAmountError: {error}"
            )


def transfer_money(wallet):
    """
    Handle transfer.
    """
    print("\n--- CHUYỂN TIỀN ---")

    phone_number = input(
        "Nhập số điện thoại người nhận: "
    ).strip()

    if not re.fullmatch(r"\d{10}", phone_number):
        print(
            "Số điện thoại phải gồm đúng 10 số."
        )
        return

    while True:
        try:
            amount = int(
                input(
                    "Nhập số tiền cần chuyển: "
                )
            )

            wallet.transfer(
                phone_number,
                amount
            )

            print(
                f"\nChuyển tiền thành công "
                f"tới số điện thoại "
                f"{phone_number}."
            )

            print(
                f"Số tiền đã chuyển: "
                f"{amount:,} VND"
            )

            print(
                f"Số dư còn lại: "
                f"{wallet.get_balance():,} VND"
            )

            break

        except ValueError:
            print(
                "Lỗi: Vui lòng nhập số tiền hợp lệ."
            )

            logging.error(
                "ValueError: Invalid numeric input "
                "for transfer."
            )

        except InvalidAmountError as error:
            print(
                "Lỗi: Số tiền giao dịch "
                "phải lớn hơn 0."
            )

            logging.error(
                f"InvalidAmountError: {error}"
            )

        except InsufficientBalanceError as error:
            print(
                "\nGiao dịch thất bại: "
                "Số dư của bạn không đủ."
            )

            print(
                f"Số dư hiện tại: "
                f"{wallet.get_balance():,} VND"
            )

            logging.error(
                f"InsufficientBalanceError: "
                f"{error}"
            )

            break


def show_balance(wallet):
    """
    Display current balance.
    """
    print("\n--- SỐ DƯ VÍ MOMO ---")

    print(
        f"Số dư hiện tại: "
        f"{wallet.get_balance():,} VND"
    )


def main():
    """
    Main program.
    """
    wallet = Wallet()

    while True:

        display_menu()

        choice = input(
            "Chọn chức năng (1-4): "
        ).strip()

        if choice == "1":
            deposit_money(wallet)

        elif choice == "2":
            transfer_money(wallet)

        elif choice == "3":
            show_balance(wallet)

        elif choice == "4":
            print(
                "Cảm ơn bạn đã sử dụng dịch vụ."
            )

            logging.info(
                "System shutdown."
            )

            break

        else:
            print(
                "Lựa chọn không hợp lệ."
            )


if __name__ == "__main__":
    main()