/**
 * 看板娘全局插件
 * 自动在配置的页面显示看板娘，无需手动添加标签
 */
import { createVNode, render } from 'vue'
import SimpleMascot from '@/components/simple-mascot.vue'
import { shouldShowMascot } from '@/utils/mascot-config.js'

export default {
    install(app) {
        let mascotInstance = null
        let mascotContainer = null

        // 创建看板娘容器
        const createMascotContainer = () => {
            if (!mascotContainer) {
                mascotContainer = document.createElement('div')
                mascotContainer.id = 'global-mascot-container'
                mascotContainer.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
          z-index: 9999;
        `
                document.body.appendChild(mascotContainer)
            }
            return mascotContainer
        }

        // 挂载看板娘
        const mountMascot = () => {
            if (!mascotInstance) {
                const container = createMascotContainer()
                const vnode = createVNode(SimpleMascot)
                render(vnode, container)
                mascotInstance = vnode.component
                console.log('🎭 全局看板娘已挂载')
            }
        }

        // 卸载看板娘
        const unmountMascot = () => {
            if (mascotInstance && mascotContainer) {
                render(null, mascotContainer)
                mascotInstance = null
                console.log('🎭 全局看板娘已卸载')
            }
        }

        // 检查当前页面是否需要显示看板娘
        const checkAndToggleMascot = () => {
            const pages = getCurrentPages()
            if (pages.length === 0) return

            const currentPage = pages[pages.length - 1]
            const route = currentPage.route || ''
            const normalizedRoute = route.startsWith('/') ? route : '/' + route

            const shouldShow = shouldShowMascot(normalizedRoute)

            console.log(`🎭 插件检测: 路由=${normalizedRoute}, 应显示=${shouldShow}`)

            if (shouldShow) {
                mountMascot()
                // 通知组件更新可见性
                if (mascotInstance && mascotInstance.proxy) {
                    mascotInstance.proxy.updateMascotVisibility?.()
                }
            } else {
                // 不卸载，只是通过组件自己的v-show隐藏
                if (mascotInstance && mascotInstance.proxy) {
                    mascotInstance.proxy.updateMascotVisibility?.()
                }
            }
        }

        // 初始化：立即挂载
        mountMascot()

        // 监听页面切换
        app.mixin({
            onShow() {
                checkAndToggleMascot()
            }
        })

        // 监听全局页面变化事件
        uni.$on('pageChange', checkAndToggleMascot)

        console.log('✅ 看板娘插件已安装')
    }
}
