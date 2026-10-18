# 第三方资料与素材说明

## 字体

- 上游：Noto Serif CJK SC Regular，Noto CJK项目。
- 官方仓库：https://github.com/notofonts/noto-cjk
- 本次下载源：https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Regular.otf
- 上游许可证：https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/LICENSE
- 许可：SIL Open Font License 1.1；全文随附在`site/assets/fonts/OFL.txt`。
- 上游字体版权记录：© 2017–2024 Adobe (http://www.adobe.com/)，保留于子集字体的name表。
- 修改：按本版网页字符集合裁剪为WOFF2，并改名Shanhe Serif；原始版权与许可证名称记录保留在字体文件内。修改字体继续遵循OFL，不单独售卖，不把OFL扩展为整个作品的许可。
- 字体为本地资源，网页运行不调用外部字体服务。正文使用访问者设备的系统字体。
- 子集制作日期：2026-10-18。需要新字符时可使用`tools/subset_font.py`重建。

## v1.1书法标题字体

- 上游：Ma Shan Zheng Regular，作者与版权记录保留在字体内。
- 下载源：https://raw.githubusercontent.com/google/fonts/main/ofl/mashanzheng/MaShanZheng-Regular.ttf
- 许可：SIL Open Font License 1.1，全文见`site/assets/fonts/MaShanZheng-OFL.txt`。
- 修改：裁剪为本版标题所需字符，改名Shanhe Brush，以WOFF2本地加载。重建工具：`tools/subset_brush.py`。

## v1.1行政区划数据

- 发布项目：[Supeset/China-GeoData](https://github.com/Supeset/China-GeoData)，上游文件`geojson/china_province_full.geojson`。
- 项目声明MIT许可，原文保存于`site/assets/licenses/China-GeoData-MIT.txt`；保留Copyright (c) 2025 圈集。
- 本包维护数据位于`tools/data/provinces.json`，含35个要素；网页图面按路线区域裁切显示，保留省级边界并添加省名。路线与底图共用投影。
- 当前背景表达现行行政区划空间关系，不冒充1930年代行政区划；路线依旧是主要节点连接。项目声明的许可与地图的公开使用要求分别处理，未声称已获得地图审查批准。

## v1.1档案及报道配图

原始文件直接保存到本地，没有裁切、水印移除或色彩改造；在对应事件段落中使用并提供原文链接，不作为无关装饰背景。网页上的图注简洁呈现来源，维护信息集中于此。

| 本地文件 | 原文与内容 | 来源署名 |
| --- | --- | --- |
| `site/assets/photos/ticket-1956.jpg` | https://xq.xjtu.edu.cn/info/1022/2508.htm ，1956年9月2日乘车证 | 西安交通大学西迁精神专题网；图片保留原有水印 |
| `site/assets/photos/departure-1956.jpeg` | https://xqjy.xjtu.edu.cn/info/1063/1245.htm ，1956年8月从徐家汇启程 | 西安交通大学“西迁记忆” |
| `site/assets/photos/opening-1956.jpg` | https://xqjy.xjtu.edu.cn/info/1063/1246.htm ，迁校后首次开学典礼 | 西安交通大学“西迁记忆” |
| `site/assets/photos/walk-2026.png` | https://news.xjtu.edu.cn/info/1007/230870.htm ，2026年健步走活动报道配图 | 西安交通大学新闻网；图片：校工会 |

上述网页未标明统一开放许可，不能将它们或本补丁包整体标为CC／MIT素材包；这里不声称已取得新闻图片的另行授权。若改变用途、进行二次分发或由学校公开宣传，应据具体使用范围核对图片权利信息。活动海报是报道配图，不是现场摄影。

## 图形与正文（基础版）

- 路线、节点、红旗／五角星／书本／列车／书信图标、轮渡图形为原创代码与SVG；行政区背景和照片来源另见v1.1记录。
- 坐标：人工近似地理参照，非精确遗址定位、测绘成果或历史轨迹数据。
- 正文：依据页面来源列表与任务书所列材料进行原创改写；未取得图片使用权的资料不作为图片分发。
- 历史事实与原始资料的权利归属分别处理。不要把整个项目标记为已获学校官方授权，或把图片来源信息等同于转载许可。
- 发布到公开GitHub不自动为自有代码和正文添加开源许可。是否为原创部分选择MIT、CC等许可，由作者决定；本包未擅自替作者授予此类许可。

## GitHub Actions

工作流引用GitHub官方Actions：checkout、configure-pages、upload-pages-artifact、deploy-pages。它们在GitHub运行时按对应项目许可与平台规则使用，本包未包含这些Actions的源码副本。无需手填访问令牌。
