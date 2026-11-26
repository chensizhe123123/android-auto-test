"""启动与 GPS 开关（对应 TC-01 / TC-02 / TC-03 / TC-04）。"""
import time

from uiautomator2 import Device

from pages.base_page import PKG, dismiss_dialogs
from pages.status_page import StatusPage


def test_tc01_cold_start_after_clear_data(device: Device):
    """TC-01：清除数据（恢复首次安装状态）后冷启动，应进入 Status 页。"""
    print("\n[TC-01] pm clear:", device.shell(f"pm clear {PKG}"))
    for perm in ("android.permission.ACCESS_FINE_LOCATION",
                 "android.permission.ACCESS_COARSE_LOCATION"):
        device.shell(f"pm grant {PKG} {perm}")

    device.app_start(PKG, stop=True)
    print("[TC-01] 当前 Activity:", device.app_current()["activity"])

    # 清数据后首次启动会弹 What's New 弹窗，必须先清掉，否则页面元素被遮挡
    print("[TC-01] 关闭弹窗:", dismiss_dialogs(device))

    page = StatusPage(device)
    assert page.wait_loaded(timeout=15), "清数据冷启动后未进入 Status 页"
    assert page.find_text(r"Lat") is not None, "Status 页缺少 Lat 字段"


def test_tc02_switch_default_on(app: Device):
    """TC-02：启动后 GPS 开关默认开启。"""
    page = StatusPage(app)
    page.goto("Status")
    assert page.wait_loaded(), "未进入 Status 页"
    assert page.gps_on(), "GPS 开关默认不是开启状态"


def test_tc03_values_freeze_when_off(app: Device):
    """TC-03：关闭开关后 Status 数值冻结不再更新。"""
    page = StatusPage(app)
    page.goto("Status")
    assert page.wait_loaded(), "未进入 Status 页"
    page.set_gps(on=False)
    time.sleep(2)
    t1 = page.fix_time(timeout=3)
    time.sleep(3)
    t2 = page.fix_time(timeout=3)
    print(f"\n[TC-03] Time 采样: {t1!r} -> {t2!r}")
    assert not (t1 and t2 and t1 != t2), f"关闭开关后数值仍在更新: {t1} -> {t2}"


def test_tc04_values_resume_when_on(app: Device):
    """TC-04：重新开启开关后数值恢复刷新。"""
    page = StatusPage(app)
    page.goto("Status")
    assert page.wait_loaded(), "未进入 Status 页"
    page.set_gps(on=False)
    time.sleep(2)
    page.set_gps(on=True)
    t1 = page.fix_time(timeout=15)
    assert t1 is not None, "开启后 15 秒内未读到 Time 字段"
    time.sleep(3)
    t2 = page.fix_time(timeout=5)
    print(f"\n[TC-04] Time 采样: {t1!r} -> {t2!r}")
    assert t2 is not None, "开启开关 3 秒后 Time 字段消失"
    assert t1 != t2, f"开启开关后数值未恢复更新: {t1} == {t2}"
