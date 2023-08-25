class outputValueClass:
    # 各メソッドの返り値を格納するクラス
    # 正常／異常終了のステータスを格納するインスタンス変数
    # 出力結果を格納するフィールド
    # まずは、値を格納するメソッド無しでやってみる。

    def __init__(self) -> None:
        self.status = True
        self.return_Value = None
