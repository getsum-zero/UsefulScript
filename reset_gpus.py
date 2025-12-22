import torch
import time
import argparse

def main(gpu_id: int, size: int):
    torch.cuda.set_device(gpu_id)
    device = torch.device("cuda")

    print(f"Using GPU {gpu_id}: {torch.cuda.get_device_name(device)}")
    print(f"Matrix size: {size} x {size}")

    # 预先分配，避免反复 malloc
    a = torch.randn(size, size, device=device, dtype=torch.float16)
    b = torch.randn(size, size, device=device, dtype=torch.float16)

    # 预热
    for _ in range(5):
        _ = a @ b
    torch.cuda.synchronize()

    print("Running compute loop... (Ctrl+C to stop)")

    while True:
        c = a @ b
        # 防止被编译器/调度器优化掉
        c.sum().item()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--size", type=int, default=8192)
    args = parser.parse_args()

    main(args.gpu, args.size)
