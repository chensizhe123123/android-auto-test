"""侦察：依次进入各页面，打印该页独占的文字与当前 Activity。"""
import re
import time

import uiautomator2 as u2

from pages.base_page import BasePage, dismiss_dialogs

d = u2.connect()
d.app_start("com.android.gpstest", stop=True)
time.sleep(4)
dismiss_dialogs(d, rounds=1, timeout=1)

base = BasePage(d)
for name in ("Status", "Sky", "Map", "Accuracy", "Settings"):
    base.goto(name)
    time.sleep(2)
    act = d.app_current()["activity"]
    texts = [t for t in re.findall(r'text="([^"]*)"', d.dump_hierarchy()) if t.strip()]
    print(f"=== {name} | activity={act} | 文本节点数={len(texts)}")
    print("   " + " | ".join(texts[:35]))
    print()
