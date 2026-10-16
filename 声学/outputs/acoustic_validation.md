# 独立声学项目验证记录

本记录为桌面“声学”独立目录的重新执行结果。分离前的67项联合验证记录保留在 acoustic_validation_before_split.md，不作为本次测试数量。

- 声学独立测试：29 passed，0失败、0跳过；日志 acoustic_test_summary.txt，JUnit acoustic_test_results.xml。
- 测试及全部声学演示使用导入拦截器禁止 optical_model 及其子模块；均运行成功，确认没有运行时光电依赖。
- 原测试仅更新通用组件的导入路径，没有删减测试或降低断言；29项测试逻辑与分离前一致。
- 通用建筑实现位于 src/acoustic_model/shared/buildings.py，与原GIS实现一致；必要参数校验组件位于同目录config.py。本项目不携带光电设备模型或光电参数。
- pyproject.toml 独立声明 acoustic-capability 包和所需依赖；src布局自动包含 acoustic_model.shared。
- acoustic_demo.json：9个合成场景；acoustic_demo_assumed_angles.json：9个显式假设角度场景；acoustic_official_unknown_height.json：9个合成场景加1个官方轮廓场景。
- 三组声学结果的scenarios内容均与分离前完全一致；配置文件路径已更新为桌面“声学”。官方数据仍为原始工作区路径，高度语义仍未知。
- 光电目录重新执行38项测试全部通过；原有11个源码/配置/测试/示例文件哈希不变，六场景演示JSON与历史输出完整一致。
- 光电验证日志位于 C:/Users/72665/Desktop/光电/outputs/separation_test_summary.txt。

## 如何重跑

在桌面“声学”文件夹的终端执行：

```powershell
python -m pip install -e ".[test]"
python -m pytest -q
python examples/run_acoustic_demo.py
python examples/run_acoustic_demo.py --assumed-angles --output outputs/acoustic_demo_assumed_angles.json
```

本会话因既有虚拟环境和旧依赖目录的访问限制，实际使用Python 3.12.14启动器，向sys.path加入本工作区 work/split_runtime 后运行上述入口；依赖版本与 acoustic_requirements_tested.txt 一致。该验证环境不是声学项目的硬编码运行依赖，用户可使用自己的Python 3.10+环境安装本项目。

声学结果仍是简化经验模型下的相对指标；测试通过不证明真实探测概率、定位精度或精确声场。原始参数和未标定限制见docs中的资料盘点与方法说明。
