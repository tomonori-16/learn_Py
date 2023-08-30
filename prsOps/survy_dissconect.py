""" Cloud Watchに保存されているAmazon Connectに関するログをから"Error"
    という単語が含まれている文字列を抜き出したファイルを用意して、
    Amazon Connectのコンタクトログも用意する。
    その両ファイルの文字列をContactIDで結合して、Amazon Connectの
    コンタクトフローによる切断の原因を調査する為のファイルを作成する。
"""
import sys
import csv
from pathlib import Path
import re

import common.usedAnyW as usdaw

pathCwd = Path.cwd() #カレントパスを設定
print(pathCwd)

CSVFILENAME = 'contactSrchResult.csv' # AmazonConnctのコンタクトログファイル
CLWLOGFILENAME = 'cwl.txt'            # Cloud Watchのログファイル
CONECTIDCSV = 'AzcContactId'          # ConnectId の項目名(AmazonConnectのログファイル)
CONNECTIDCLW = 'ContactId'            # CloudWatchのログファイル
RETURNCSV = 'wokrfile.csv'            # "Error"という単語を含んだlogの一覧(但し余計な改行が残る)
RESULTCSV = 'about_error_string.csv'  # 最終結果"Error"という単語を含んだlogの一覧

class WlogClass:
    """ cloud Watch logの1行ごとをlistで保持するクラス。

        引数で渡された文字列を含むログがあればそれを返す。
        呼び出されたログはWlogClassから削除する
    """
    clwLogList=[]

    def __init__(self) -> None:
        pass

    @classmethod
    def _deleteST(cls,tgIndex):
        """ 取得されたリストの要素を削除する。
            本来はlistのpopメソッドを使えば不要なメソッドだが、
            学習プロジェクトの為そのまま利用する。

            Parameters
            ----------
            tgIndex:int
                    clwLogListから削除する要素のインディックス番号
        """
        outputValue = usdaw.outputValueClass()
        try:
            del cls.clwLogList[tgIndex]
            return outputValue  # 成功した場合はステータスTrueを返す
        except KeyError as e:
            print(e.args)
            print('検索対象listの削除に失敗しました。')
            outputValue.status = False
            return outputValue
        except Exception:
            print('検索対象listの削除失敗')
            outputValue.status = False
            return outputValue

    @classmethod
    def searchLogText(cls,argContactID):
        """ コンタクトIDでCloud Watchのログテキストを検索する。
            引数で渡された文字列で、clwLogListを検索する。
            該当するListの要素があればそれを返す。

            Parameters:
            ----------
            argContactID:string
                コンタクトID（文字列）

            Returns:
            ----------
            outputValue:outputValueClass
                return_ValueにコンタクトIDに該当したListの要素(string)
                statusに処理結果（正常／異常終了）のステータス(boolean)
        """
        count = 0
        outputValue = usdaw.outputValueClass()
        outputValue.return_Value = 'NoErrorString'
        try:
            for row in cls.clwLogList:
                # print('検索文字{c} 対象文字列{r}'.format(r=row,c=argContactID))
                if argContactID in row:
                    outputValue.return_Value = row
                    # ログを返したら、当該ログはclwLogListから削除する
                    # 本来はlistのpopメソッドを使えば良いが、学習用プロジェクトの為そのまま
                    if cls._deleteST(tgIndex=count):
                        pass
                    else:
                        outputValue.status = False
                    return outputValue
                count+=1
            return outputValue
        except Exception as e:
            print(e.args)
            print('検索失敗')
            outputValue.status = False
            return outputValue

def import_contactSrc_csv():
    """ Amazon Connectの切断の履歴を取り込む

        Connectのログはcsv形式で出力されるが、
        ConnectIDをConnectのログから抽出する際に
        Connectの1行のレコードがDict形式であった方が都合が良いので、
        1行分をDictにして、それをListに纏めて返す。
        csvファイル明は固定で、定数CSVFILENAMEに設定する

        Parameters:
        ----------
            無し

        Returns:
        ----------
        outputValue:outputValueClass
            return_Valueにcsvの1行をdict形式にして纏めたList
            statusに処理結果（正常／異常終了）のステータス(boolean)
    """
    outputValue = usdaw.outputValueClass()
    try:
        with open(Path(pathCwd/Path(CSVFILENAME)))as csvf:
            csvFileDicObj = csv.DictReader(csvf)
            csvFileDicList = [row for row in csvFileDicObj]
        outputValue.return_Value = csvFileDicList
        return outputValue
    except OSError as e:
        print(e.args)
        print("Connectのログファイル(CSVファイル)を開くことができません。")
        outputValue.status = False
        return outputValue
    except Exception as e:
        print(e.args)
        print('Connectのログファイル読み込みでExceptionが発生しました。')
        outputValue.status = False
        return outputValue
    except:
        print('Connectログファイル??')
        outputValue.status = False
        return outputValue

