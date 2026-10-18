# 山河为证——从长征路到西迁路

v1.1：新增行政区划背景、红色主题图标、书法标题、4幅档案与报道配图，以及2026年4月7日回信内容。

一份可直接运行、同步到GitHub并发布到GitHub Pages的静态网页项目。电脑使用“左侧地图＋右侧叙事”，手机使用“上方地图＋下方正文”。页面包含完整正文、两条示意路线、章节联动、人物与轮渡史料卡、来源说明。

**无需npm安装、构建工具、API密钥或后台。**你只需Python启动本地预览，或者直接将`site/`作为静态网站发布。网页通过同一个网址适配手机和电脑。

## 1. 最快启动

解压后进入`shanhe-h5`文件夹，确认里面同时有`README.md`、`site`、`tools`和`.github`。

在此文件夹打开终端：

```bash
python -m http.server 8000 --directory site --bind 127.0.0.1
```

如果Windows提示没有python，可改用`py -m http.server 8000 --directory site --bind 127.0.0.1`；macOS/Linux常用`python3`。

浏览器访问 **http://127.0.0.1:8000/**。停止预览：回到终端按`Ctrl+C`。

不要直接双击`index.html`作为交互测试方式：网页使用ES modules，浏览器通常限制`file://`加载模块。本地HTTP预览能正确加载。

手机与电脑在同一局域网时，可把`--bind 127.0.0.1`改为`--bind 0.0.0.0`，再用手机访问`http://电脑的局域网IP:8000/`。是否可达还取决于本机防火墙和网络隔离。停止预览即关闭该服务。

## 2. 项目里有什么

| 文件 | 用途 |
| --- | --- |
| `site/index.html` | 完整正文与页面结构，无JS时仍能阅读 |
| `site/styles.css` | 颜色、字体、布局与手机适配；CSS文件后缀是`.css` |
| `site/app.js` | 阅读进度、章节地图状态、史料弹层、目录 |
| `site/data.js` | 章节状态、来源信息、补充故事 |
| `site/config.js` | 作者、学院和最终网址 |
| `site/assets/route-overview.svg` | 无行政边界的地理坐标示意总览 |
| `site/assets/ferry.svg` | 据文字绘制的原创南京轮渡示意 |
| `site/assets/fonts/` | 本地宋体、书法标题字体子集及OFL许可证 |
| `.github/workflows/pages.yml` | 推送后自动检查并部署GitHub Pages |
| `tools/check_project.py` | 本地资源、锚点、模块、SVG和字体文件检查 |
| `tools/check_interactions.mjs` | 可选：DOM模拟下的章节与弹层逻辑回归检查 |
| `tools/build_static.py` | 从任务书重建HTML和示意地图；普通浏览不依赖它 |
| `tools/subset_font.py` | 可选：修改字体字符集后重建子集 |
| `tools/make_qr.py` | 可选：用最终公开网址生成二维码 |
| `docs/内容与开发任务书.md` | v1.0内容脚本与开发要求；v1.1扩展见更新说明 |
| `docs/验证说明.md` | 本次检查范围、结果与后续实测清单 |
| `THIRD_PARTY_NOTICES.md` | 字体来源、修改记录及素材说明 |

不包含Git仓库历史、账户信息或令牌。配图与行政区划数据的来源、许可及维护记录见`THIRD_PARTY_NOTICES.md`。还未替你创建GitHub仓库或公开发布。

## 3. 用GitHub Desktop同步（适合少写命令）

