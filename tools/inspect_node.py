"""按文字筛选控件节点，打印 class / id / desc / clickable / bounds。
用法: python tools/inspect_node.py <xml文件> "文字1|文字2"
"""
import sys
import xml.etree.ElementTree as ET

path = sys.argv[1]
targets = sys.argv[2].split("|")
root = ET.parse(path).getroot()
for n in root.iter("node"):
    t = n.get("text", "")
    if t and (t in targets or t.startswith(tuple(targets))):
        cls = (n.get("class") or "").split(".")[-1]
        rid = (n.get("resource-id") or "").split("/")[-1]
        print(f"{t} | class={cls} | id={rid} | desc={n.get('content-desc')} | clickable={n.get('clickable')} | bounds={n.get('bounds')}")
