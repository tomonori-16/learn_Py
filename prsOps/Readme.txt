◆common配下のモジュールをインポートする為に
.pthファイルにpythonのモジュール検索パスを追加して、pythonのシステムパス配下に配置します。

確認方法は、
import sys
print(sys.path)

を実行すると、pythonのシステムパスを確認できます。

当プロジェクトの場合は、「pression_path.pth」をpythonのシステムパスに配置します。
