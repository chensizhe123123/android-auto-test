# GPSTest 测试用例表

被测版本：3.10.6（google debug 包，源码构建）
环境：Pixel 6 / Android 14 (API 34) 模拟器
设计方法：等价类划分、边界值分析、场景法
执行结果列：阶段 4 手工执行后填写

| 编号 | 模块 | 用例名 | 前置条件 | 步骤 | 预期结果 | 优先级 | 执行结果 |
|---|---|---|---|---|---|---|---|
| TC-01 | 启动 | 冷启动进入 Status 页 | App 已安装且未运行 | 1. 点击桌面 GPSTest 图标 | 进入 Status 页，标题显示 Status，可见 Lat / Long / Alt / # Sats 等标签 | P0 | 待执行 |
| TC-02 | 启动 | 启动后 GPS 开关默认状态 | Auto-Start GNSS 为勾选状态 | 1. 冷启动 App | 工具栏右侧 GPS 开关处于开启状态 | P0 | 待执行 |
| TC-03 | 开关 | 关闭 GPS 开关 | 已进入 Status 页且开关为开 | 1. 点击工具栏 GPS 开关 | 开关变为关闭状态，Status 页数值停止刷新 | P0 | 待执行 |
| TC-04 | 开关 | 重新开启 GPS 开关 | 开关处于关闭状态 | 1. 再次点击 GPS 开关 | 开关恢复开启，数值恢复刷新 | P0 | 待执行 |
| TC-05 | 导航 | Status 切换到 Sky | 已进入 Status 页 | 1. 点左上角菜单图标 2. 点击 Sky | 标题变为 Sky，页面出现极坐标天空图与图例 | P0 | 待执行 |
| TC-06 | 导航 | Sky 切换到 Map | 当前处于 Sky 页 | 1. 打开菜单 2. 点击 Map | 标题变为 Map，右上角出现定位到当前位置按钮 | P0 | 待执行 |
| TC-07 | 导航 | Map 切换到 Accuracy | 当前处于 Map 页 | 1. 打开菜单 2. 点击 Accuracy | 标题变为 Accuracy，页面显示 Measure accuracy 与三个输入框及 SAVE 按钮 | P0 | 待执行 |
| TC-08 | 导航 | Accuracy 切换到 Settings | 当前处于 Accuracy 页 | 1. 打开菜单 2. 点击 Settings | 标题变为 Settings，显示 Display / GNSS / Map 三组设置项 | P1 | 待执行 |
| TC-09 | 导航 | Settings 切换到 Help | 当前处于 Settings 页 | 1. 打开菜单 2. 点击 Help | 进入 Help 页面，页面标题为 Help | P1 | 待执行 |
| TC-10 | 导航 | 返回 Status 页 | 当前处于 Help 页 | 1. 打开菜单 2. 点击 Status | 回到 Status 页，Lat / Long 等字段可见 | P0 | 待执行 |
| TC-11 | 设置-外观 | 开启深色主题 | 已进入 Settings 页，Use Dark Theme 未勾选 | 1. 勾选 Use Dark Theme | 勾选框变为勾选状态，界面背景变为深色 | P1 | 待执行 |
| TC-12 | 设置-外观 | 关闭深色主题 | Use Dark Theme 已勾选 | 1. 取消勾选 Use Dark Theme | 勾选框取消，界面恢复浅色 | P1 | 待执行 |
| TC-13 | 设置-显示 | 切换 Keep Screen On | 已进入 Settings 页 | 1. 取消勾选 Keep Screen On 2. 再次勾选 | 勾选状态随点击正确切换并保持 | P1 | 待执行 |
| TC-14 | 设置-格式 | 坐标格式改为 DMS | 已进入 Settings 页，Coordinate format 为 Decimal degrees | 1. 点击 Coordinate format 2. 选择 DMS | 返回后 Status 页 Lat / Long 以度分秒格式显示 | P1 | 待执行 |
| TC-15 | 设置-单位 | 距离单位改为 Feet | 已进入 Settings 页，距离单位为 Meters | 1. 点击 Preferred distance units 2. 选择 Feet | 返回后 Status 页 Alt 数值旁单位显示为 ft | P1 | 待执行 |
| TC-16 | Accuracy-输入校验 | 空值提交 | 已进入 Accuracy 页 | 1. 不填任何输入框 2. 点击 SAVE | 提示必填项不能为空或按钮不可用，不保存数据 | P1 | 待执行 |
| TC-17 | Accuracy-输入校验 | 非法字符输入 | 已进入 Accuracy 页 | 1. 在 Your latitude 输入 abc 2. 点击 SAVE | 输入被拒绝或提示格式非法，不保存 | P1 | 待执行 |
| TC-18 | Accuracy-边界值 | 纬度上边界 90 | 已进入 Accuracy 页 | 1. 纬度输入 90 2. 经度输入 116 3. 点击 SAVE | 接受输入并保存成功 | P1 | 待执行 |
| TC-19 | Accuracy-边界值 | 纬度越界 91 | 已进入 Accuracy 页 | 1. 纬度输入 91 2. 点击 SAVE | 提示纬度超出有效范围，不保存 | P1 | 待执行 |
| TC-20 | 分享 | 点击分享按钮 | 已进入 Status 页 | 1. 点击工具栏分享图标 | 弹出系统分享面板，可选择应用 | P2 | 待执行 |
| TC-21 | 设置-GNSS | 关闭自启动后重启 | Auto-Start GNSS 已勾选 | 1. 取消勾选 Auto-Start GNSS 2. 结束进程并重新启动 | 启动后 GPS 开关为关闭状态 | P2 | 待执行 |
