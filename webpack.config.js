const path = require("path");

module.exports = {
  entry: {
    index: "./static/ts/index.tsx",
    manage: "./static/ts/manage.tsx",
    unsubscribe: "./static/ts/unsubscribe.tsx",
  },
  devtool: "inline-source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/i,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        use: [
          {
            loader: "file-loader",
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
    modules: [
      path.resolve(__dirname, "node_modules"),
      path.resolve(__dirname, "static", "ts"),
    ]
  },
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "static", "js", "dist"),
  },
};
