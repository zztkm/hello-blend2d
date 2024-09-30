# Blend2D と C++ でのビルド訓練

Blend2D を使ってみたかったが、そもそも Cmake など C++ のビルドシステムについての知識がなかったので、それをついでに学んだ内容をメモったリポジトリです。

## ビルドに必要なツール

TODO: 他にも依存ツールがあるかもしれないが、新規にインストールしたものを記載しているので、足りないものが見つかった場合は追記する。

- CMake
- [Ninja](https://ninja-build.org/)
  - Ninja を使うことで、`compile_commands.json` が生成される
  - Windows のデフォルトジェネレーター `Visual Studio` では生成されないらしいが、よくわかっていない。
  - Ninja は色々な場所で採用されているっぽいので、今回採用してみた。

## ビルド手順

Blend2D と asmjit を取得する。

```bash
git clone https://github.com/blend2d/blend2d
git clone https://github.com/asmjit/asmjit blend2d/3rdparty/asmjit
```

build ディレクトリを作成し、cmake でビルドシステムを生成する。

```bash
mkdir app/build
cd app/build

cmake -G "Ninja" -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
```

生成されたビルドシステムで ninja を実行する。

```bash
# build ディレクトリで
ninja
```

以降、app.cpp を編集したら、再度 ninja を実行することで、再ビルドが行われる。

```bash
ninja
```

生成した実行ファイルを実行すると、画像が生成されるので開いて結果を確認する。

```bash
open output.png
```

例: ![output.png](./output.png)

## エディタの設定について

[clangd](https://clangd.llvm.org/) を使ってみた。

インストールは <https://clangd.llvm.org/installation> を参照。

上の手順で cmake -G "Ninja" でビルドシステムを生成すると、`compile_commands.json` が生成されるので、clangd はそれを使って補完ができる。

VS Code を起動した状態で、`compile_commands.json` を生成しても、補完が効かない場合は、VS Code を再起動すると効く。
