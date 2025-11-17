"""
YOLOv8 + PyQt5 水果识别演示程序 (app.py)

功能：
- 加载训练好的 YOLOv8 模型（支持 .pt）
- 图片检测（选择图片并检测 -> 显示带框图像 + 类别计数）
- 视频/摄像头检测（选择视频或打开摄像头进行实时检测）
- 保存标注后的图片/视频
- 设置置信度阈值、显示 top-k 等

使用方法：
    python app.py

注意：在运行前请确保在同一个虚拟环境中安装了 requirements.txt 中的依赖，
并确保模型路径正确（默认指向 runs/detect/train4/weights/best.pt）
"""

import sys
import os
import time
from pathlib import Path
from collections import Counter

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QTableWidget, QTableWidgetItem, QMessageBox, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QImage

import cv2
import numpy as np
from ultralytics import YOLO


# ---------------------------
# Helper: convert numpy image (BGR) -> QPixmap
# ---------------------------
def cvimg_to_qpixmap(cv_img_bgr):
    """Convert BGR OpenCV image (H,W,3) to QPixmap"""
    rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


# ---------------------------
# Detector Thread (for performing model.predict without blocking UI)
# ---------------------------
class DetectorThread(QThread):
    # signals: annotated image (BGR), counts dict, raw results object
    result_ready = pyqtSignal(np.ndarray, dict, object)
    finished_signal = pyqtSignal()

    def __init__(self, model, source, conf_thres=0.25, is_video=False, frame_rate=0.03, parent=None):
        super().__init__(parent)
        self.model = model
        self.source = source  # either image path, video path, or camera index
        self.conf_thres = conf_thres
        self._running = True
        self.is_video = is_video
        self.frame_rate = frame_rate  # seconds between frames for webcam loop

    def stop(self):
        self._running = False

    def run(self):
        try:
            if self.is_video:
                # video or webcam
                cap = cv2.VideoCapture(self.source)
                if not cap.isOpened():
                    print("Cannot open video source:", self.source)
                    self.finished_signal.emit()
                    return
                while self._running:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # run model inference on frame
                    results = self.model.predict(source=frame, conf=self.conf_thres, save=False, verbose=False)
                    # results[0] is ultralytics.engine.results.Results
                    annotated = results[0].plot()  # returns BGR numpy image
                    # count classes
                    counts = {}
                    try:
                        names = results[0].names
                        boxes = results[0].boxes
                        cls_ids = [int(b.cls[0]) for b in boxes]
                        class_names = [names[c] for c in cls_ids]
                        counts = dict(Counter(class_names))
                    except Exception:
                        counts = {}
                    # emit
                    self.result_ready.emit(annotated, counts, results[0])
                    # small sleep to yield (controls display fps)
                    time.sleep(self.frame_rate)
                cap.release()
            else:
                # single image
                results = self.model.predict(source=self.source, conf=self.conf_thres, save=False, verbose=False)
                annotated = results[0].plot()
                counts = {}
                try:
                    names = results[0].names
                    boxes = results[0].boxes
                    cls_ids = [int(b.cls[0]) for b in boxes]
                    class_names = [names[c] for c in cls_ids]
                    counts = dict(Counter(class_names))
                except Exception:
                    counts = {}
                self.result_ready.emit(annotated, counts, results[0])
        except Exception as e:
            print("DetectorThread exception:", e)
        finally:
            self.finished_signal.emit()


