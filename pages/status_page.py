"""Status 页对象。"""
import re

from .base_page import BasePage


class StatusPage(BasePage):
    TITLE = "Status"
    FIX_TIME_RE = r"\d{1,2}:\d{2}:\d{2}\.\d+\s*(?:AM|PM)"

    def wait_loaded(self, timeout=10):
        return self.wait_title("Status", timeout)

    def fix_time(self, timeout=10):
        """取状态页 Time 字段（每收到一次定位解算就刷新）。"""
        return self.poll(self.FIX_TIME_RE, timeout=timeout)

    def sats_text(self):
        return self.find_text(r"\d+/\d+/\d+")
