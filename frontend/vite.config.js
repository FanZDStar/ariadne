import { defineConfig, loadEnv } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    base: './',
    plugins: [
      uni(),
    ],
    define: {
      // 注入环境变量到运行时
      'process.env.VUE_APP_API_BASE_URL': JSON.stringify(env.VUE_APP_API_BASE_URL),
      'process.env.NODE_ENV': JSON.stringify(mode)
    }
  }
})
