if __name__ == '__main__':
    from ultralytics import YOLO

    model = YOLO("yolov8s.yaml")
    results = model.train(data=r"C:\Users\colet\Documents\GitHub\Pantry-Detection\Algorithms\YOLOv8\coco8.yaml", epochs=35, device = 0)

# on 203-b computer:
# installed cuda 12.1
# installed pytorch: pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
# the cu121 at the end stands for cuda 12.1
# make sure to run nvidia-smi and check for cuda 12.1 compare with nvcc --version for cuda 12.1 as well
# add cuda 12.1 to path: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1
