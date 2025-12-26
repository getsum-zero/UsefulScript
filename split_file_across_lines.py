### 按行分割文件
import argparse
from pathlib import Path

def split_file(input_file: str, num_parts: int, output_dir: str):
    """
    将一个 file 文件平均分成 num_parts 份，保存到 output_dir。
    """
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 读取所有行
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    total_lines = len(lines)
    if total_lines == 0:
        print("输入 file 文件为空。")
        return

    # 计算每部分的大小（向上取整确保均分）
    base_count = total_lines // num_parts
    remainder = total_lines % num_parts

    start = 0
    for part in range(num_parts):
        # 每部分的实际数量
        count = base_count + (1 if part < remainder else 0)
        end = start + count

        sub_lines = lines[start:end]
        part_file = output_path / f"part_{part}.txt"

        with open(part_file, 'w', encoding='utf-8') as out:
            out.writelines(line + "\n" for line in sub_lines)

        print(f"Saved part {part}: {len(sub_lines)} lines -> {part_file}")

        start = end

    print("分割完成。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将文件平均分为若干份")
    parser.add_argument(
        "--input_file", "-i", required=True,
        help="输入 文件路径"
    )
    parser.add_argument(
        "--num_parts", "-n", type=int, required=True,
        help="要分成的份数"
    )
    parser.add_argument(
        "--output_dir", "-o", default="splits",
        help="输出分割文件的目录，默认是 splits/"
    )

    args = parser.parse_args()
    split_file(args.input_file, args.num_parts, args.output_dir)
