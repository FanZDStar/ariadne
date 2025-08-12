# ariadne
Ariadne   恋恋有声

清晰阐述项目创意、实现功能、运行/部署指南。若项目包含可执
行成果（如部署的网站链接、可执行文件、安装包等），须在文档中明确说明访问方式或获取途
径，可执行文件应发布至仓库的Release区域。

## 前端启动过程

1. 进入 `frontend` 目录：
	```powershell
	cd frontend
	```
2. 安装依赖（首次启动或依赖变更时）：
	```powershell
	npm install
	```
3. 启动开发服务器（H5模式）：
	```powershell
	npm run dev:h5
	```
4. 浏览器访问终端提示的本地地址即可预览前端页面。
5. 其他平台启动方式可参考 `frontend/package.json` 的 scripts 字段。