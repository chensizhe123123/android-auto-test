# Android 自动化测试工程

## 阶段2：被测对象与可测功能点（工位机 Pixel 6 / API 34 模拟器）

- 源码：barbeau/gpstest（Apache-2.0），分支 master，本地 D:\android-test\gpstest
- 构建：JAVA_HOME=jbr-21 ./gradlew :GPSTest:assembleGoogleDebug
- 产物：GPSTest/build/outputs/apk/google/debug/GPSTest-google-debug.apk（约 12 MB，debug 签名）
- 安装：因签名与官方 release 包不同，须先 adb uninstall com.android.gpstest 再安装

可测功能点（不依赖真实卫星信号）：
1. 启动与首屏：Status 页标签结构完整
2. 抽屉导航：Status/Map/Sky/Accuracy/Settings/Help 六项切换
3. GPS 开关：工具栏开关可开/关并联动
4. 主题切换：Use Dark Theme 生效
5. 屏幕常亮：Keep Screen On 勾选切换
6. 坐标格式：Coordinate format 弹窗选择生效
7. 单位切换：Preferred distance/speed units 生效
8. Accuracy 输入校验：空值/非法值/边界值
9. GNSS 设置：Auto-Start GNSS 勾选切换
10. 分享按钮：触发系统分享面板

模拟器限制（不可断言）：卫星数量、C/N0 数值、天空图分布、Map 底图、真实定位精度
