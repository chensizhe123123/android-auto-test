"""页面导航（对应 TC-05 / TC-06 / TC-07）。"""
from uiautomator2 import Device

from pages.base_page import BasePage


def test_tc05_status_to_sky(app: Device):
    """TC-05：Status 切到 Sky，Sky 图例正常渲染。"""
    base = BasePage(app)
    base.goto("Status")
    assert base.wait_title("Status"), "未进入 Status 页"
    base.goto("Sky")
    assert base.wait_title("Sky"), "Status -> Sky 切换失败"
    assert base.poll(r"Global Navigation Satellite Systems", timeout=10) is not None, \
        "Sky 页 10 秒内未渲染图例"


def test_tc06_sky_to_map(app: Device):
    """TC-06：Sky 切到 Map，标题变为 Map 且不再显示 Status 字段。"""
    base = BasePage(app)
    base.goto("Sky")
    assert base.wait_title("Sky"), "未进入 Sky 页"
    base.goto("Map")
    assert base.wait_title("Map"), "Sky -> Map 切换失败"
    assert base.find_text(r"^Lat:$") is None, "Map 页仍显示 Status 字段，切换异常"


def test_tc07_map_to_accuracy(app: Device):
    """TC-07：Map 切到 Accuracy，表单页正常显示。"""
    base = BasePage(app)
    base.goto("Map")
    assert base.wait_title("Map"), "未进入 Map 页"
    base.goto("Accuracy")
    assert base.wait_title("Accuracy"), "Map -> Accuracy 切换失败"
    assert base.find_text(r"Measure accuracy|SAVE") is not None, "Accuracy 页缺少表单标记"
