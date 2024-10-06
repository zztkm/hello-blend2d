import argparse
import logging
import os
import pathlib
import shutil
import stat
import subprocess

logging.basicConfig(level=logging.DEBUG)


def cmd(args: list[str]) -> None:
    """コマンドを実行する."""
    # 実行コマンドをフルパスに変換する
    if (exe := shutil.which(args[0])) is None:
        raise FileNotFoundError(args[0])
    args = [exe, *args[1:]]
    subprocess.run(args, check=True)


def mk_build_dir(*, clean: bool) -> pathlib.Path:
    """Build 用ディレクトリを作成する."""
    app_dir = pathlib.Path("app")
    build_dir = app_dir / "build"

    if clean:
        # build ディレクトリを削除する
        logging.info("cleaning build directory...")
        shutil.rmtree(build_dir, onexc=handle_permission_error)

    # build ディレクトリを作成する (存在する場合はスキップする)
    build_dir.mkdir(exist_ok=True)

    return build_dir


# 参考: https://docs.python.org/3/library/shutil.html#rmtree-example
def handle_permission_error(func, path: str, _) -> None:
    """Clear the readonly bit and reattempt the removal."""
    pathlib.Path(path).chmod(stat.S_IWRITE)
    func(path)


def cmake() -> None:
    """CMake を実行する."""
    # cmake -G "Ninja" -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
    cmd(["cmake", "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=1", ".."])


def build() -> None:
    """ビルドする."""
    # cmake --build .
    cmd(["ninja"])


def install_deps(*, clean: bool) -> None:
    """依存関係をインストールする."""
    # 依存関係がすでにインストールされている場合はスキップする
    deps = {
        "blend2d": {
            "url": "https://github.com/blend2d/blend2d",
            "path": "blend2d",
        },
        "asmjit": {
            "url": "https://github.com/asmjit/asmjit",
            "path": "blend2d/3rdparty/asmjit",
        },
    }

    if clean:
        # asmjit は blend2d に含まれているので一緒に削除される
        logging.info("cleaning dependencies...")
        shutil.rmtree(deps["blend2d"]["path"], onexc=handle_permission_error)
    elif pathlib.Path(deps["blend2d"]["path"]).exists():
        # blend2d 内に asmjit が存在するか確認する
        if pathlib.Path(deps["asmjit"]["path"]).exists():
            # インストールをスキップする
            return
        cmd(["git", "clone", deps["asmjit"]["url"], deps["asmjit"]["path"]])
        return

    # blend2d と asmjit を取得する
    cmd(["git", "clone", deps["blend2d"]["url"], deps["blend2d"]["path"]])
    cmd(["git", "clone", deps["asmjit"]["url"], deps["asmjit"]["path"]])


def main(clean: bool, clean_deps: bool) -> None:
    """メイン処理."""
    try:
        install_deps(clean=clean_deps)
        # build ディレクトリを作成してそこに移動する
        os.chdir(mk_build_dir(clean=clean))
        cmake()
        build()
    except Exception:
        logging.exception("cmake or build failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="clean build directory")
    parser.add_argument("--clean-deps", action="store_true", help="clean dependencies")

    args = parser.parse_args()

    main(args.clean, args.clean_deps)
