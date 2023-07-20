import csv
from pathlib import Path
import re

pathCwd = Path.cwd() #�J�����g�p�X��ݒ�
print(pathCwd)

CSVFILENAME = 'contactSrchResult.csv' # AmazonConnct�̃R���^�N�g���O�t�@�C��
CLWLOGFILENAME = 'cwl.txt'           # Cloud Watch�̃��O�t�@�C��
CONECTIDCSV = 'AzcContactId'          # ConnectId �̍��ږ�(AmazonConnect�̃��O�t�@�C��)
CONNECTIDCLW = 'ContactId'            # CloudWatch�̃��O�t�@�C��
RETURNCSV = 'wokrfile.csv'            # "Error"�Ƃ����P����܂�log�̈ꗗ(�A���]�v�ȉ��s���c��)
RESULTCSV = 'about_error_string.csv'  # �ŏI����"Error"�Ƃ����P����܂�log�̈ꗗ

def import_contactSrc_csv():
    # Amazon Connect�̐ؒf�̗�������荞��
    # ��荞�ރt�@�C����csv�`��
    # ��荞�񂾌��ʂ�list�ŕԂ�
    with open(Path(pathCwd/Path(CSVFILENAME)))as csvf:
        csvFileDicObj = csv.DictReader(csvf)
        csvFileDicList = [row for row in csvFileDicObj]
    return csvFileDicList

def import_wlog_txt():
    # Amazon Connect��Cloud Watch log����荞��
    # ��荞�ރt�@�C����txt�`��
    # ��荞�񂾌��ʂ�list�ŕԂ��B
    with open(Path(pathCwd/Path(CLWLOGFILENAME)),mode='r',encoding='utf-8') as textf:
        cwlRowList = []
        cwlRow = textf.readline()
        cwlRowList.append(cwlRow)
        while cwlRow != '':     # �ǂݍ��ݍs����ɂȂ�܂�
            cwlRow = textf.readline()
            cwlRowList.append(cwlRow)
    return cwlRowList

class WlogClass:
    # cloud Watch log��list��ێ�����N���X�B
    # �Ăяo��������Z�b�g���ꂽ�p�����[�^���܂ރ��O������΂����Ԃ��B
    # �Ăяo���ꂽ���O��WlogClass����폜����
    clwLogList=[]

    def __init__(self) -> None:
        pass

    @classmethod
    def _deleteST(cls,tgIndex):
       # �����ŌĂяo���ꂽ���O�͍폜����
       del cls.clwLogList[tgIndex]

    @classmethod
    def searchLogText(cls,argContactID):
        # �R���^�N�gID��Cloud Watch�̃��O�e�L�X�g����������B
        count = 0
        outPutValue = 'NoErrorString'
        for row in cls.clwLogList:
           # print('��������{c} �Ώە�����{r}'.format(r=row,c=argContactID))
            if argContactID in row:
                outPutValue = row
                # ���O��Ԃ�����A���Y���O��clwLogList����폜����
                cls._deleteST(tgIndex=count)
                return outPutValue
            count+=1
        return outPutValue


def concatDict(argCnntactFlowDict,argCloudWatchLogText):
    # �������ꂽdict��Ԃ��B
    #argCnntactFlowDict.update(CloudWatchLog=argCloudWatchLogText)
    outPutDict = {key:item for key,item in argCnntactFlowDict.items()}   # �ԋp�p��Dict���쐬
    outPutDict.update(CloudWatchLog=re.sub('\n','',argCloudWatchLogText))   # �ԋp�p��Dict��CLW�̃��O��ǉ�
    return outPutDict

def makeLastCsv(argConncatLogTexDictList):
    # AmazonConnect��Cloud Watch�̃��O���܂Ƃ܂���Dict��List�ɓZ�܂���
    # �n�����̂ŁAList��W�J���Ȃ���ADict��csv�t�@�C���ɕۑ����Ă����B
    count = 0
    with open(Path(pathCwd/Path(RETURNCSV)),'w',encoding='utf-8') as f:
        # dict��list��W�J���Ȃ���Acsv�t�@�C���ɏ�������ł����B
        for csvRowDict in argConncatLogTexDictList:
            if count == 0:
                # �ŏ���csv.DictWriter�̎擾�ƁAcsv�̍��ڍs�̍쐬
                csvHedderStr = csvRowDict.keys()
                csvWriter = csv.DictWriter(f,csvHedderStr)
                csvWriter.writeheader()
            csvWriter.writerow(csvRowDict)
            count+=1

    # csv�t�@�C���̍s���ɉ��s������̂ō폜���鏈���B
    with open(Path(pathCwd/Path(RETURNCSV)),'r',encoding='utf-8') as fReader,\
            open(Path(pathCwd/Path(RESULTCSV )),'w',encoding='utf-8') as fWriter:
        for row in fReader:
            row = re.sub('^\n','',row)
            fWriter.write(row)

if __name__ == "__main__":
    # dic�^������list��Amazon Connect�̃��O(csv�t�@�C���`��)����荞��
    conntactFlowDicList = import_contactSrc_csv()

    # dic�^��Cloud Watch �̃��O����荞��
    cloudWatchDicList =  import_wlog_txt()
    #print(cloudWatchDicList)

    # cloudWatch�̃��O�𑀍�ΏۂƂ��ăZ�b�g
    WlogClass.clwLogList = cloudWatchDicList

    # Amazon Connect�̃R���^�N�g���O��Cloud Watch�̃��O����������
    conncatLogTextDicList = []  # dic�^�ō쐬������������1�s���܂Ƃ߂�List
    for csvRow  in conntactFlowDicList:
        sarchConntactId = csvRow[CONECTIDCSV]   # Amazon Connect��csv�t�@�C������conntactID���擾
        clwlgTxt = WlogClass.searchLogText(argContactID=sarchConntactId)
        logTxtLine = concatDict(argCnntactFlowDict=csvRow,argCloudWatchLogText=clwlgTxt)
        # AmazonConnect��Conntactlog��cludWatch�̃��O���������č쐬����Dict���Acsv�`���ŕۑ�����B
        conncatLogTextDicList.append(logTxtLine)
        makeLastCsv(argConncatLogTexDictList=conncatLogTextDicList)
