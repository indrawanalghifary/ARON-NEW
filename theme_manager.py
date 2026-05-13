from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor

class ThemeManager:
    def __init__(self, app: QApplication):
        self.app = app
        self.current_theme = "light"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name: str):
        palette = QPalette()
        if theme_name == "dark":
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        elif theme_name == "light":
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        elif theme_name == "blue":
            palette.setColor(QPalette.Window, QColor(35, 47, 62))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(20, 30, 40))
            palette.setColor(QPalette.AlternateBase, QColor(35, 47, 62))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(35, 47, 62))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 170, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 170, 255))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        self.app.setPalette(palette)
        self.current_theme = theme_name

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.apply_theme("light")
        elif self.current_theme == "light":
            self.apply_theme("blue")
        else:
            self.apply_theme("dark")