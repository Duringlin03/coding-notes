import os
import random
import shutil
from PIL import Image

# 原始数据集（你下载的路径）
BASE_DIR = r"D:\code\fruit_detection\data\Fruits-360 dataset\fruits-360_original-size\fruits-360-original-size"

TRAIN_DIR = os.path.join(BASE_DIR, "Training")
TEST_DIR = os.path.join(BASE_DIR, "Test")

OUTPUT_DIR = r"D:\code\fruit_detection\data\yolo_fruit"

# 创建目标目录结构
for folder in ["images/train", "images/val", "labels/train", "labels/val"]:
    os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

# 获取类别目录
classes = sorted(os.listdir(TRAIN_DIR))
class_to_id = {cls: idx for idx, cls in enumerate(classes)}

print("检测到类别数量:", len(classes))


def convert_folder(src_folder, cls_name, mode):
    """将单个类别文件夹转换为 YOLO 格式"""
    cls_id = class_to_id[cls_name]
    img_files = os.listdir(src_folder)

    for img_name in img_files:
        img_path = os.path.join(src_folder, img_name)

        # 跳过非图片文件
        if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        # 打开图像
        img = Image.open(img_path)
        w, h = img.size

        # 自动生成一个居中的大 bbox（80%）
        x, y = 0.5, 0.5
        bw, bh = 0.8, 0.8

        # 写入标签文件
        label_path = os.path.join(OUTPUT_DIR, f"labels/{mode}", img_name.replace(".jpg", ".txt"))
        with open(label_path, "w") as f:
            f.write(f"{cls_id} {x} {y} {bw} {bh}")

        # 复制图像
        shutil.copy(img_path, os.path.join(OUTPUT_DIR, f"images/{mode}", img_name))


# 处理训练集
print("开始转换 Training 数据...")
for cls in classes:
    cls_folder = os.path.join(TRAIN_DIR, cls)
    convert_folder(cls_folder, cls, mode="train")

# 处理验证集（使用 Test 作为 val）
print("开始转换 Test 数据...")
for cls in classes:
    cls_folder = os.path.join(TEST_DIR, cls)
    convert_folder(cls_folder, cls, mode="val")

print("转换完成！")

# 写 data.yaml
yaml_path = os.path.join(OUTPUT_DIR, "data.yaml")
with open(yaml_path, "w") as f:
    f.write(f"train: {OUTPUT_DIR}/images/train\n")
    f.write(f"val: {OUTPUT_DIR}/images/val\n")
    f.write(f"nc: {len(classes)}\n")
    f.write("names: [\n")
    for cls in classes:
        f.write(f"  '{cls}',\n")
    f.write("]\n")

print("data.yaml 已生成。全部完成！")
