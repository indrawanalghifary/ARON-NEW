import json
import os
import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog
from PySide6.QtCore import QStringListModel, Signal, QObject, QThread, QTimer, QUrl
from aron_ui import Ui_MainWindow
from datetime import datetime
from theme_manager import ThemeManager
from api_db import SupabaseAPI
from PySide6.QtGui import QDesktopServices
from qasync import QEventLoop, asyncSlot
import time
import asyncio
# from perbaikan import process_pdf_resi_ultimate
# from manual import aron
from bagus import main



class SupabaseExpirationChecker(QObject):
    expiration_checked = Signal(bool, str) # Signal to emit (is_expired, user_email)

    def __init__(self, supabase_api: SupabaseAPI, user_email: str, parent=None):
        super().__init__(parent)
        self.supabase_api = supabase_api
        self.user_email = user_email

    def check_expiration(self):
        if not self.user_email:
            self.expiration_checked.emit(True, "") # No user logged in, consider it expired or invalid
            return

        try:
            user_data = self.supabase_api.read_data("user_data", {"email": self.user_email})
            if user_data and user_data[0] and "expire_date" in user_data[0]:
                expire_date_str = user_data[0]["expire_date"]
                # Assuming expire_date_str is in ISO format, e.g., "YYYY-MM-DDTHH:MM:SS+00:00"
                expire_date = datetime.fromisoformat(expire_date_str.replace("Z", "+00:00"))
                current_date = datetime.now(expire_date.tzinfo) # Ensure timezone awareness

                if current_date > expire_date:
                    print(f"API for {self.user_email} has expired.")
                    self.expiration_checked.emit(True, self.user_email)
                else:
                    print(f"API for {self.user_email} is still active. Expires on: {expire_date}")
                    self.expiration_checked.emit(False, self.user_email)
            else:
                print(f"No expiration data found for {self.user_email}.")
                self.expiration_checked.emit(True, self.user_email) # Consider no data as expired
        except Exception as e:
            print(f"Error checking expiration for {self.user_email}: {e}")
            self.expiration_checked.emit(True, self.user_email) # Emit expired on error

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Browser
        self.browsers = []

        # Supabase client initialization (placeholders)
        self.supabase_url: str = "https://shhtzvevhywlixllklmm.supabase.co/"
        self.supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNoaHR6dmV2aHl3bGl4bGxrbG1tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4NDEwMjcsImV4cCI6MjA3MTQxNzAyN30.xTGInN9vGZEyEbFivNRbXXdiE1IH1WVA1Oxd8IY5t-A"
        self.supabase_api = SupabaseAPI(self.supabase_url, self.supabase_key)
        self.logged_in_user_email = None
        self.user = None

        # Setup for API expiration check
        self.expiration_thread = QThread()
        self.expiration_checker = SupabaseExpirationChecker(self.supabase_api, "") # User email will be set after login
        self.expiration_checker.moveToThread(self.expiration_thread)
        self.expiration_checker.expiration_checked.connect(self.handle_expiration_check_result)
        self.expiration_thread.start()

        self.expiration_timer = QTimer(self)
        self.expiration_timer.setInterval(5 * 60 * 1000) # 5 minutes in milliseconds
        self.expiration_timer.timeout.connect(self.expiration_checker.check_expiration)

        self.ui.tombol_login.clicked.connect(self.login)
        self.ui.input_password.returnPressed.connect(self.login) # Connect Enter key to login
        self.ui.tombol_logout.clicked.connect(self.logout) # Assuming a logout button exists

        self.theme_manager = ThemeManager(app)
        self.ui.tombol_tema.clicked.connect(self.show_theme_dialog)

        # Disable tabs initially, except the "Akun" tab (index 1)
        self.ui.tabWidget.setTabEnabled(0, False) # Tiktok tab
        # self.ui.tabWidget.setTabEnabled(1, True) # Akun tab is already enabled by default
        self.ui.stackedWidget.setCurrentIndex(1) # Show page_login initially

        

        #Initialize open url
        self.ui.tombol_website.clicked.connect(self.buka_url)

        self.file_path = None
        self.ui.input_file.clicked.connect(self.pilih_pdf_input)

        self.folder_path = None
        self.ui.output_file.clicked.connect(self.pilih_folder)

        self.ui.start.clicked.connect(self.jalankan_edit)

    def jalankan_edit(self):
        if not self.ui.line_save_path.text() or not self.ui.line_file_path.text():
            QMessageBox.warning(self,"Perhatian", "Pastikan file PDF dan Penyimpanan sudah dipilih")
            return
        try :
            nama_dasar = "Resi Asmin"
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nama_file = f"{nama_dasar}_{timestamp}.pdf"
            folder_tujuan = self.folder_path
            save_file = os.path.join(folder_tujuan, nama_file)
            # hasil = process_pdf_resi_ultimate(self.file_path,save_file)
            # hasil = aron(self.file_path,save_file)
            hasil = main(self.file_path, save_file, self.supabase_api)
            self.ui.output_resi.clear()
            text = "\n".join(hasil)
            self.ui.output_resi.setPlainText(text)
            QMessageBox.information(self, "Suksess", f"Berhasil Di simpan di {save_file}")
        except Exception as e :
            QMessageBox.warning(self,"Error", f"Maaf Terjadi error {e}")
    

    def pilih_pdf_input(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if self.file_path:
            self.ui.line_file_path.setText(self.file_path)
            print(f"Path file yang dipilih: {self.file_path}")

    def pilih_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(
            self,
            "Pilih Folder untuk Menyimpan File",
            "",  # path awal, bisa isi default misalnya os.getcwd()
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if self.folder_path:
            self.ui.line_save_path.setText(self.folder_path)
            print(f"Folder yang dipilih: {self.folder_path}")



    def buka_url(self):
        url = QUrl("https://www.silentech.com")  # Ganti dengan URL yang kamu inginkan
        QDesktopServices.openUrl(url)



    def expired(self):
        user_data = self.supabase_api.read_data("user_data", {"email": self.user.email})
        if user_data and user_data[0] and "expire_date" in user_data[0]:
            expire_date_str = user_data[0]["expire_date"]
            # Assuming expire_date_str is in ISO format, e.g., "YYYY-MM-DDTHH:MM:SS+00:00"
            expire_date = datetime.fromisoformat(expire_date_str.replace("Z", "+00:00"))
            return expire_date

    def login(self):
        email = self.ui.input_username.text()
        password = self.ui.input_password.text()

        try:
            self.user = self.supabase_api.sign_in(email, password)
            if self.user:
                self.logged_in_user_email = self.user.email
                self.expiration_checker.user_email = self.logged_in_user_email
                self.expiration_timer.start()
                self.expiration_checker.check_expiration() # Initial check

                print(f"Login successful for user: {self.user.email}")
                self.ui.tabWidget.setTabEnabled(0, True) # Enable Tiktok tab
                self.ui.tabWidget.setCurrentIndex(0) # Switch to Tiktok tab

                # Switch to page_informasi in stackedWidget
                self.ui.stackedWidget.setCurrentIndex(0) # 0 is page_informasi

                # Update UI to show self.user info in "Akun" tab
                self.ui.label_akun.setText(f"Nama: {self.user.email}")
                self.ui.label_serial.setText(f"ID: {self.user.id}")
                self.ui.label_id.setText(f"Last Sign In: {self.user.last_sign_in_at}")
                self.ui.label_expire.setText(f"Expired at: {self.expired()}")

            else:
                print("Login failed: Invalid credentials or an error occurred.")
                QMessageBox.warning(self, "Login Gagal", "Email atau kata sandi salah.")
        except Exception as e:
            print(f"An error occurred during login: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat login: {e}")

    def handle_expiration_check_result(self, is_expired: bool, user_email: str):
        if is_expired:
            QMessageBox.warning(self, "Sesi Berakhir", f"Sesi untuk {user_email} telah berakhir. Silakan perpanjang atau login kembali.")
            self.logout()
            QApplication.instance().quit()

    def logout(self):
        self.supabase_api.sign_out()
        self.logged_in_user_email = None
        self.expiration_timer.stop()
        self.ui.tabWidget.setTabEnabled(0, False) # Disable Tiktok tab
        self.ui.stackedWidget.setCurrentIndex(1) # Show page_login
        self.ui.label_akun.setText("Nama:")
        self.ui.label_serial.setText("ID:")
        self.ui.label_expire.setText("Last Sign In:")
        QMessageBox.information(self, "Logout Berhasil", "Anda telah berhasil keluar.")

    def show_theme_dialog(self):
        themes = ["dark", "light", "blue"]
        theme, ok = QInputDialog.getItem(self, "Pilih Tema", "Pilih tema:", themes, 0, False)
        if ok and theme:
            self.theme_manager.apply_theme(theme)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()