1. 安装并登录[GitHub Desktop](https://desktop.github.com/)。
2. 选择`File → New repository`，名称建议`shanhe-h5`，在电脑上创建一个新仓库。
3. 把本项目**文件夹里面的全部内容**复制到新仓库根目录，不要再套一层`shanhe-h5`。仓库根目录应直接看到`site/`和`README.md`。
4. 确认`.github/workflows/pages.yml`也已复制。文件管理器可能隐藏以点开头的目录；缺少它就没有自动发布工作流。
5. 在Desktop中填写提交说明，例如“完成H5第一版”，点击`Commit to main`。
6. 点击`Publish repository`，确认名称。若使用免费个人账户并准备公开源码与网页，选择公开仓库；发布前检查不要把投稿表、联系方式或私人文件放进去。
7. 完成下一节的Pages设置。以后修改文件后，重复`Commit to main → Push origin`即可同步并触发发布。

GitHub Desktop自动生成的说明文件如与项目冲突，保留本项目README；不要把`.github`或`site`漏掉。分支若不是`main`，建议改为`main`，或同步修改工作流的`branches`。

## 4. 开启GitHub Pages

本项目使用GitHub官方静态部署Actions，上传目录明确为`site/`，不是整个仓库。因此开发文档、Python工具和配置说明不会作为网站页面发布；公开仓库中仍可看到源码文件。

1. 打开GitHub仓库网页，进入`Settings → Pages`。
2. 在`Build and deployment → Source`中选择 **GitHub Actions**。
3. 回到`Actions`，找到`Deploy static site to GitHub Pages`。
4. 初次提交可能早于Pages启用：可以选择`Run workflow`手动运行，或对`main`再做一次修改并推送。
5. 工作流成功后，从部署结果或`Settings → Pages`取得最终网址。通常为`https://用户名.github.io/仓库名/`，实际以GitHub显示的网址为准。
6. 使用未登录的浏览器打开该网址，再在手机和微信内测试。

已配置最小部署所需的`contents: read`、`pages: write`与`id-token: write`权限；不需要在仓库中手填Personal Access Token。若账户、组织或学校策略禁用了Actions/Pages，需要在对应设置中解决，不能靠修改页面代码绕过。

不要同时再添加另一套部署工作流。选择本项目的Actions发布方式即可，无需另建`gh-pages`分支。

### 常见故障

| 现象 | 检查位置 |
| --- | --- |
| Actions列表里没有工作流 | `.github/workflows/pages.yml`是否在仓库根目录下；是否已提交推送 |
| Pages尚未启用／Configure Pages报错 | `Settings → Pages → Source`是否为GitHub Actions，启用后重跑 |
| 提交后没有自动更新 | 分支是否为`main`；是否点击Push；Actions是否成功 |
| 网页404 | 使用Pages部署结果中的URL；确认上传目录`site`中有`index.html` |
| 页面没有样式 | 检查`styles.css`是否上传；大小写是否一致；不要把`./`改为站点根路径`/` |
| 显示旧版本 | 等工作流完成，再强制刷新；本项目未添加Service Worker |
| 某些网络访问慢或打不开 | 用投稿时的实际手机网络测试；若更换托管平台，上传同一个`site/`目录并重新生成二维码 |

官方说明：[自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[配置发布源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。工作流使用2026-10-18核对的官方Actions版本。

## 5. 如果你习惯Git命令

先在GitHub创建一个**空仓库**，不要预先添加README。然后在本项目根目录执行：

```bash
git init
git add .
git commit -m "实现山河为证H5第一版"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shanhe-h5.git
git push -u origin main
```

将`YOUR_USERNAME`和仓库名替换为自己的。认证交给GitHub Desktop、系统凭据管理器或GitHub CLI完成，不把令牌写在代码、远程URL、截图或聊天记录中。

后续更新：

```bash
git add .
git commit -m "调整正文与地图排版"
git push
```

## 6. 你通常需要改哪里

### 作者与作品信息

修改`site/config.js`：

```js
export const siteConfig = {
  title: '山河为证',
  author: '你的姓名',
  affiliation: '你的学院',
  publicUrl: 'https://你的用户名.github.io/你的仓库名/',
};
```

姓名和学院会出现在页脚；`publicUrl`作为维护记录，网页不会强行跳转或自动生成二维码。作品标题同时存在于静态HTML、文案和配置中，若改名请一并搜索修改，`title`不是全站文案模板开关。

### 正文与史料

- 快速改正文：直接修改`site/index.html`中对应P0—P7章节。
- 改弹层故事、来源弹层和图片弹层资料：修改`site/data.js`。
- v1.1的回信段落、图片卡片和省界绘制在`tools/presentation_v2.py`；P7最终内容由该文件生成，覆盖旧任务书的尾声初稿。
- 来源同时有静态页脚与动态面板，修改时同步两处，或用下面的生成脚本重建。
- 系统性改稿：先改`docs/内容与开发任务书.md`，保持章节标记格式，再运行`python tools/build_static.py`。它会**覆盖**现有`site/index.html`和`site/assets/route-overview.svg`，直接在这两处做的个性化修改应先备份或提交Git。
- 生成器从`data.js`读取来源条目，并调用`presentation_v2.py`加入本轮改动；两份Python文件应一起保留。大改数据格式后应同步修改生成器。

### 颜色与字体

主色在`site/styles.css`开头的`:root`变量中。主标题和副标题使用Shanhe Brush书法子集，来自Ma Shan Zheng；章节标题使用Shanhe Serif字符子集，来自Noto Serif CJK SC Regular；正文默认使用设备上的苹方、微软雅黑等系统字体。浏览器在用户设备上调用系统字体，包内不分发商业系统字体。

字体文件本地加载，无Google Fonts外部请求。子集已覆盖本版网页使用的可用字形；后续新增字未包含时会自动回退到系统宋体，不会让内容消失。

如要重建字体：从[上游官方仓库](https://github.com/notofonts/noto-cjk/tree/main/Serif)下载简体中文Regular OTF，在本机运行：

```bash
python -m pip install "fonttools[woff]" brotli
python tools/subset_font.py /path/to/NotoSerifCJKsc-Regular.otf
```

重建后的修改字体仍以新名称Shanhe Serif发布，保留OFL和版权信息；不要提交完整原始OTF，它体积较大且不是网页运行必需项。

### 地图

当前路线下方已加入省级行政区划背景。路线仍是主要节点的叙事连接，不是精确行军轨迹或历史铁路数据；精度与资料说明保留在维护文档，不再占用作品正文。

- 节点坐标、标签偏移、路线顺序：`tools/build_static.py`中的`NODES`。
- 哪章显示到哪一段：`site/data.js`中的`chapters`。
- 正式底图不要随手放在现有SVG下面：底图与节点必须采用同一投影并配准。
- 行政区背景数据在`tools/data/provinces.json`，由`tools/presentation_v2.py`与路线采用同一投影生成，不需要地图服务密钥。地图数据的许可与公开发布要求分别核对。
- 添加照片前，核对图片使用依据并在图旁与来源区补充信息；公开发布的照片不因标来源就自动获得转载许可。

## 7. 生成投稿二维码

等Pages部署完成，先在未登录浏览器中验证最终URL，然后：

```bash
python -m pip install "qrcode[pil]"
python tools/make_qr.py "https://YOUR_USERNAME.github.io/shanhe-h5/"
```

二维码生成到`output/作品二维码.png`，不会自动进入网站或Git提交。请用另一台设备扫码复核。该工具不检查URL是否真的部署成功；扫码验证仍由你完成。

投稿压缩包可另行准备：征集表、作品说明、最终链接、二维码、必要来源说明。不要用本地`127.0.0.1`或GitHub仓库源码地址替代网页访问链接。

## 8. 检查与发布前自测

```bash
python tools/check_project.py
```

如果安装了Node，还可检查JS语法：

```bash
node --check site/app.js
node --check site/data.js
node --check site/config.js
```

文件检查不等于浏览器视觉验证。发布前建议确认：

- [ ] 360/390px手机宽度、平板和1440px电脑下无横向滚动。
- [ ] 从上往下与反向滚动，地图章节均正确；从目录跳转后正文可见。
- [ ] 手机点击史料卡、关闭按钮可操作；桌面Tab/Enter/Esc正常。
- [ ] 关闭动画偏好、禁用JS时正文仍可读。
- [ ] 两条路线终点、1935/1936时间关系无误。
- [ ] 最终网址、字体和静态资源均加载成功，二维码扫码正确。
- [ ] 若添加了照片或底图，已完成史实、使用依据与来源核对。

本次验证与限制详见`docs/验证说明.md`。源码没有替你登录、创建GitHub仓库、推送或部署；以上为本地交付与配置指导。

可选的交互逻辑检查需要Node及开发依赖：在根目录运行`npm ci`，然后`npm run test:dom`。该测试使用DOM模拟，不启动浏览器，也不验证真实CSS布局或原生弹层的焦点约束。网站运行不依赖这些开发包，`node_modules`不要提交。

## v1.1增量更新

本轮仅替换补丁包列出的文件，按原路径覆盖仓库即可。`site/config.js`、GitHub Pages工作流及个人设置不需要覆盖。详细变更、素材出处及检查范围见`docs/v1.1更新说明.md`。

书法字体重建：`python tools/subset_brush.py /path/to/MaShanZheng-Regular.ttf`，依赖与宋体子集重建相同。标题之外新增的字未包含时会回退到宋体。
