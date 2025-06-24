import pandas as pd
import numpy as np
from datetime import datetime

def bnh(
        _df,
        _start = '2010-01-01',
        _end = datetime.now(),
        _col = 'Adj close',
):
    # 데이터프레임의 복사본 생성
    df = _df.copy()

    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)
    # 인덱스를 시계열 데이터로 변경
    df.index = pd.to_datetime(df.index)
    # 결측치의 무한대 값 제거
    flag = df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df= df.loc[~flag, ]
    try : 
        df = df.loc[_start : _end, [_col]]
    except Exception as e:
        print(e)
        print('입력된 인자값이 잘못되었습니다.')
        return ""
    # 일별 수익률 계산하여 rtn 컬럼에 대입
    df['rtn'] = (df[_col].pct_change() +1).fillna(1)
    # 누적 수익률 계산하여 acc_rtn 컬럼에 대입
    df['acc_rtn'] = df['rtn'].cumprod()
    acc_rtn = df.iloc[-1, -1]
    # 결과 데이터프레임의 최종 누적 수익률을 되돌려준다.
    return df,acc_rtn