import sys
import os
import cv2
import numpy as np
from ultralytics import YOLO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# ==== 配置区（根据你的路径修改） ====
MODEL_PATH = r"D:\code\fruit_detection\runs\detect\train4\weights\best.pt"
# =====================================

class InferenceWorker(QtCore.QThread):
    """在后台线程中运行模型推理，避免阻塞主线程"""
    result_ready = QtCore.pyqtSignal(np.ndarray, dict)  # annotated_image, counts

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.frame = None
        self._running = False
        self._single = True

    def infer_once(self, frame):
        """触发一次推理（非循环）"""
        self.frame = frame
        self._single = True
        if not self.isRunning():
            self.start()

    def start_stream(self, frame):
        """开始流式推理（不断推理到 stop_stream 被调用）"""
        self.frame = frame
        self._single = False
        self._running = True
        if not self.isRunning():
            self.start()

    def stop_stream(self):
        self._running = False

    def run(self):
        while True:
            if self.frame is None:
                return
            # copy the frame to avoid mutation race conditions
            frame = self.frame.copy()

            # run ultralytics model on frame (BGR numpy)
            try:
                results = self.model(frame)  # ultralytics handles numpy
                r = results[0]

                # annotated image (numpy BGR)
                annotated = r.plot()  # returns numpy array with boxes drawn

                # extract counts
                counts = {}
                # r.boxes.cls is a tensor of class indices or None if no boxes
                try:
                    cls_inds = r.boxes.cls.tolist() if hasattr(r.boxes, "cls") and r.boxes.cls is not None else []
                except Exception:
                    # fallback: loop boxes
                    cls_inds = []
                    try:
                        for box in r.boxes:
                            cls_inds.append(int(box.cls))
                    except Exception:
                        cls_inds = []

                # get names mapping
                try:
                    names = r.names if hasattr(r, "names") else self.model.names
                except Exception:
                    names = {}

                for ci in cls_inds:
                    cname = names[int(ci)] if int(ci) in names else str(ci)
                    counts[cname] = counts.get(cname, 0) + 1

                self.result_ready.emit(annotated, counts)
            except Exception as e:
                print("Inference error:", e)
                self.result_ready.emit(frame, {})  # return raw frame on error

            if self._single:
                return
            if not self._running:
                return
            # small sleep to avoid hogging CPU/GPU
            self.msleep(20)


class FruitDetectorGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("水果识别与计数系统 - PyQt GUI")
        self.setGeometry(150, 100, 1100, 720)

        # Load model (this may take a moment)
        try:
            self.model = YOLO(MODEL_PATH)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "模型加载失败", f"无法加载模型：{e}")
            raise

        # UI 元件
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # 左侧：图像显示区
        left = QtWidgets.QVBoxLayout()
        self.image_label = QtWidgets.QLabel("图片/视频帧将在这里显示")
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #222; color: #ddd;")
        left.addWidget(self.image_label)

        # 下方按钮
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_load = QtWidgets.QPushButton("加载图片")
        self.btn_detect = QtWidgets.QPushButton("检测图片")
        self.btn_camera = QtWidgets.QPushButton("打开摄像头")
        self.btn_stopcam = QtWidgets.QPushButton("关闭摄像头")
        self.btn_save = QtWidgets.QPushButton("保存结果")
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_detect)
        btn_layout.addWidget(self.btn_camera)
        btn_layout.addWidget(self.btn_stopcam)
        btn_layout.addWidget(self.btn_save)
        left.addLayout(btn_layout)

        layout.addLayout(left)

        # 右侧：信息面板
        right = QtWidgets.QVBoxLayout()
        self.info_label = QtWidgets.QLabel("识别结果")
        self.info_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        right.addWidget(self.info_label)

        self.counts_text = QtWidgets.QTextEdit()
        self.counts_text.setReadOnly(True)
        self.counts_text.setFixedWidth(260)
        right.addWidget(self.counts_text)

        right.addStretch()
        layout.addLayout(right)

        # 状态
        self.current_image = None  # numpy BGR
        self.annotated_image = None
        self.cam = None
        self.streaming = False

        # Worker 线程
        self.worker = InferenceWorker(self.model)
        self.worker.result_ready.connect(self.on_result_ready)

        # 绑定信号
        self.btn_load.clicked.connect(self.load_image)
        self.btn_detect.clicked.connect(self.detect_current_image)
        self.btn_camera.clicked.connect(self.start_camera)
        self.btn_stopcam.clicked.connect(self.stop_camera)
        self.btn_save.clicked.connect(self.save_result)

    def load_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
        if not path:
            return
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)  # 支持中文路径
        if img is None:
            QtWidgets.QMessageBox.warning(self, "打开失败", "无法读取该图片。")
            return
        self.current_image = img
        self.annotated_image = img.copy()
        self.show_image(self.annotated_image)
        self.counts_text.clear()
        self.info_label.setText(f"图片：{os.path.basename(path)}")

    def detect_current_image(self):
        if self.current_image is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先加载一张图片。")
            return
        # 启动一次性推理
        self.worker.infer_once(self.current_image)

    def start_camera(self):
        if self.streaming:
            return
        # 打开摄像头（索引 0），如果使用外接摄像头可以改为 1/2...
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cam.isOpened():
            QtWidgets.QMessageBox.critical(self, "摄像头打开失败", "无法打开摄像头，请检查设备或更换索引。")
            return
        self.streaming = True
        # 启动流式推理（先读取一帧触发）
        ret, frame = self.cam.read()
        if not ret:
            QtWidgets.QMessageBox.critical(self, "摄像头读取失败", "无法读取摄像头帧。")
            self.cam.release()
            self.cam = None
            self.streaming = False
            return
        self.worker.start_stream(frame)
        # 启动一个定时器刷新界面（在主线程显示最新 annotated_image）
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._camera_loop)
        self.timer.start(30)

    def _camera_loop(self):
        if not self.streaming or self.cam is None:
            return
        ret, frame = self.cam.read()
        if not ret:
            return
        # 更新当前帧供 worker 使用
        self.worker.frame = frame
        # show latest annotated if exists, else show raw frame
        if self.annotated_image is not None:
            self.show_image(self.annotated_image)
        else:
            self.show_image(frame)

    def stop_camera(self):
        if not self.streaming:
            return
        self.streaming = False
        if hasattr(self, "timer"):
            self.timer.stop()
        if self.cam:
            self.cam.release()
            self.cam = None
        self.worker.stop_stream()
        self.info_label.setText("摄像头已关闭")

    def save_result(self):
        if self.annotated_image is None:
            QtWidgets.QMessageBox.information(self, "提示", "没有可保存的检测结果。")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存检测结果", "result.jpg", "JPEG Files (*.jpg);;PNG Files (*.png)")
        if not path:
            return
        # cv2.imwrite 对中文路径不稳定，使用 imencode + tofile
        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            ret, enc = cv2.imencode(".jpg", self.annotated_image)
        else:
            ret, enc = cv2.imencode(".png", self.annotated_image)
        if ret:
            enc.tofile(path)
            QtWidgets.QMessageBox.information(self, "已保存", f"检测结果已保存到：\n{path}")
        else:
            QtWidgets.QMessageBox.warning(self, "保存失败", "图像保存失败。")

    def on_result_ready(self, annotated, counts):
        """接收 worker 发来的结果并显示"""
        self.annotated_image = annotated
        self.show_image(annotated)
        # 更新统计文本
        if counts:
            lines = [f"{k}: {v} 个" for k, v in sorted(counts.items(), key=lambda x: -x[1])]
            total = sum(counts.values())
            lines.append(f"\n总计检测到：{total} 个水果")
            self.counts_text.setPlainText("\n".join(lines))
            self.info_label.setText("检测完成")
        else:
            self.counts_text.setPlainText("未检测到水果或发生错误。")
            self.info_label.setText("检测完成（无结果）")

    def show_image(self, img_bgr):
        """将 BGR numpy 转为 Qt 可显示的 QImage 并显示到 QLabel"""
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QtGui.QImage(img_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # 缩放以适应 label
        pixmap = QtGui.QPixmap.fromImage(qimg).scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FruitDetectorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
