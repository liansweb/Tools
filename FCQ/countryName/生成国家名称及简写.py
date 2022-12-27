import  re
import yaml

path = "国家名称及简写.txt"

countryNameDict = {}

with open(path,"r") as fp:
    a = fp.readlines()
    for i in a:
        if re.search("China",str(i)):
            continue
        b = re.match("(\w+)\s-\s\w+\s(.+)",str(i))
        if b:
            if re.search("[a-zA-Z]+",str(b[2])):
                c = re.match("[a-zA-Z\s()]+(.+)",str(b[2]))[1]
                countryNameDict[c]=b[1]
            else:
                countryNameDict[b[2]]=b[1]

yamlPath = "国家名称及简写.yaml"
with open(yamlPath, "w") as f:  # 写文件
    yaml.safe_dump(data=countryNameDict, stream=f,default_flow_style=False,encoding='utf-8',allow_unicode=True)

