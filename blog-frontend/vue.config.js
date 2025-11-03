// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080', // 假设你的后端运行在8080端口
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      }
    }
  }
}