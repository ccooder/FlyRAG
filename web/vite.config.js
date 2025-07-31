import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    // 别名
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '~@': path.resolve(__dirname, 'src')
    }
  },
  plugins: [vue()],
  // 开发环境配置
  server: {
    // // host: 'localhost',
    // port: 9000,
    // hmr: {
    //   // 有错误信息弹出提示
    //   overlay: false
    // },
    proxy: {
      // '/api': {
      //   target: webpackConfig.PROXY_URL,
      //   changeOrigin: true, //是否跨域
      //   rewrite: (path) => path.replace(/^\/api/, ''),
      // },
      '/ragAPI': {
        target: 'http://192.168.28.245:7788',
        changeOrigin: true, //是否跨域
        rewrite: (path) => path.replace(/^\/ragAPI/, '')
      }
    }
  }
})
