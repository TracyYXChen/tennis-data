import pandas as pd
import os

RAW_DIR = 'raw'
RAW_MATCHES = 'all_matches.csv'
RAW_LIST = 'top2000info.csv'
PROCESSED_DIR = 'processed'

if not os.path.exists(RAW_DIR):
    raise FileExistsError('Please put your files %s and %s under %s'%(RAW_MATCHES, RAW_LIST, RAW_DIR))

if not os.path.exists(PROCESSED_DIR):
    os.mkdir(PROCESSED_DIR)
PROCESSED_LIST = 'processedList.csv'
PROCESSED_MATCHES = 'processedMatches.csv'
FIRST_YEAR_MATCHES = 'firstYearMatches.csv'
rawListPath = os.path.join(RAW_DIR, RAW_LIST)
outListPath = os.path.join(PROCESSED_DIR, PROCESSED_LIST)
rawMatchPath = os.path.join(RAW_DIR, RAW_MATCHES)
outMatchPath = os.path.join(PROCESSED_DIR, PROCESSED_MATCHES)
firstMatchPath = os.path.join(PROCESSED_DIR, FIRST_YEAR_MATCHES)


def processFullList(cutoff=1993):
    selectedColumns = ['pid', 'birthday', 'age_year', 'age_day', 'ioc', 'first_name', 'last_name', 'pro_year', 'height', 'hand', 
    'rank_single_ch', 'rank_single_ch_date']
    rawDf = pd.read_csv(rawListPath, sep=',')[selectedColumns]
    #processedDf = rawDf[rawDf['pro_year'] >= cutoff]
    rawDf.to_csv(outListPath, index=False)


def processMatches():
    selectedColumns = ['pid', 'ioc', 'year', 'start', 'level', 'sfc', 'games', 'o_id', 'o_rank', 'wl']
    rawDf = pd.read_csv(rawMatchPath, sep=',')[selectedColumns]
    idList = list(pd.read_csv(outListPath, sep=',')['pid'])
    processedDf = rawDf[rawDf['pid'].isin(idList)]
    processedDf.to_csv(outMatchPath, index=False)

def proYearMatches():
    # proyear and the year after that
    yearAfter = 1
    matchDf = pd.read_csv(outMatchPath, sep=',')
    idDf = pd.read_csv(outListPath, sep=',')
    proYearDict = dict(zip(list(idDf['pid']), list(idDf['pro_year'])))
    #print(proYearDict)
    # for each player, only keep matches that happened within $yearAfter the $pro_year
    CUTOFFYEAR = 'cutoffYear'
    matchDf[CUTOFFYEAR] = matchDf.apply(lambda row: proYearDict[row['pid']] + yearAfter, axis=1) 
    #print(matchDf)
    matchDf[matchDf['year'] <=  matchDf[CUTOFFYEAR]].to_csv(firstMatchPath, index=False)



if __name__ == "__main__":
    print("processed files...")
    processFullList()
    processMatches()
    #proYearMatches()