def import_wlog_txt():
    """ Cloud Watch のAmazon Connectのlogを取り込む

        txt形式のAmazon Connectのログの1行ごとを要素としたListを返す
        ログファイル名は定数CLWLOGFILENAMEに設定する。

        Parameters:
        ----------
                無し

        Returns:
        ----------
        outputValue:outputValueClass
            return_Valueにテキストファイルの1行を纏めたList
            statusに処理結果（正常／異常終了）のステータス(boolean)
    """
    outputValue = usdaw.outputValueClass()
    try:
        textf = open(Path(pathCwd/Path(CLWLOGFILENAME)),mode='r',encoding='utf-8')
        cwlRowList = []
        for count,cwlRow in enumerate(textf,start=1):
            cwlRowList.append(cwlRow)
        textf.close()
        outputValue.return_Value = cwlRowList
        print('cloudWatchのLogは{}件'.format(count))
        return outputValue
    except OSError as e:
        print(e.args)
        print("CloudWatchのログファイル(テキストファイル)を開くことができません。")
        outputValue.status = False
        return outputValue
    except Exception as e:
        print(e.args)
        print('CloudWatchのログファイル読み込みでExceptionが発生しました。')
        outputValue.status = False
        return outputValue
    except:
        print('CloudWatchログファイル??')
        outputValue.status = False
        return outputValue

def concatDict(argCnntactFlowDict,argCloudWatchLogText):
    """ Amazon Connectのログ（dict）とCloud Watchのログ（str）を結合したdictを返す。

        Parameters:
        ----------
        argCnntactFlowDict:Dict
             Amazon connectのログ1行分
        argCloudWatchLogTex:string
                cloud Watchのログ1行分

        Returns:
        ----------
        outputValue:outputValueClass
            return_Valueに結合したログ(dict)
            statusに処理結果（正常／異常終了）のステータス(boolean)
    """
    outputValue = usdaw.outputValueClass()
    try:
        outPutDict = {key:item for key,item in argCnntactFlowDict.items()}   # 返却用のDictを作成
        outPutDict.update(CloudWatchLog=re.sub('\n','',argCloudWatchLogText))   # 返却用のDictにCLWのログを追加
        outputValue.return_Value = outPutDict
        return outputValue
    except Exception as e:
        print(e.args)
        print('ログの結合に失敗しました')
        outputValue.status = False
        return outputValue

def makeCsv(argCsvList):
    """ AmazonConnectとCloud Watchのログを結合したDictがListに纏まって
        渡されるので、Listを展開しながら、Dictをcsvファイルに保存していく。
        作成されるcsvファイル名は、定数RETURNCSVに設定する。
        Parameters:
        ----------
        argCsvList:List
             Amazon connectとCloud Watchのログ1行分(dict)を纏めたList

        Returns:
        ----------
        outputValue:outputValueClass
            return_Valueは設定無し
            statusに処理結果（正常／異常終了）のステータス(boolean)

    """
    count = 0
    outputValue = usdaw.outputValueClass()
    try:
        with open(Path(pathCwd/Path(RETURNCSV)),'w',encoding='utf-8') as f:
            # dictのlistを展開しながら、csvファイルに書き込んでいく。
            for csvRowDict in argCsvList:
                if count == 0:
                    # 最初はcsv.DictWriterの取得と、csvの項目行の作成
                    csvHedderStr = csvRowDict.keys()
                    csvWriter = csv.DictWriter(f,csvHedderStr)
                    csvWriter.writeheader()
                else:
                    csvWriter.writerow(csvRowDict)
                count+=1
            return outputValue
    except OSError as e:
        print(e.args)
        errorString = 'csvファイルの操作に失敗しました。{}'.format(RETURNCSV)
        print(errorString)
        outputValue.status = False
        return outputValue
    except Exception as e:
        print(e.args)
        print('csvファイルの作成に失敗しました。(予期せぬ例外){}'.format(RETURNCSV))
        outputValue.status = False
        return outputValue

