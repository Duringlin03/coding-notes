from ultralytics import YOLO
import cv2
from collections import Counter

# 1. 加载模型
model = YOLO(r"D:\code\fruit_detection\runs\detect\train4\weights\best.pt")

# 2. 输入图片路径
img_path = r"D:\code\fruit_detection\apple.jpg"

# 3. 推理
results = model.predict(img_path, save=True)

# 4. 解析结果：统计水果数量
fruit_list = []

for r in results:
    boxes = r.boxes
    names = r.names  # 类别名称列表

    for box in boxes:
        cls_id = int(box.cls[0])   # 类别ID
        fruit_name = names[cls_id]  # 类别名称
        fruit_list.append(fruit_name)

# 使用 Counter 统计各类水果数量
count_result = Counter(fruit_list)

# 5. 打印统计结果
print("=== 水果识别与计数结果 ===")
total = 0
for fruit, num in count_result.items():
    print(f"{fruit}: {num} 个")
    total += num

print(f"\n总计检测到：{total} 个水果")
print("\n预测完成，检测结果已保存！")
