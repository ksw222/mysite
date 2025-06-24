# 프레임워크 로드
# lender_template : html문서를 덮어씌워서 사용자에게 보내는 class
# request : 요청보내는 class
import pandas as pd
from flask import Flask, render_template, request, url_for
from invest import Quant, load_data

# Flask class 생성
# 생성자 함수 필요한 인자 : 파일의 이름
app = Flask(__name__)


# 네비게이터 -> 복잡한 주소로 요청이 들어왔을때 함수와 연결
# route() 함수에 인자가 의미하는 것은?
# root url + 주소(route함수에 인자)
@app.route('/')
def index():
    # # csv 파일 로드
    # df = pd.read_csv('csv/AAPL.csv').tail(20)
    # # 컬름의 이름들을 리스트로 변경하여 변수에 저장
    # cols = list(df.columns)
    # # values를 리스트 안에 딕셔너리 형태로 변환
    # value = df.to_dict('records')
    # # 그래프에서 보여줄 데이터를 생성
    # x = list(df['Date'])
    # y = list(df['Adj Close'])
    # return render_template('index.html',
    #                        columns = cols,
    #                        values = value,
    #                        axis_x = x,
    #                        axis_y = y)
    return render_template('test.html')

@app.route('/main', methods=['post'])
def main():
    return render_template('index.html')

@app.route('/invest')
def invest():
    input_code = request.args['code']
    input_start_time = f"{request.args['s_year']}-{request.args['s_month']}-{request.args['s_day']}"
    input_end_time = f"{request.args['e_year']}-{request.args['e_month']}-{request.args['e_day']}"
    input_kind = request.args['kind']
    print(
        f"""
            {input_code}
            {input_start_time}
            {input_end_time}
            {input_kind}
        """
    )
    # input_code를 이용해서 csv파일을 로드
    df = pd.read_csv(f"csv/{input_code}.csv")
    quant = Quant(df, _start = input_start_time, _col='Close')

    if input_kind == 'bnh':
        result, rtn = quant.buyandhold()
    elif input_kind =='boll':
        result, rtn = quant.bollinger()
    elif input_kind == 'hall':
        result, rtn = quant.halloween()
    elif input_kind == 'mmt':
        result, rtn = quant.momentum()

    result.reset_index(inplace=True)

    result = result.loc[ result['rtn'] != 1, ]
    cols = list(result.columns)
    value = result.to_dict('records')
    x = list(result['Date'])
    y = list(result['acc_rtn'])
    res_data = {
        "columns" : cols,
        "values" : value,
        'axis_x' : x,
        'axis_y' : y
    }
    return res_data


# 웹서버를 실행
app.run(debug=True)