# 声学模块实际验证记录（2026-10-15）

本记录来自本轮真实执行，不沿用历史34 passed。

- pytest：67 passed，其中原有光电相关38项、新增声学29项；最终失败0，未跳过测试。
- 首轮发现未知CRS异常未转换的问题，修复在声学输入适配层后全部重跑通过。没有删除测试或降低断言。
- 日志：`acoustic_test_summary.txt`；JUnit：`acoustic_test_results.xml`。
- 光电源码/配置/测试/示例共11个文件SHA256保持不变，证据：`optical_preservation_audit.json`。
- 重新生成的光电六场景结果与原有 optical_demo.json 完整JSON相等：True。
- 光电回归输出：`optical_regression_demo.json`；单场景输出：`optical_case.json`。原有历史输出未覆盖。
- 声学默认9场景：`acoustic_demo.json`；显式假设角度9场景：`acoustic_demo_assumed_angles.json`。
- 官方轮廓模式10场景：`acoustic_official_unknown_height.json`；第10项真实读取官方轮廓，但声源/射线/噪声是合成输入，高度仍未知。
- 数据复核：`acoustic_data_audit.json`，含两份DOC哈希/文本一致性、PDF声学页完整文字、官方建筑字段/CRS/几何/配套文件哈希及DEM信息。

## 本轮实际执行环境

桌面虚拟环境启动器在当前会话仍无法启动；为完成验证，使用了已能启动的Python 3.12.14和独立安装的依赖，没有修改项目原有虚拟环境。

- 实际使用的Python启动器：`C:/Users/72665/Documents/Codex/2026-09-20/x20-3/work/normalize/lo/LibreOffice/program/python.exe`（启动Python 3.12.14）。
- 验证依赖目录：`C:\Users\72665\Documents\Codex\2026-10-13\gis-python-1-pdf-2-doc\work\acoustic_runtime`。
- 版本清单：`acoustic_requirements_tested.txt`。用户本机通常安装 `pip install -e ".[test]"` 后直接执行README里的标准命令。

本轮在该解释器中把验证依赖目录加入sys.path，然后运行以下等价入口：

```powershell
python -m pytest -q -o cache_dir=.pytest-acoustic-cache --basetemp=.pytest-acoustic-tmp2 --junitxml=outputs/acoustic_test_results.xml
python examples/run_acoustic_demo.py
python examples/run_acoustic_demo.py --assumed-angles --output outputs/acoustic_demo_assumed_angles.json
python examples/run_acoustic_demo.py --buildings "C:/Users/72665/Documents/Codex/2026-10-13/gis-python-1-pdf-2-doc/work/data/创意二数据集/区域数据/building/zheng_apart.shp" --output outputs/acoustic_official_unknown_height.json
python examples/run_optical_demo.py --assumed-optics --output outputs/optical_regression_demo.json
python examples/run_optical_case.py --assumed-optics --output outputs/optical_case.json
```

## 声学输出样例

均为500–2000 Hz、Z计权的合成声源与噪声；所有相对质量均未标定，不能读成探测概率。

|场景|距离m|直达线|合成噪声dB_SPL|估计接收声级dB_SPL|信噪差dB|相对质量|
|---|---:|---|---:|---:|---:|---:|
|quiet_clear|200.0000|clear|40.0000|53.7804|13.7804|1.0000|
|farther_clear|400.0000|clear|40.0000|47.5598|7.5598|0.8780|
|traffic|200.0000|clear|60.0000|53.7804|-6.2196|0.1890|
|mixed_city_noise|200.0000|clear|63.6478|53.7804|-9.8674|0.0066|
|wind_rain|200.0000|clear|55.5630|53.0839|-2.4791|0.3760|
|building_screen|200.0000|blocked|40.0000|41.7804|1.7804|0.5890|
|narrow_corridor|200.0000|clear|40.0000|53.7804|13.7804|1.0000|
|missing_building_height|200.0000|unknown|40.0000|null|null|null|
|missing_source_level|200.0000|clear|40.0000|null|null|null|

建筑遮挡场景中，声级降低12 dB但仍为有限值；相对质量不被几何规则直接置零。缺楼高/缺声源声级时返回null。狭窄街巷场景只改变多路径代理与可选方向不确定性，没有凭空增加声压反射项。

默认设备缺测角参数，方向尺度始终为空。显式假设角度场景：

|场景|方位尺度deg|俯仰尺度deg|
|---|---:|---:|
|quiet_clear|2.0000|3.0000|
|farther_clear|2.7321|3.7321|
|traffic|6.8659|7.8659|
|mixed_city_noise|7.9602|8.9602|
|wind_rain|5.7437|6.7437|
|building_screen|8.6278|9.6278|
|narrow_corridor|8.0000|9.0000|
|missing_building_height|null|null|
|missing_source_level|null|null|

上述尺度不是标准差、置信区间或实际定位误差。范围误差、实际探测概率、模型有效范围和实测探测距离均保留missing。

## 验证局限

合成测试仅检验代码与写明的假设一致。官方数据复读仅证明可读取二维轮廓并正确保留未知高度，不能证明真实城区声场、现场探测距离、绕射/反射精度或声音分类精度。仍须补实测声源、接收点噪声、阵列校准、建筑高度/材质与共同垂直基准。
