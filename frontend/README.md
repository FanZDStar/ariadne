# Frontend
## 前端启动过程

1. 进入 `frontend` 目录：
	```powershell
	cd frontend
	```
2. 安装依赖（首次启动或依赖变更时）：
	```powershell
	npm install
	```
3. 配置环境变量
	- 创建 `.env` 文件，并添加以下内容：
	```
	# API 访问地址，举例：本机测试环境
	VUE_APP_API_BASE_URL=http://localhost:8000
	```
3. 启动开发服务器（H5模式）：
	```powershell
	npm run dev:h5
	```
4. 浏览器访问终端提示的本地地址即可预览前端页面。
5. 其他平台启动方式可参考 `frontend/package.json` 的 scripts 字段。
