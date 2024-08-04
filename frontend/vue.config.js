const CompressionWebpackPlugin = require("compression-webpack-plugin");

module.exports = {
  assetsDir: "static",
  configureWebpack: {
    plugins: [
      new CompressionWebpackPlugin({
        algorithm: "gzip",
        test: /\.(js|css|json|txt|html|ico|svg)(\?.*)?$/i,
        threshold: 2048,
        deleteOriginalAssets: false,
        minRatio: 0.8,
      }),
    ],
  },
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true,
        modifyVars: {
          'primary-color': '#50799e',
          'text-color': '#6e6e6e',
          'border-color': '#eee',
          'nice-blue': '#f0f'

        },
      },
    },
  },
  devServer: {
    // proxy: {
    //   "/api": {
    //     target: "http://114.218.158.78:12223",
    //     changeOrigin: true,
    //   },
    // },
  },
};
