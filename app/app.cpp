//  参考: https://blend2d.com/doc/getting-started.html
#include <blend2d.h>

int main(int argc, char *argv[]) {
  // 480x480 の PRGB32 フォーマットの画像
  BLImage img(480, 480, BL_FORMAT_PRGB32);
  // 描画コンテキスト
  BLContext ctx(img);

  ctx.clearAll();

  // 線形グラデーション値で初期化した BLGradient オブジェクトを作成
  // 今回は 0, 0 から 480, 480 に向かってグラデーションするように設定
  BLGradient linear(BLLinearGradientValues(0, 0, 480, 480));

  // 0.0 から 1.0 までの範囲で、カラーストップを追加
  // 青から緑へのグラデーション
  linear.addStop(0.0, BLRgba32(0xFF0000FF));
  linear.addStop(0.5, BLRgba32(0xFF008080));
  linear.addStop(1.0, BLRgba32(0xFF00FF00));

  // 塗りつぶし色を設定
  ctx.setFillStyle(linear);

  // (ドキュメントの日本語訳): 角丸四角形を半径 r で塗りつぶす
  // r の値を変えると、角丸四角形の角の丸みが変わる
  ctx.fillRoundRect(40.0, 40.0, 400.0, 400.0, 45.5);

  ctx.end();

  img.writeToFile("output.png");
  return 0;
}