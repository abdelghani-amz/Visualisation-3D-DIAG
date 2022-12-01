const path = require('path')

const webpack = require('webpack')
const CopyPlugin = require('copy-webpack-plugin')

const entry = path.join(__dirname, 'src', 'main.js')
const outputPath = path.join(__dirname, 'public')
const itkConfig = path.resolve(__dirname, 'src', 'itkConfig.js')

module.exports = {
  entry,
  output: {
    path: outputPath,
    filename: 'index.js',
    library: {
      type: 'umd',
      name: 'bundle',
    },
  },
  module: {
    rules: [
      { test: /\.js$/, loader: 'babel-loader' }
    ]
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: path.join(__dirname, 'node_modules', 'itk-wasm', 'dist', 'web-workers'),
          to: path.join(__dirname, 'dist', 'itk', 'web-workers')
        },
        {
          from: path.join(__dirname, 'node_modules', 'itk-image-io'),
          to: path.join(__dirname, 'dist', 'itk', 'image-io')
        },
        {
          from: path.join(__dirname, 'node_modules', 'itk-mesh-io'),
          to: path.join(__dirname, 'dist', 'itk', 'mesh-io')
        }
    ]})
  ],
  resolve: {
    fallback: { fs: false, path: false, url: false, module: false },
    alias: {
      '../itkConfig.js': itkConfig,
      '../../itkConfig.js': itkConfig,
    },
  },
  performance: {
    maxAssetSize: 10000000
  }
}