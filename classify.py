import re
import os

def classify_scripts(input_folder, output_folder_with_numbers, output_folder_without_numbers):
    # 创建输出文件夹
    if not os.path.exists(output_folder_with_numbers):
        os.makedirs(output_folder_with_numbers)
    if not os.path.exists(output_folder_without_numbers):
        os.makedirs(output_folder_without_numbers)

    # 遍历输入文件夹中的剧本
    for filename in os.listdir(input_folder):
        input_filepath = os.path.join(input_folder, filename)
        try:
            with open(input_filepath, 'r', encoding='utf-8') as file:
                script_content = file.read()

                # 使用正则表达式检测剧本中是否包含数字后跟着点或者顿号
                if re.search(r'\n+\d+[.、\s]', script_content):
                        output_filepath = os.path.join(output_folder_with_numbers, filename)
                else:
                    output_filepath = os.path.join(output_folder_without_numbers, filename)

                # 将剧本内容写入相应的输出文件夹
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(script_content)
        except UnicodeDecodeError:
            print(f"Error reading file {filename}: UnicodeDecodeError")
    

if __name__ == "__main__":
    input_folder = "jubenPro"
    output_folder_with_numbers = "output_scripts_with_numbers"
    output_folder_without_numbers = "output_scripts_without_numbers"

    classify_scripts(input_folder, output_folder_with_numbers, output_folder_without_numbers)