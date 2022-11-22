# VOICE CHANGER
音声変換を行うためのプログラムです。
音声変換は周波数分析またはリサンプリングで行っています。
実行する場合はPythonの実行環境と以下のライブラリが必要になります。
- numpy
- scipy
- matplotlib
- wave
- pyaudio
- tkinter

## 使用方法
実行には以下のファイルを使用します。
```bash
SWVC/
├── gui_chanfl.py
├── gui_graph.py
├── gui_inv.py
├── stylelib
　   └── gray-background.mplstyle
```

変成器のプログラムは次のコマンドで実行できます。
```bash
$ python gui_chanfl.py 

```
逆再生をする場合は`gui_inv.py`, 音波のグラフをリアルタイムで出力する
場合は`gui_inv.py`を実行してください。

`stylelib`ディレクトリにはmatplotlib用のmplstyleファイル`gray-background.mplstyle`をおいています。
使用する場合はこのファイルを`~/.config/matplotlib/stylelib/`（Linuxの場合）などに追加し、
`command/graphics/wav_plot`の8行目にある`# plt.style.use('gray-background')`をアンコメント（`# `を削除）してください。

音声データを保存する場合、dataディレクトリに保存されます。オリジナルの音声は`original_data`, 音声変換した
データは`change_data`, 逆再生されたデータは`inverse_data`という名前で保存されます。
繰り返し行うと上書き保存されるため、何度も保存したい場合は名前を書き換えてください。
