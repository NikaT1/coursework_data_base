// vue.config.js
module.exports = {
    // https://cli.vuejs.org/config/#devserver-proxy
    devServer: {
        port: 3000,
        proxy: {
            '/cases': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/inquisitions': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/accusations': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/bibles': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/localities': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/persons': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            },
            '/auth': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            }
        }
    }
}