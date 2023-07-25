import csv
from pathlib import Path
import re

pathCwd = Path.cwd() #カレントパスを設定
print(pathCwd)

CSVFILENAME = 'contactSrchResult.csv' # AmazonConnctのコンタクトログファイル
CLWLOGFILENAME = 'cwl.txt'           # Cloud Watchのログファイル
CONECTIDCSV = 'AzcContactId'          # ConnectId の項目名(AmazonConnectのログファイル)
CONNECTIDCLW = 'ContactId'            # CloudWatchのログファイル
RETURNCSV = 'wokrfile.csv'            # "Error"という単語を含んだlogの一覧(但し余計な改行が残る)
RESULTCSV = 'about_error_string.csv'  # 最終結果"Error"という単語を含んだlogの一覧

def import_contactSrc_csv():
    # Amazon Connectの切断の履歴を取り込む
    # 取り込むファイルはcsv形式
    # 取り込んだ結果をlistで返す
    with open(Path(pathCwd/Path(CSVFILENAME)))as csvf:
        csvFileDicObj = csv.DictReader(csvf)
        csvFileDicList = [row for row in csvFileDicObj]
    return csvFileDicList

def import_wlog_txt():
    # Amazon ConnectのCloud Watch logを取り込む
    # 取り込むファイルはtxt形式
    # 取り込んだ結果をlistで返す。
    with open(Path(pathCwd/Path(CLWLOGFILENAME)),mode='r',encoding='utf-8') as textf:
        cwlRowList = []
        cwlRow = textf.readline()
        cwlRowList.append(cwlRow)
        while cwlRow != '':     # 読み込み行が空になるまで
            cwlRow = textf.readline()
            cwlRowList.append(cwlRow)
    return cwlRowList

class WlogClass:
    # cloud Watch logのlistを保持するクラス。
    # 呼び出し元からセットされたパラメータを含むログがあればそれを返す。
    # 呼び出されたログはWlogClassから削除する
    clwLogList=[]

    def __init__(self) -> None:
        pass

    @classmethod
    def _deleteST(cls,tgIndex):
       # 検索で呼び出されたログは削除する
       del cls.clwLogList[tgIndex]

    @classmethod
    def searchLogText(cls,argContactID):
        # コンタクトIDでCloud Watchのログテキストを検索する。
        count = 0
        outPutValue = 'NoErrorString'
        for row in cls.clwLogList:
           # print('検索文字{c} 対象文字列{r}'.format(r=row,c=argContactID))
            if argContactID in row:
                outPutValue = row
                # ログを返したら、当該ログはclwLogListから削除する
                cls._deleteST(tgIndex=count)
                return outPutValue
            count+=1
        return outPutValue


def concatDict(argCnntactFlowDict,argCloudWatchLogText):
    # 結合されたdictを返す。
    #argCnntactFlowDict.update(CloudWatchLog=argCloudWatchLogText)
    outPutDict = {key:item for key,item in argCnntactFlowDict.items()}   # 返却用のDictを作成
    outPutDict.update(CloudWatchLog=re.sub('\n','',argCloudWatchLogText))   # 返却用のDictにCLWのログを追加
    return outPutDict

def makeLastCsv(argConncatLogTexDictList):
    # AmazonConnectとCloud WatchのログがまとまったDictがListに纏まって
    # 渡されるので、Listを展開しながら、Dictをcsvファイルに保存していく。
    count = 0
    with open(Path(pathCwd/Path(RETURNCSV)),'w',encoding='utf-8') as f:
        # dictのlistを展開しながら、csvファイルに書き込んでいく。
        for csvRowDict in argConncatLogTexDictList:
            if count == 0:
                # 最初はcsv.DictWriterの取得と、csvの項目行の作成
                csvHedderStr = csvRowDict.keys()
                csvWriter = csv.DictWriter(f,csvHedderStr)
                csvWriter.writeheader()
            csvWriter.writerow(csvRowDict)
            count+=1

    # csvファイルの行頭に改行が入るので削除する処理。
    with open(Path(pathCwd/Path(RETURNCSV)),'r',encoding='utf-8') as fReader,\
            open(Path(pathCwd/Path(RESULTCSV )),'w',encoding='utf-8') as fWriter:
        for row in fReader:
            row = re.sub('^\n','',row)
            fWriter.write(row)

if __name__ == "__main__":
    # dic型を内包したlistでAmazon Connectのログ(csvファイル形式)を取り込む
    conntactFlowDicList = import_contactSrc_csv()

    # dic型でCloud Watch のログを取り込む
    cloudWatchDicList =  import_wlog_txt()
    #print(cloudWatchDicList)

    # cloudWatchのログを操作対象としてセット
    WlogClass.clwLogList = cloudWatchDicList

    # Amazon ConnectのコンタクトログとCloud Watchのログを結合する
    conncatLogTextDicList = []  # dic型で作成した結合した1行をまとめたList
    for csvRow  in conntactFlowDicList:
        sarchConntactId = csvRow[CONECTIDCSV]   # Amazon ConnectのcsvファイルからconntactIDを取得
        clwlgTxt = WlogClass.searchLogText(argContactID=sarchConntactId)
        logTxtLine = concatDict(argCnntactFlowDict=csvRow,argCloudWatchLogText=clwlgTxt)
        # AmazonConnectのConntactlogとcludWatchのログを結合して作成したDictを、csv形式で保存する。
        conncatLogTextDicList.append(logTxtLine)
        makeLastCsv(argConncatLogTexDictList=conncatLogTextDicList)
