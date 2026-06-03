import json
import os
import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox
from PySide6.QtCore import QStringListModel, Signal, QObject, QThread, QTimer, QUrl
from PySide6.QtGui import QColor
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
from split import spk_proses, convert_config
from stamp_colors import get_platform_color, normalize_color, get_all_colors


class ColorPickerDialog(QDialog):
    """Dialog untuk memilih warna stamp dengan preset colors dan custom RGB"""
    
    def __init__(self, platform="default", parent=None):
        super().__init__(parent)
        self.platform = platform
        self.selected_color = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Pilih Warna Stamp 🎨")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Label
        label = QLabel(f"Pilih warna stamp untuk {self.platform.upper()}")
        layout.addWidget(label)
        
        # Combo box dengan preset colors
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset Colors:"))
        
        self.color_combo = QComboBox()
        colors = get_all_colors(normalize=False)  # Get RGB 0-255
        self.color_names = list(colors.keys())
        self.color_names.sort()
        self.color_combo.addItems(self.color_names)
        
        # Set default based on platform
        if self.platform.lower() == "tiktok" and "black" in self.color_names:
            self.color_combo.setCurrentText("black")
        elif self.platform.lower() == "shopee" and "red" in self.color_names:
            self.color_combo.setCurrentText("red")
        
        self.color_combo.currentTextChanged.connect(self.on_color_changed)
        preset_layout.addWidget(self.color_combo)
        layout.addLayout(preset_layout)
        
        # Preview color
        self.preview_label = QLabel()
        self.preview_label.setStyleSheet("border: 1px solid #ccc; min-height: 40px;")
        layout.addWidget(QLabel("Preview:"))
        layout.addWidget(self.preview_label)
        
        # Custom RGB section
        custom_label = QLabel("Atau input RGB Custom (0-255):")
        layout.addWidget(custom_label)
        
        rgb_layout = QHBoxLayout()
        
        # R spinbox
        rgb_layout.addWidget(QLabel("R:"))
        self.r_spinbox = QSpinBox()
        self.r_spinbox.setMaximum(255)
        self.r_spinbox.setValue(0)
        self.r_spinbox.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.r_spinbox)
        
        # G spinbox
        rgb_layout.addWidget(QLabel("G:"))
        self.g_spinbox = QSpinBox()
        self.g_spinbox.setMaximum(255)
        self.g_spinbox.setValue(0)
        self.g_spinbox.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.g_spinbox)
        
        # B spinbox
        rgb_layout.addWidget(QLabel("B:"))
        self.b_spinbox = QSpinBox()
        self.b_spinbox.setMaximum(255)
        self.b_spinbox.setValue(0)
        self.b_spinbox.valueChanged.connect(self.on_rgb_changed)
        rgb_layout.addWidget(self.b_spinbox)
        
        layout.addLayout(rgb_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("OK ✓")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set initial preview
        self.on_color_changed(self.color_combo.currentText())
    
    def on_color_changed(self, color_name):
        """Update spinbox dan preview ketika color combo berubah"""
        if not color_name:
            return
        
        colors = get_all_colors(normalize=False)
        if color_name in colors:
            r, g, b = colors[color_name]
            self.r_spinbox.blockSignals(True)
            self.g_spinbox.blockSignals(True)
            self.b_spinbox.blockSignals(True)
            
            self.r_spinbox.setValue(r)
            self.g_spinbox.setValue(g)
            self.b_spinbox.setValue(b)
            
            self.r_spinbox.blockSignals(False)
            self.g_spinbox.blockSignals(False)
            self.b_spinbox.blockSignals(False)
            
            self.update_preview()
    
    def on_rgb_changed(self):
        """Update preview ketika RGB spinbox berubah, clear combo selection"""
        self.color_combo.blockSignals(True)
        self.color_combo.setCurrentIndex(-1)  # Clear selection
        self.color_combo.blockSignals(False)
        
        self.update_preview()
    
    def update_preview(self):
        """Update preview color"""
        r = self.r_spinbox.value()
        g = self.g_spinbox.value()
        b = self.b_spinbox.value()
        
        # Create QColor dan set background
        color = QColor(r, g, b)
        rgb_str = f"rgb({r}, {g}, {b})"
        self.preview_label.setStyleSheet(
            f"background-color: {rgb_str}; border: 1px solid #ccc; min-height: 40px;"
        )
    
    def get_color_normalized(self):
        """Get selected color dalam format PyMuPDF (0-1.0 range)"""
        r = self.r_spinbox.value()
        g = self.g_spinbox.value()
        b = self.b_spinbox.value()
        
        return normalize_color((r, g, b))
    
    def get_color_rgb(self):
        """Get selected color dalam format RGB (0-255 range)"""
        return (
            self.r_spinbox.value(),
            self.g_spinbox.value(),
            self.b_spinbox.value()
        )


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

        # initialize split_map
        self.split_map = {}
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

        #shopee
        self.file_path_shopee = None
        self.ui.input_file_shopee.clicked.connect(self.pilih_pdf_input_shopee)

        self.folder_path_shopee = None
        self.ui.output_file_shopee.clicked.connect(self.pilih_folder_shopee)

        self.ui.start_shopee.clicked.connect(self.jalankan_edit_shopee)

    def jalankan_edit(self):
        if not self.ui.line_save_path.text() or not self.ui.line_file_path.text():
            QMessageBox.warning(self,"Perhatian", "Pastikan file PDF dan Penyimpanan sudah dipilih")
            return
        
        # Show color picker dialog untuk TikTok
        color_dialog = ColorPickerDialog(platform="tiktok", parent=self)
        if color_dialog.exec() == QDialog.Accepted:
            try :
                nama_dasar = "Aron-Tiktok"
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                nama_file = f"{nama_dasar}_{timestamp}.pdf"
                folder_tujuan = self.folder_path
                save_file = os.path.join(folder_tujuan, nama_file)
                
                # Get selected color dari dialog (normalized untuk PyMuPDF)
                stamp_color = color_dialog.get_color_normalized()
                
                hasil = main(self.file_path, save_file, split_map=self.split_map, codename=self.codename, stamp_color=stamp_color)
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
####shopee
    def jalankan_edit_shopee(self):
        if not self.ui.line_save_path_shopee.text() or not self.ui.line_file_path_shopee.text():
            QMessageBox.warning(self,"Perhatian", "Pastikan file PDF dan Penyimpanan sudah dipilih")
            return
        
        # Show color picker dialog untuk Shopee
        color_dialog = ColorPickerDialog(platform="shopee", parent=self)
        if color_dialog.exec() == QDialog.Accepted:
            try :
                nama_dasar = "Aron-Shopee"
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                nama_file = f"{nama_dasar}_{timestamp}.pdf"
                folder_tujuan = self.folder_path_shopee
                save_file = os.path.join(folder_tujuan, nama_file)
                
                # Get selected color dari dialog (normalized untuk PyMuPDF)
                stamp_color = color_dialog.get_color_normalized()
                
                hasil = spk_proses(self.file_path_shopee, save_file, split_map=self.split_map, codename=self.codename, stamp_color=stamp_color)
                self.ui.output_resi_shopee.clear()
                text = "\n".join(hasil)
                self.ui.output_resi_shopee.setPlainText(text)
                QMessageBox.information(self, "Suksess", f"Berhasil Di simpan di {save_file}")
            except Exception as e :
                QMessageBox.warning(self,"Error", f"Maaf Terjadi error {e}")

    def pilih_pdf_input_shopee(self):
        self.file_path_shopee, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if self.file_path_shopee:
            self.ui.line_file_path_shopee.setText(self.file_path_shopee)
            print(f"Path file yang dipilih: {self.file_path_shopee}")

    def pilih_folder_shopee(self):
        self.folder_path_shopee = QFileDialog.getExistingDirectory(
            self,
            "Pilih Folder untuk Menyimpan File",
            "",  # path awal, bisa isi default misalnya os.getcwd()
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if self.folder_path_shopee:
            self.ui.line_save_path_shopee.setText(self.folder_path_shopee)
            print(f"Folder yang dipilih: {self.folder_path_shopee}")

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

                # Load split_map from config
                self.split_map = convert_config(response)
                print(self.split_map)
                self.codename = codename
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