# ---------------------------
# Main Window
# ---------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 水果识别与计数 (PyQt5)")
        self.resize(1100, 700)

        # Load model (default path) — 改为你的 best.pt 路径
        default_model_path = r"D:\code\fruit_detection\runs\detect\train4\weights\best.pt"
        if not os.path.exists(default_model_path):
            # fallback to yolov8n if no model present (graceful)
            default_model_path = "yolov8n.pt"
        self.model = YOLO(default_model_path)

        # UI elements
        self.img_label = QLabel("图片/视频预览区")
        self.img_label.setFixedSize(800, 600)
        self.img_label.setStyleSheet("border: 1px solid #888;")
        self.img_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.btn_load_image = QPushButton("加载图片")
        self.btn_load_image.clicked.connect(self.load_image)

        self.btn_load_video = QPushButton("加载视频")
        self.btn_load_video.clicked.connect(self.load_video)

        self.btn_open_cam = QPushButton("打开摄像头")
        self.btn_open_cam.clicked.connect(self.open_camera)

        self.btn_stop = QPushButton("停止检测")
        self.btn_stop.clicked.connect(self.stop_detector)
        self.btn_stop.setEnabled(False)

        self.btn_save = QPushButton("保存结果")
        self.btn_save.clicked.connect(self.save_result)
        self.btn_save.setEnabled(False)

        # Confidence slider
        self.slider_conf = QSlider(Qt.Horizontal)
        self.slider_conf.setMinimum(0)
        self.slider_conf.setMaximum(100)
        self.slider_conf.setValue(30)
        self.slider_conf.setTickInterval(5)
        self.lbl_conf = QLabel("置信度阈值: 0.30")

        self.slider_conf.valueChanged.connect(self.on_conf_changed)

        # Frame rate control for webcam
        self.lbl_fps = QLabel("摄像头间隔(ms):")
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(30, 2000)
        self.spin_interval.setValue(100)  # 100 ms ~ 10 FPS

        # Table for class counts
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["类别", "数量"])
        self.table.setFixedWidth(250)

        # Layouts
        left_v = QVBoxLayout()
        left_v.addWidget(self.img_label)
        left_v.addSpacing(6)
        h2 = QHBoxLayout()
        h2.addWidget(self.btn_load_image)
        h2.addWidget(self.btn_load_video)
        h2.addWidget(self.btn_open_cam)
        h2.addWidget(self.btn_stop)
        h2.addWidget(self.btn_save)
        left_v.addLayout(h2)

        conf_h = QHBoxLayout()
        conf_h.addWidget(self.lbl_conf)
        conf_h.addWidget(self.slider_conf)
        left_v.addLayout(conf_h)

        fps_h = QHBoxLayout()
        fps_h.addWidget(self.lbl_fps)
        fps_h.addWidget(self.spin_interval)
        left_v.addLayout(fps_h)

        main_h = QHBoxLayout()
        main_h.addLayout(left_v)
        main_h.addWidget(self.table)

        self.setLayout(main_h)

        # detector thread handle
        self.detector_thread = None
        self.current_annotated = None  # last annotated BGR image
        self.current_counts = {}
        self.current_result_obj = None

    def on_conf_changed(self, v):
        val = v / 100.0
        self.lbl_conf.setText(f"置信度阈值: {val:.2f}")

    def load_image(self):
        self.stop_detector()
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", ".", "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        # start a detector thread for single image
        conf = self.slider_conf.value() / 100.0
        self.detector_thread = DetectorThread(self.model, path, conf_thres=conf, is_video=False)
        self.detector_thread.result_ready.connect(self.on_result_ready)
        self.detector_thread.finished_signal.connect(self.on_finished)
        self.btn_stop.setEnabled(True)
        self.detector_thread.start()

    def load_video(self):
        self.stop_detector()
        path, _ = QFileDialog.getOpenFileName(self, "选择视频", ".", "Videos (*.mp4 *.avi *.mov *.mkv)")
        if not path:
            return
        conf = self.slider_conf.value() / 100.0
        interval = self.spin_interval.value() / 1000.0
        self.detector_thread = DetectorThread(self.model, path, conf_thres=conf, is_video=True, frame_rate=interval)
        self.detector_thread.result_ready.connect(self.on_result_ready)
        self.detector_thread.finished_signal.connect(self.on_finished)
        self.btn_stop.setEnabled(True)
        self.detector_thread.start()

    def open_camera(self):
        self.stop_detector()
        # try camera index 0
        conf = self.slider_conf.value() / 100.0
        interval = self.spin_interval.value() / 1000.0
        self.detector_thread = DetectorThread(self.model, 0, conf_thres=conf, is_video=True, frame_rate=interval)
        self.detector_thread.result_ready.connect(self.on_result_ready)
        self.detector_thread.finished_signal.connect(self.on_finished)
        self.btn_stop.setEnabled(True)
        self.detector_thread.start()

    def stop_detector(self):
        if self.detector_thread and self.detector_thread.isRunning():
            try:
                self.detector_thread.stop()
                self.detector_thread.wait(timeout=2000)
            except Exception:
                pass
        self.btn_stop.setEnabled(False)

    def on_result_ready(self, annotated_bgr, counts, result_obj):
        # update display
        self.current_annotated = annotated_bgr
        self.current_counts = counts
        self.current_result_obj = result_obj
        pix = cvimg_to_qpixmap(annotated_bgr)
        # scale pixmap to label size while keeping aspect
        pix = pix.scaled(self.img_label.size(), Qt.KeepAspectRatio)
        self.img_label.setPixmap(pix)
        # update table
        self.table.setRowCount(0)
        items = sorted(counts.items(), key=lambda x: -x[1])
        for i, (name, c) in enumerate(items):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(name)))
            self.table.setItem(i, 1, QTableWidgetItem(str(c)))
        self.btn_save.setEnabled(True)

    def on_finished(self):
        self.btn_stop.setEnabled(False)

    def save_result(self):
        if self.current_annotated is None:
            QMessageBox.information(self, "提示", "暂无结果可保存")
            return
        # ask where to save image
        path, _ = QFileDialog.getSaveFileName(self, "保存标注图片", "result.jpg", "Images (*.jpg *.png)")
        if not path:
            return
        # write BGR image with OpenCV
        try:
            cv2.imwrite(path, self.current_annotated)
            QMessageBox.information(self, "保存成功", f"已保存到: {path}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))


# ---------------------------
# Run
# ---------------------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
