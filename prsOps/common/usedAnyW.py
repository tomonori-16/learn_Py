class outputValueClass:
    """ 各メソッドの返り値を格納するクラス

    Parameters:
    ----------
    status:boolean
        メソッドの正常／異常終了のステータスを格納するインスタンス変数
    return_Value:untyped
        メソッドの出力結果(成果物)を格納するフィールド
    """

    def __init__(self) -> None:
        # まずは、値を格納するメソッド無しでやってみる。
        self.status = True
        self.return_Value = None
