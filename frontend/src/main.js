import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import SimpleMascot from '@/components/simple-mascot.vue'
import MascotPlugin from '@/plugins/mascot-plugin.js'

export function createApp() {
	const app = createSSRApp(App);

	// 全局注册看板娘组件
	app.component('SimpleMascot', SimpleMascot);

	// 使用看板娘插件（自动管理显示/隐藏）
	app.use(MascotPlugin);

	console.log('✅ 全局注册SimpleMascot组件和插件');

	return {
		app,
	};
}