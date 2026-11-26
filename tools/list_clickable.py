"""列出可点击节点和按钮类节点，用于找无 id 的控件（如抽屉按钮）。
用法: python tools/list_clickable.py <xml文件>
"""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
for n in root.iter("node"):
    cls = (n.get("class") or "").split(".")[-1]
    rid = (n.get("resource-id") or "").split("/")[-1]
    desc = n.get("content-desc") or ""
    text = n.get("text") or ""
    if n.get("clickable") == "true" or desc or cls == "ImageButton":
        print(f"class={cls:<18} id={rid:<22} desc={desc:<28} text={text:<20} bounds={n.get('bounds')}")
