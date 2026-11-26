# GPSTest 测试计划

## 1. 被测对象

- 应用：GPSTest（包名 `com.android.gpstest`），开源 GNSS 测试工具，Apache-2.0
- 源码：`barbeau/gpstest`，master 分支
- 构建方式：`./gradlew :GPSTest:assembleGoogleDebug`，debug 签名
- 版本：versionName 3.10.6 / versionCode 24100
- 安装方式：先 `adb uninstall com.android.gpstest` 再安装（签名与官方 release 包不同，不可覆盖）

## 2. 测试环境

| 项 | 配置 |
|---|---|
| 设备 | Android Emulator Pixel 6 / Android 14（API 34）/ Google APIs x86_64 |
| 构建工具 | Gradle 8.14.3 + AGP 8.11.1 + JDK 21 |
| 调试工具 | adb 37.0.1、Android Studio 2026.1.4 |
| 自动化 | Python 3.x + uiautomator2 3.7.1 + pytest 9.2.0 + pytest-html 4.2.0 |

## 3. 测试范围

### 范围内

1. 应用启动与首屏（Status 页面结构）
2. 侧边抽屉导航（Status / Map / Sky / Accuracy / Settings / Help）
3. 工具栏 GPS 开关开与关
4. Settings：Use Dark Theme、Keep Screen On、Coordinate format、距离与速度单位、Auto-Start GNSS
5. Accuracy 页坐标输入校验（空值 / 非法值 / 边界值）
6. 工具栏分享入口

### 范围外及原因

| 不测内容 | 原因 |
|---|---|
| 卫星数量、C/N0 数值、天空图分布 | 模拟器无真实 GNSS 信号，数值恒定或为空，不可断言 |
| Map 底图加载 | 依赖 Google 地图瓦片服务，模拟器内不可用 |
| 真实定位精度统计 | 需真机与外场环境 |
| NMEA / 原始观测日志 | 需真机与长时间采集 |

## 4. 测试策略

- 设计方法：等价类划分、边界值分析、场景法
- 执行方式：先手工执行并记录缺陷（阶段 4），再把稳定用例自动化（阶段 5）
- 优先级：P0 为启动、导航、核心开关；P1 为设置项生效；P2 为展示类与次要入口
- 断言原则：只断言稳定可观测的结果（控件存在、文字内容、勾选状态），不断言随时间变化的数值

## 5. 风险与应对

| 风险 | 影响 | 应对 |
|---|---|---|
| 模拟器无 GNSS 信号 | 卫星相关功能不可测 | 明确列入范围外，报告中说明 |
| 元素无 resource-id，坐标数值为纯文本 | 定位不稳、脚本易碎 | 优先用 resourceId 与 text，必要时用 xpath，禁用坐标点击 |
| 调试包与发行包行为差异 | 结论可能不适用正式版 | 报告中标注被测包来源与签名类型 |
| 模拟器性能波动 | 界面响应慢导致超时 | 统一使用显式等待，不用固定 sleep |

## 6. 退出标准

- 用例总数不少于 15 条，其中 P0 不少于 5 条
- P0 用例 100% 通过；P1 通过率不低于 90%
- 发现的缺陷全部登记为 GitHub Issue（含环境、复现步骤、预期与实际、截图或日志）
- 输出 `docs/test-report.md` 与 pytest HTML 报告