def eraseNewLineAtBiginningOfLine():
    """ csvファイルの行頭に改行が入るので削除する処理。
        定数RETURNCSVに設定されたファイル名のcsvファイルをオープンし、
        行頭のスペースを削除しながら、
        定数RESULTCSVに設定されたファイル名のcsvファイルに保存する。

        Returns:
        ----------
        outputValue:outputValueClass
            return_Valueは設定無し
            statusに処理結果（正常／異常終了）のステータス(boolean)
    """
    outputValue = usdaw.outputValueClass()
    try:
        with open(Path(pathCwd/Path(RETURNCSV)),'r',encoding='utf-8') as fReader,\
                open(Path(pathCwd/Path(RESULTCSV )),'w',encoding='utf-8') as fWriter:
            for row in fReader:
                row = re.sub('^\n','',row)
                fWriter.write(row)
            return outputValue
    except OSError as e:
        print(e.args)
        errorString = 'csvファイルの操作に失敗しました（改行削除処理）。{}'.format(RETURNCSV)
        print(errorString)
        outputValue.status = False
        return outputValue
    except Exception as e:
        print(e.args)
        print('csvファイルの作成に失敗しました。（改行削除処理）（予期せぬ例外）'.format(RETURNCSV))
        outputValue.status = False
        return outputValue

def makeLastCsv(argConncatLogTexDictList):
    """ AmazonConnectとCloud WatchのログがまとまったDictがListに纏まって
        渡されるので、Listを展開しながら、Dictをcsvファイルに保存していく。

    """
    outputValue = usdaw.outputValueClass()
    try:
        makeCsvOutputValue = makeCsv(argConncatLogTexDictList)
        if makeCsvOutputValue.status:
            pass
        else:
            outputValue.status =False
            return outputValue
        # csvファイルの行頭に改行が入るので削除する処理。
        erasNewLineOutputValue = eraseNewLineAtBiginningOfLine()
        if erasNewLineOutputValue.status:
            pass
        else:
            outputValue.status =False
            return outputValue
    except Exception as e:
        print(e.args)
        print('csvファイルの作成に失敗しました。')
        outputValue.status =False
        return outputValue
    return outputValue  # 成功した場合はステータスTrueを返す

if __name__ == "__main__":
    try:
        # dic型を内包したlistでAmazon Connectのログ(csvファイル形式)を取り込む
        importContactSrcCsvOutputValue = import_contactSrc_csv()
        if importContactSrcCsvOutputValue.status:
            pass
        else:
            sys.exit()
        # dic型でCloud Watch のログを取り込む
        importWlogTxtOutputValue = import_wlog_txt()
        if importWlogTxtOutputValue.status:
            # cloudWatchのログを操作対象としてセット
            WlogClass.clwLogList = importWlogTxtOutputValue.return_Value
        else:
            sys.exit()
        # Amazon ConnectのコンタクトログとCloud Watchのログを結合する
        conncatLogTextDicList = []  # dic型で作成した結合した1行をまとめたList
        for csvRow  in importContactSrcCsvOutputValue.return_Value:
            sarchConntactId = csvRow[CONECTIDCSV]   # Amazon ConnectのcsvファイルからconntactIDを取得
            clwlgTxt = WlogClass.searchLogText(argContactID=sarchConntactId)
            # AmazonConnectのConntactlogとcludWatchのログを結合してDictで保存する。
            logTxtLine = concatDict(argCnntactFlowDict=csvRow,argCloudWatchLogText=clwlgTxt.return_Value)
            if logTxtLine.status:
                conncatLogTextDicList.append(logTxtLine.return_Value)
            else:
                sys.exit()

        # AmazonConnectのConntactlogとcludWatchのログを結合して作成したDictを、csv形式で保存する。
        makeLastCsvOutputValue = makeLastCsv(argConncatLogTexDictList=conncatLogTextDicList)
        if makeLastCsvOutputValue .status:
            pass
        else:
            sys.exit()

    except Exception as e:
        print(e.args)
        print("ログ成形の失敗")