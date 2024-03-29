import os
import re

def add_scene_numbers(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        scene_count = 0
        output_lines = []

        for line in lines:
            # 检测行中是否存在"内景"或"外景"字样，且行开头不为数字
            if ("内景" in line or "外景" in line) and not line.strip()[0].isdigit():
                scene_count += 1
                # 在行的开头添加数字序号
                line = f"{scene_count}. {line}"

            output_lines.append(line)

        # 保存到输出文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(output_lines)

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"Error processing file: {e}")



def add_scene_numbers_all():
     
    for filename in os.listdir("jubenPro"):
        input_file_path = 'jubenPro/'
        output_file_path = 'jubenPro/' 
        input_file_path+=filename
        output_file_path+=filename
        add_scene_numbers(input_file_path,output_file_path)
    return


if __name__ == "__main__":
    add_scene_numbers_all()
