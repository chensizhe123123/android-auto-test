"""pytest 全局配置：设备连接、每条用例冷启动、失败自动截图。"""
import os
import time

import pytest
import uiautomator2 as u2

PKG = "com.android.gpstest"

os.makedirs("reports", exist_ok=True)


@pytest.fixture(scope="session")
def device():
    """整个测试会话只连一次设备。"""
    d = u2.connect()
    d.settings["wait_timeout"] = 10
    return d


@pytest.fixture()
def app(device, request):
    """每条用例前冷启动 App，保证用例之间互不污染。"""
    device.app_start(PKG, stop=True)
    time.sleep(3)
    yield device
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        path = f"reports/failure_{request.node.name}_{int(time.time())}.png"
        device.screenshot(path)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
