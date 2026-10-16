# 示例结果及验证说明

本次34项pytest全部通过，见test_results.xml、test_summary.txt。源码及配置可在optical_model_project.zip中取得；README.md提供安装和运行命令。

## 合成验证：optical_demo.json

显式启用assumed-optics。传感器(0,0,5)m朝北，目标(0,200,5)m，假设目标宽高0.35m；可见光焦距50mm、热成像75mm（设备允许的焦距）；传感器物理宽高和像素判据为示例值。两个场景分别为空场景、有box(−5,80,5,100)、base=0/top=20m的合成不透明建筑。对比度输入可见光0.8、热成像0.7；气温20℃。

|场景|LOS|可见光相对指标|热成像相对指标|
|---|---|---:|---:|
|日间1000lux，无雾无雨|clear|0.8000|0.7000|
|夜间1lux，无雾无雨|clear|0.0800|0.7000|
|日间1000lux，可见度500m，雨10mm/h|clear|0.1607|0.3766|
|建筑遮挡（以上三种环境）|blocked|0|0|

这些数值是配置中的假设函数输出，**不是识别概率或真实设备准确率**。夜间热成像指标相同，是因为只改变lux而保持热对比度不变；现实热对比度可能变化，需用户输入和标定。雨雾参数为示例系数，不能宣称热成像在雾中的真实优势。

JSON包含每个因子的单位、来源状态、配置快照、FOV、目标中心是否入框、像素尺度、LOS和适用范围；真实recognition_probability、effective_recognition_distance默认null。

## 默认资料模式：optical_original_config.json

不启用假设物理尺寸，无遮挡时FOV、入框判断及相对识别指标都明确为null；建筑明确遮挡时相对指标为0，表示已确认几何上无法看到，不表示已计算缺失FOV。

## 官方数据通路

- `official_unknown_height_demo.json`：使用完整官方轮廓，转换EPSG:32649，构造穿过第一栋建筑内部的水平合成射线。high语义未确认，LOS=unknown，识别指标null。
- `official_assumed_height_demo.json`：同一射线，显式将high假设为相对米高度、平地base=0。LOS=blocked，指标0；审计字段和结果中保留assumed，不可解释成正式建筑高度测量。
- `data_audit.json`：完整字段、CRS、几何有效性、DEM统计及原始文件哈希；具体数据解释见data_inventory.md。

## 当前不能可靠计算

真实NVT-951 FOV（缺有效传感器尺寸或直接FOV）；真实最低成像照度（未提供）；真实有效识别距离/概率（无判据、测试条件、标注数据）；官方三维建筑遮挡精度（high语义、基底和垂直基准不明确）。下一步优先确认建筑高度含义/垂直基准，再取得光学尺寸与标定数据。
