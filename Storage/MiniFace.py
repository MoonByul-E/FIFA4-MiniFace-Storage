from io import IOBase
from flask import Blueprint, render_template, request
import mysql_UserData ,mysql_FIFA4, json, bcrypt, Mail, string, random, requests, base64, os

MiniFace_Blueprint = Blueprint("MiniFace", __name__, url_prefix = "/miniface")
db_Class = mysql_FIFA4.Database()
db_Class_UserData = mysql_UserData.Database()
main_Class = Mail.Mail()

playerData = requests.get("https://static.api.nexon.co.kr/fifaonline4/latest/spid.json")
playerJson = json.loads(playerData.content)

@MiniFace_Blueprint.route("/board/<PlayerCode>")
def function_Board(PlayerCode):
    Token = request.args.get("Token")

    SQL = f"SELECT * FROM LoginData WHERE TOKEN = \'{Token}\';"
    SELECT_LOGINDATA_WHERE_TOKEN = db_Class_UserData.excuteAll(SQL)
    print(SELECT_LOGINDATA_WHERE_TOKEN)

    isFind = False

    if SELECT_LOGINDATA_WHERE_TOKEN: # 정상적인 토큰이면
        if len(PlayerCode) == 6 and PlayerCode.isdigit(): # 선수 코드가 6자리 및 숫자로 이루워져있을때
            for i in range(len(playerJson)):
                if str(playerJson[i]["id"])[3:] == PlayerCode: # 해당 선수 코드가 존재하는 선수코드일때
                    isFind = True

                    SQL = f"SHOW TABLES LIKE 'Board_{PlayerCode}';"
                    SHOW_TABLES_LIKE = db_Class.excuteAll(SQL)

                    if not SHOW_TABLES_LIKE: # 선수 코드 테이블이 없다면
                        SQL = f"""CREATE TABLE Board_{PlayerCode}(
                                No int not null AUTO_INCREMENT,
                                Title varchar(100),
                                Author varchar(100),
                                primary key(No)
                            );"""
                        db_Class.execute(SQL)
                        db_Class.commit()
                        os.mkdir(f"./Storage/static/img/{PlayerCode}")

                        Result_Board = [{
                            "No": -1,
                            "Title": "업로드된 미니 페이스가 없습니다. 첫 미니 페이스를 업로드 해보세요!",
                            "Author": "없음"
                        }]

                        Success_NewBoard = {
                            "Result": "Success Board",
                            "Array": str(Result_Board)
                        }
                        return json.dumps(Success_NewBoard, ensure_ascii=False)

                    else: # 선수 코드 테이블이 있다면
                        SQL = f"SELECT * FROM Board_{PlayerCode}"
                        SELECT_BOARD = db_Class.excuteAll(SQL)

                        if SELECT_BOARD: # 빈 테이블이 아니면
                            Success_Board = {
                                "Result": "Success Board",
                                "Array": str(SELECT_BOARD)
                            }
                            return json.dumps(Success_Board, ensure_ascii=False)

                        else: # 빈 테이블이면
                            Result_Board = [{
                                "No": -1,
                                "Title": "업로드된 미니 페이스가 없습니다. 첫 미니 페이스를 업로드 해보세요!",
                                "Author": "없음"
                            }]

                            Success_NewBoard = {
                                "Result": "Success Board",
                                "Array": str(Result_Board)
                            }
                            return json.dumps(Success_NewBoard, ensure_ascii=False)

            if isFind == False: # 선수 코드가 올바르지 않을때 
                PlayerCode_Error = {
                    "Result": "PlayerCode Error"
                }
                return json.dumps(PlayerCode_Error)

        else: # 선수 코드가 올바르지 않을때   
            PlayerCode_Error = {
                "Result": "PlayerCode Error"
            }
            return json.dumps(PlayerCode_Error)

    else: # 비정상적인 토큰일때
        Token_Error = {
            "Result": "Token Error"
        }
        return json.dumps(Token_Error)

@MiniFace_Blueprint.route("/upload/<PlayerCode>")
def function_Upload(PlayerCode):
    Title = request.args.get("Title")
    Base64 = request.args.get("Base64").replace(" ", "+").encode("UTF-8")
    Token = request.args.get("Token")

    SQL = f"SELECT * FROM LoginData WHERE TOKEN = \'{Token}\';"
    SELECT_LOGINDATA_WHERE_TOKEN = db_Class_UserData.excuteAll(SQL)

    if SELECT_LOGINDATA_WHERE_TOKEN: # 정상적인 토큰이면
        if len(PlayerCode) == 6 and PlayerCode.isdigit(): # 선수 코드가 6자리 및 숫자로 이루워져있을때
            for i in range(len(playerJson)):
                if str(playerJson[i]["id"])[3:] == PlayerCode: # 해당 선수 코드가 존재하는 선수코드일때
                    SQL = f"SHOW TABLES LIKE 'Board_{PlayerCode}';"
                    SHOW_TABLES_LIKE = db_Class.excuteAll(SQL)

                    if not SHOW_TABLES_LIKE: # 선수 코드 테이블이 없다면
                        Table_Error = {
                            "Result": "Table Error"
                        }
                        return json.dumps(Table_Error)

                    else: # 선수 코드 테이블이 있다면
                        SQL = f"INSERT INTO Board_{PlayerCode}(Title, Author) VALUES(\"{Title}\", \"{SELECT_LOGINDATA_WHERE_TOKEN[0]['ID']}\");"
                        db_Class.execute(SQL)
                        db_Class.commit()

                        with open(f"./Storage/static/img/{PlayerCode}/{db_Class.getID()}.png", "wb") as fh:
                            fh.write(base64.decodebytes(Base64))

                        Success_Upload = {
                            "Result": "Upload Ok"
                        }

                        return json.dumps(Success_Upload)


    #with open("imageToSave.png", "wb") as fh:
        #fh.write(base64.decodebytes(Base64))

    print(type(Base64))
    return str(db_Class.getID())