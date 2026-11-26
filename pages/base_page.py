"""页面对象基类：工具栏、抽屉导航、控件树查询等公共能力。

实测结论：
1. 抽屉菜单项在实时控件树里是 TextView（id 复用模板），与工具栏标题文字重名，
   按纯 text 定位会命中多个节点 -> 改为在抽屉容器内部按文字查找并坐标点击。
2. id=title 不稳定 -> 页面判断改为读取"工具栏区域内(y<300)的标题文字"。
"""
import re
import time
import xml.etree.ElementTree as ET

PKG = "com.android.gpstest"
DRAWER_IDS = (f"{PKG}:id/nav_drawer_left_pane", f"{PKG}:id/navigation_drawer")
TITLES = ("Status", "Sky", "Map", "Accuracy", "Settings", "Help")
TOOLBAR_BOTTOM = 300


class BasePage:
    def __init__(self, d):
        self.d = d

    # ---------- 工具栏 ----------
    def gps_switch(self):
        return self.d(resourceId=f"{PKG}:id/gps_switch")

    def gps_on(self):
        return self.gps_switch().info.get("checked") is True

    def set_gps(self, on=True):
        if self.gps_on() != on:
            self.gps_switch().click()
            time.sleep(1.5)
        return self

    def share_button(self):
        return self.d(resourceId=f"{PKG}:id/share")

    # ---------- 控件树查询 ----------
    def _tree(self):
        root = ET.fromstring(self.d.dump_hierarchy())
        parents = {c: p for p in root.iter() for c in p}
        return root.iter("node"), parents

    def all_texts(self):
        return re.findall(r'text="([^"]*)"', self.d.dump_hierarchy())

    def find_text(self, pattern):
        for t in self.all_texts():
            if re.search(pattern, t):
                return t
        return None

    def poll(self, pattern, timeout=10, interval=0.5):
        deadline = time.time() + timeout
        while time.time() < deadline:
            t = self.find_text(pattern)
            if t is not None:
                return t
            time.sleep(interval)
        return None

    def current_title(self):
        """读取工具栏区域的页面标题（避开抽屉里的同名菜单项）。"""
        nodes, _ = self._tree()
        for n in nodes:
            t = (n.get("text") or "").strip()
            if t not in TITLES:
                continue
            b = re.findall(r"\d+", n.get("bounds") or "")
            if len(b) == 4 and int(b[1]) < TOOLBAR_BOTTOM:
                return t
        return None

    def wait_title(self, expected, timeout=15):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.current_title() == expected:
                return True
            dismiss_anr(self.d)
            time.sleep(0.5)
        return False

    def find_text_node(self, text):
        """在抽屉容器内部按文字查找节点。"""
        nodes, parents = self._tree()
        for n in nodes:
            if (n.get("text") or "").strip() != text:
                continue
            p = parents.get(n)
            while p is not None:
                if p.get("resource-id") in DRAWER_IDS:
                    return n
                p = parents.get(p)
        return None

    @staticmethod
    def bounds_center(node):
        x1, y1, x2, y2 = (int(v) for v in re.findall(r"\d+", node.get("bounds")))
        return (x1 + x2) // 2, (y1 + y2) // 2

    def tap_node(self, node):
        x, y = self.bounds_center(node)
        self.d.click(x, y)
        return self

    # ---------- 抽屉导航 ----------
    def drawer_open(self):
        return self.d(className="android.widget.ImageButton",
                      description="Close navigation drawer").exists(timeout=1)

    def open_drawer(self):
        if not self.drawer_open():
            self.d(className="android.widget.ImageButton",
                   description="Open navigation drawer").click()
            time.sleep(1)
        return self

    def goto(self, name, timeout=8):
        dismiss_anr(self.d)
        self.open_drawer()
        deadline = time.time() + timeout
        node = None
        while time.time() < deadline:
            node = self.find_text_node(name)
            if node is not None:
                break
            dismiss_anr(self.d)
            time.sleep(0.5)
        if node is None:
            raise AssertionError(f"抽屉中找不到菜单项: {name}")
        self.tap_node(node)
        time.sleep(1.5)
        return self


# ---------- 通用：首次启动弹窗处理 ----------
DIALOG_TEXTS = ("While using the app", "仅在使用中允许", "CLOSE", "GOT IT", "OK", "不允许")


def dismiss_dialogs(d, rounds=2, timeout=1):
    """关闭可能出现的弹窗（权限框 / What's New / 提示框），返回实际关闭的按钮文字。"""
    closed = []
    for _ in range(rounds):
        for label in DIALOG_TEXTS:
            el = d(text=label)
            if el.exists(timeout=timeout):
                el.click()
                closed.append(label)
                time.sleep(1)
                break
    return closed


# ---------- 已知缺陷规避：ANR 弹窗 ----------
ANR_TEXTS = ("Wait", "等待")


def dismiss_anr(d, timeout=0.5):
    """若出现 ANR 弹窗（GPSTest isn't responding），点 Wait 让应用恢复。

    说明：GPSTest 存在主线程阻塞缺陷（Issue #1），会不时弹出 ANR 框。
    自动化里必须识别并放行，否则弹窗会遮挡页面元素，导致用例随机失败。
    """
    for label in ANR_TEXTS:
        el = d(text=label)
        if el.exists(timeout=timeout):
            el.click()
            time.sleep(2)
            return label
    return None
