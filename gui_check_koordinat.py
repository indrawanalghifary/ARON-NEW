
import sys
import json
import fitz

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QAction, QImage, QPixmap, QPainter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QGraphicsRectItem, QListWidget, QMessageBox
)


class PdfView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.selection_mode = True
        self.start_scene_pos = None
        self.temp_rect = None

        self.page_items = []
        self.page_info = []
        self.selection_callback = None

    def load_pdf(self, pdf_path, zoom=1.5):
        self.scene.clear()
        self.page_items.clear()
        self.page_info.clear()

        doc = fitz.open(pdf_path)
        y_offset = 0

        for page_no in range(len(doc)):
            page = doc[page_no]

            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)

            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format_RGB888
            ).copy()

            item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            item.setPos(0, y_offset)

            self.scene.addItem(item)

            info = {
                "page": page_no + 1,
                "zoom": zoom,
                "x": 0,
                "y": y_offset,
                "width": pix.width,
                "height": pix.height
            }

            self.page_items.append(item)
            self.page_info.append(info)

            y_offset += pix.height + 20

        self.setSceneRect(self.scene.itemsBoundingRect())

    def wheelEvent(self, event):
        if self.selection_mode:
            super().wheelEvent(event)
            return

        factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1/factor, 1/factor)

    def mousePressEvent(self, event):
        if self.selection_mode and event.button() == Qt.LeftButton:
            self.start_scene_pos = self.mapToScene(event.position().toPoint())

            self.temp_rect = QGraphicsRectItem()
            self.scene.addItem(self.temp_rect)

            self.temp_rect.setRect(
                QRectF(self.start_scene_pos, self.start_scene_pos)
            )
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selection_mode and self.temp_rect:
            current = self.mapToScene(event.position().toPoint())

            rect = QRectF(
                self.start_scene_pos,
                current
            ).normalized()

            self.temp_rect.setRect(rect)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.selection_mode and self.temp_rect:

            rect = self.temp_rect.rect()

            page_data = None

            for info in self.page_info:
                page_rect = QRectF(
                    info["x"],
                    info["y"],
                    info["width"],
                    info["height"]
                )

                if page_rect.intersects(rect):
                    page_data = info
                    break

            if page_data:
                zoom = page_data["zoom"]

                x1 = (rect.left() - page_data["x"]) / zoom
                y1 = (rect.top() - page_data["y"]) / zoom
                x2 = (rect.right() - page_data["x"]) / zoom
                y2 = (rect.bottom() - page_data["y"]) / zoom

                result = {
                    "page": page_data["page"],
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "x2": round(x2, 2),
                    "y2": round(y2, 2),
                    "width": round(x2 - x1, 2),
                    "height": round(y2 - y1, 2),
                }

                if self.selection_callback:
                    self.selection_callback(result)

            self.temp_rect = None
            return

        super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Coordinate Designer")
        self.resize(1400, 900)

        self.areas = []

        self.view = PdfView()
        self.view.selection_callback = self.add_area

        self.info_label = QLabel("Belum ada area dipilih")

        self.area_list = QListWidget()

        btn_copy = QPushButton("Copy Area Terakhir")
        btn_copy.clicked.connect(self.copy_last)

        btn_export = QPushButton("Export JSON")
        btn_export.clicked.connect(self.export_json)

        btn_import = QPushButton("Import JSON")
        btn_import.clicked.connect(self.import_json)

        btn_toggle = QPushButton("Mode Seleksi ON/OFF")
        btn_toggle.clicked.connect(self.toggle_selection)

        right = QVBoxLayout()
        right.addWidget(self.info_label)
        right.addWidget(self.area_list)
        right.addWidget(btn_copy)
        right.addWidget(btn_export)
        right.addWidget(btn_import)
        right.addWidget(btn_toggle)

        layout = QHBoxLayout()
        layout.addWidget(self.view, 4)

        side = QWidget()
        side.setLayout(right)

        layout.addWidget(side, 1)

        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)

        file_menu = self.menuBar().addMenu("File")

        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self.open_pdf)

        file_menu.addAction(open_action)

    def open_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF (*.pdf)"
        )

        if file:
            self.view.load_pdf(file)

    def add_area(self, data):
        self.areas.append(data)

        self.info_label.setText(
            json.dumps(data, indent=2)
        )

        self.area_list.addItem(
            f'Page {data["page"]} | '
            f'({data["x1"]},{data["y1"]}) - '
            f'({data["x2"]},{data["y2"]})'
        )

    def copy_last(self):
        if not self.areas:
            return

        QApplication.clipboard().setText(
            json.dumps(self.areas[-1], indent=2)
        )

    def export_json(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            "areas.json",
            "JSON (*.json)"
        )

        if not file:
            return

        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.areas, f, indent=2)

        QMessageBox.information(self, "OK", "JSON disimpan")

    def import_json(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Import JSON",
            "",
            "JSON (*.json)"
        )

        if not file:
            return

        with open(file, "r", encoding="utf-8") as f:
            self.areas = json.load(f)

        self.area_list.clear()

        for item in self.areas:
            self.area_list.addItem(
                f'Page {item["page"]} | '
                f'({item["x1"]},{item["y1"]}) - '
                f'({item["x2"]},{item["y2"]})'
            )

    def toggle_selection(self):
        self.view.selection_mode = not self.view.selection_mode

        if self.view.selection_mode:
            self.statusBar().showMessage("Mode Seleksi AKTIF")
        else:
            self.statusBar().showMessage(
                "Mode Seleksi NONAKTIF (Zoom dengan wheel)"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())