from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.predict(
    source='bus.jpg',
    save=True,
    save_dir='runs/detect/demo'
)

print("检测完成，图片已保存到 runs/detect/demo")
