"""抓取当前页面控件树，输出 resource-id / text 摘要，供编写 Page Object 使用。
用法: python tools/dump_ui.py <输出文件名>
"""
import re
import sys
import uiautomator2 as u2

PKG = "com.android.gpstest"
out = sys.argv[1] if len(sys.argv) > 1 else "ui_dump.xml"
d = u2.connect()
xml = d.dump_hierarchy()
with open(out, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"[saved] {out}  {len(xml)} chars")
ids = sorted(set(re.findall(rf'resource-id="({PKG}[^"]*)"', xml)))
print(f"[ids] {len(ids)}")
for i in ids:
    print("   ", i.replace(PKG + ":id/", ""))
texts = [t for t in re.findall(r'text="([^"]+)"', xml) if t.strip()]
print(f"[texts] {len(texts)}")
print("   ", " | ".join(texts[:40]))
