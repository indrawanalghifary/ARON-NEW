import json
import os
import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog
from PySide6.QtCore import QStringListModel, Signal, QObject, QThread, QTimer, QUrl
from aron_ui import Ui_MainWindow
from datetime import datetime
from theme_manager import ThemeManager
from api_new import get_user_info
from PySide6.QtGui import QDesktopServices
from qasync import QEventLoop, asyncSlot
import time
import asyncio
# from perbaikan import process_pdf_resi_ultimate
# from manual import aron
from bagus import main



class ExpirationChecker(QObject):
    expiration_checked = Signal(bool, str, str) # Signal to emit (is_expired, user_email, error_message)

    def __init__(self, user_token: str, user_email: str, parent=None):
        super().__init__(parent)
        self.user_token = user_token
        self.user_email = user_email

    def check_expiration(self):
        if not self.user_token:
            self.expiration_checked.emit(True, "", "") # No token available, consider it expired
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Checking expiration for token: {self.user_token[:20]}...")
            user_data = get_user_info(self.user_token)
            print(f"[{timestamp}] Full API Response: {user_data}")
            
            if user_data and "status" in user_data and user_data["status"] == "success":
                data = user_data.get("data", {})
                is_expired = data.get("is_expired", True)
                
                if is_expired:
                    print(f"[{timestamp}] API for {self.user_email} has expired.")
                    self.expiration_checked.emit(True, self.user_email, "")
                else:
                    remaining_days = data.get("remaining_days", 0)
                    expired_at = data.get("expired_at", "Unknown")
                    print(f"[{timestamp}] API for {self.user_email} is still active. Expires on: {expired_at} ({remaining_days} days remaining)")
                    self.expiration_checked.emit(False, self.user_email, "")
            elif user_data and user_data.get("status") == "error":
                error_msg = user_data.get("message", "")
                print(f"[{timestamp}] API Error for {self.user_email}: {error_msg}")
                # Emit error signal with error message
                self.expiration_checked.emit(True, self.user_email, error_msg)
            else:
                print(f"[{timestamp}] Invalid response from API for {self.user_email}. Response: {user_data}")
                self.expiration_checked.emit(True, self.user_email, "") # Consider invalid response as expired
        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Error checking expiration for {self.user_email}: {e}")
            self.expiration_checked.emit(True, self.user_email, str(e)) # Emit expired on error with error message

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Browser
        self.browsers = []

        # Token-based authentication
        self.user_token = None
        self.user_data = None

        # Setup for API expiration check
        self.expiration_thread = QThread()
        self.expiration_checker = ExpirationChecker("", "") # User token and email will be set after login
        self.expiration_checker.moveToThread(self.expiration_thread)
        self.expiration_checker.expiration_checked.connect(self.handle_expiration_check_result)
        self.expiration_thread.start()

        self.expiration_timer = QTimer(self)
        self.expiration_timer.setInterval(30 * 1000) # 30 seconds untuk testing (ubah ke 5 * 60 * 1000 untuk production)
        self.expiration_timer.timeout.connect(self.expiration_checker.check_expiration)

        self.ui.tombol_login.clicked.connect(self.login)
        self.ui.input_token.returnPressed.connect(self.login) # Connect Enter key to login
        self.ui.tombol_logout.clicked.connect(self.logout) # Assuming a logout button exists

        self.theme_manager = ThemeManager(app)
        self.ui.tombol_tema.clicked.connect(self.show_theme_dialog)

        # Disable tabs initially, except the "Akun" tab (index 1)
        self.ui.tabWidget.setTabEnabled(0, False) # Tiktok tab
        self.ui.tabWidget.setTabEnabled(1, False) # Shopee tab
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
            hasil = main(self.file_path, save_file)
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

    def manual_check_expiration(self):
        """Manual trigger untuk test expiration check - panggil dari console: window.manual_check_expiration()"""
        print("[Manual Trigger] Checking expiration manually...")
        self.expiration_checker.check_expiration()



    def buka_url(self):
        if self.user_data and "website_url" in self.user_data:
            url = QUrl(self.user_data["website_url"])
        else:
            url = QUrl("https://www.silentech.com")
        QDesktopServices.openUrl(url)

    def login(self):
        user_token = self.ui.input_token.text().strip()
        
        if not user_token:
            QMessageBox.warning(self, "Login Gagal", "Masukkan token yang valid.")
            return

        try:
            # Verify token using API
            response = get_user_info(user_token)
            
            if response and response.get("status") == "success":
                self.user_token = user_token
                self.user_data = response.get("data", {})
                
                # Update expiration checker with token and email
                account_email = self.user_data.get("account_email", "Unknown")
                self.expiration_checker.user_token = self.user_token
                self.expiration_checker.user_email = account_email
                
                self.expiration_timer.start()
                self.expiration_checker.check_expiration() # Initial check

                print(f"Login successful for token: {user_token}")
                self.ui.tabWidget.setTabEnabled(0, True) # Enable Tiktok tab
                self.ui.tabWidget.setTabEnabled(1, True) # Enable Shopee tab
                self.ui.tabWidget.setCurrentIndex(0) # Switch to Tiktok tab

                # Switch to page_informasi in stackedWidget
                self.ui.stackedWidget.setCurrentIndex(0) # 0 is page_informasi

                # Update UI to show user info in "Akun" tab
                profile_name = self.user_data.get("profile_name", "Unknown")
                self.ui.label_akun.setText(f"Nama: {profile_name}")
                self.ui.label_serial.setText(f"Email: {account_email}")
                
                codename = self.user_data.get("codename", "Unknown")
                package_title = self.user_data.get("package_title", "Unknown")
                self.ui.label_id.setText(f"Codename: {codename} ({package_title})")
                
                expired_at = self.user_data.get("expired_at", "Unknown")
                remaining_days = self.user_data.get("remaining_days", 0)
                self.ui.label_expire.setText(f"Expired at: {expired_at} ({remaining_days} days remaining)")
                
                # Clear input fields
                self.ui.input_token.clear()
            else:
                error_msg = response.get("message", "Token tidak valid atau sudah expired.")
                print(f"Login failed: {error_msg}")
                QMessageBox.warning(self, "Login Gagal", error_msg)
        except Exception as e:
            print(f"An error occurred during login: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat login: {e}")

    def handle_expiration_check_result(self, is_expired: bool, user_email: str, error_message: str = ""):
        if is_expired:
            # Check for specific error message
            if error_message and "Slot sudah penuh" in error_message:
                QMessageBox.critical(self, "Error", f"Slot sudah penuh. Aplikasi akan ditutup.")
                self.logout()
                QApplication.instance().quit()
            else:
                QMessageBox.warning(self, "Sesi Berakhir", f"Sesi untuk {user_email} telah berakhir. Silakan perpanjang atau login kembali.")
                self.logout()
                QApplication.instance().quit()

    def logout(self):
        self.user_token = None
        self.user_data = None
        self.expiration_timer.stop()
        self.ui.tabWidget.setTabEnabled(0, False) # Disable Tiktok tab
        self.ui.stackedWidget.setCurrentIndex(1) # Show page_login
        self.ui.label_akun.setText("Nama:")
        self.ui.label_serial.setText("Email:")
        self.ui.label_id.setText("Codename:")
        self.ui.label_expire.setText("Expired at:")
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