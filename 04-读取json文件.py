import json


# 定义json文件所在的路径
file_path = './json/class.json'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# print(f"读取的内容是：\n{content}")
# print(f"读取的json文件内容的数据类型是：{type(content)}")

# 提取这个班级的所有学生的姓名
# 需要将json格式的字符串转换成python的字典类型
py_obj = json.loads(content)
# print(py_obj)
# print(type(py_obj))

# 遍历所有的学生
for stu in py_obj['students']:
    print(f"学生的姓名是：{stu['name']}")
