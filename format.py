import os
import re
from jieba import posseg
import jieba
def format(line_process_by_re:list,line_process_by_jieba:list):
    scene_info = {
        "场景编号": None,
        "地点名称":None,
        "内外景": None,
        "日或夜": None
    }

    if line_process_by_re and len(line_process_by_re) > 0:
        no_chinese = re.sub(r'[\u4e00-\u9fa5]', '', line_process_by_re[0])
        scene_info["场景编号"] = no_chinese
        line_process_by_re.remove(line_process_by_re[0])

        for word in line_process_by_re:
            if "日" in word or "白天" in word:
                scene_info["日或夜"] = "日"
            elif "夜" in word or "晚" in word:
                scene_info["日或夜"] = "夜"
            if "内" in word:
                scene_info["内外景"] = "内"
            elif "外" in word:
                scene_info["内外景"] = "外"

    jieba_list=process_pair_list(line_process_by_jieba)

    for map in jieba_list:
        for key, value in map.items():        
            if (value == "n" or value == "ns" or value=="nr" or value=="v" or value=="s" )and key != "内" and "key" !="外" and key != "内景" and key !="外景":
                if scene_info["地点名称"]:
                    scene_info["地点名称"] += key
                else:
                    scene_info["地点名称"] = key
    return scene_info

def process_format(scene_info_dict):
    result=""
    if scene_info_dict['场景编号'] is not None:
        result += f"{scene_info_dict['场景编号']}.  "
    if scene_info_dict['地点名称'] is not None:
        result += f"{scene_info_dict['地点名称']}  "
    if scene_info_dict['内外景'] is not None:
        result += f"{scene_info_dict['内外景']}  "
    if scene_info_dict['日或夜'] is not None:
        result += f" {scene_info_dict['日或夜']}"
    result +="\n"
    return result

def process_pair_list(pair_list):
    result_list = []

    for pair in pair_list:
        pair_str = str(pair)
        elements = pair_str.split('/')

        if len(elements) == 2:
            key = elements[0]
            value = elements[1]

            result_list.append({key: value})
        else:
            print(f"Pair format error: {pair_str}")

    return result_list

def format_by_re(line):
    # 去除括号及括号内的内容
    clean_line = re.sub(r'（[^（）]*）', '', line)
    
    # 使用正则表达式匹配非汉字和非数字字符进行分割
    non_chinese_pattern = re.compile(r'[^0-9\u4e00-\u9fa5]+')
    segments = re.split(non_chinese_pattern, clean_line)
    segments.remove("")
    
    return segments
def format_by_jieba(line):
    process=posseg.lcut(line,use_paddle=True)
    return process

def process_by_jieba(line):
    word=jieba.cut(line,cut_all=False)
    return word

def read_file_by_line(file_path):
    lines = []
    formatted_lines = []
    file_name = os.path.basename(file_path)
    file_name_without_extension = "《"+os.path.splitext(file_name)[0]+"》"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        keyword=[]
        for index, line in enumerate(lines):
            if index >= 1:
                word = process_by_jieba(line)
                if line.strip() and line.strip()[0].isdigit():
                    break
                keyword += word
        if "翻译" in keyword or "译出" in keyword or "译" in keyword or "编译" in keyword:
            file_name_without_extension += ";外;原创"
        if "整理" in keyword:
            file_name_without_extension+=";网络"
        print(keyword)
        for line in lines:
            #这里有问题！！！and (line.strip()[1]=='.'or line.strip()[1]=='、')
            if line.strip() and line.strip()[0].isdigit() :
                formatted_lines.append(process_format(format(format_by_re(line),format_by_jieba(line))))
            else:
                formatted_lines.append(line)
        with open(f"formatted/{file_name_without_extension}.txt", 'w', encoding='utf-8') as output_file:
            output_file.writelines(formatted_lines)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")
    return lines

def format_all():
    for filename in os.listdir("output_scripts_with_numbers"):
        input_file_path = os.path.join("output_scripts_with_numbers", filename)
        read_file_by_line(input_file_path)
    return


if __name__ == "__main__":
    format_all()

