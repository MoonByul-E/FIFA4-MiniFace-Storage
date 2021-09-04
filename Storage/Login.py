from flask import Blueprint, render_template, request
import mysql_UserData, json, bcrypt, Mail, string, random

Login_Blueprint = Blueprint("Login", __name__, url_prefix = "/login")
db_Class = mysql_UserData.Database()
main_Class = Mail.Mail()

def makeToken():
    Token_len = 64
    Token_Candidate = string.ascii_letters + string.digits

    Token = ""
    for i in range(Token_len):
        Token += random.choice(Token_Candidate)

    return Token

@Login_Blueprint.route("/login")
def function_Login():
    ID = request.args.get("ID")
    PW = request.args.get("PW")

    SQL = f"SELECT * FROM LoginData;"
    SELECT_LOGINDATA = db_Class.excuteAll(SQL)

    if SELECT_LOGINDATA: #데이터 있음
        for i in range(len(SELECT_LOGINDATA)): #데이터 전체 for문
            if SELECT_LOGINDATA[i]["ID"] == ID: # 아이디 있음
                if bcrypt.checkpw(PW.encode('utf-8'), SELECT_LOGINDATA[i]["PW"].encode('utf-8')): # 비밀번호 일치
                    Token = makeToken()

                    SQL = f"UPDATE LoginData SET TOKEN = \"{Token}\" WHERE ID = \"{ID}\";"
                    db_Class.execute(SQL)
                    db_Class.commit()
                    Success_Login = {
                        "Result": "Login Ok",
                        "Token": Token
                    }
                    return json.dumps(Success_Login)
                else: # 비밀번호 불일치
                    PW_Error = {
                        "Result": "PW Error"
                    }
                    return json.dumps(PW_Error)
            else: # 아이디 없음
                ID_Error = {
                    "Result": "ID Error"
                }
                return json.dumps(ID_Error)
    else:
        ID_Error = {
            "Result": "ID Error"
        }
        return json.dumps(ID_Error)

@Login_Blueprint.route("/register")
def function_Register():
    ID = request.args.get("ID")
    PW = request.args.get("PW")
    EMail = request.args.get("EMail")

    SQL = f"SELECT * FROM LoginData;"
    SELECT_LOGINDATA = db_Class.excuteAll(SQL)

    if SELECT_LOGINDATA: #데이터 있음
        for i in range(len(SELECT_LOGINDATA)): #데이터 전체 for문
            if SELECT_LOGINDATA[i]["ID"] == ID: # 아이디 중복
                ID_Overlap = {
                    "Result": "ID Overlap"
                }
                return json.dumps(ID_Overlap)

            elif SELECT_LOGINDATA[i]["EMail"] == EMail: #이메일 중복
                EMail_Overlap = {
                    "Result": "EMail Overlap"
                }
                return json.dumps(EMail_Overlap)

    SQL = f"INSERT INTO LoginData(ID, PW, EMail) VALUES(\"{ID}\", \"{bcrypt.hashpw(password=PW.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')}\", \"{EMail}\");"
    db_Class.execute(SQL)
    db_Class.commit()

    Success_Register = {
        "Result": "Register Ok",
        "ID": ID,
        "EMail": EMail
    }
    return json.dumps(Success_Register)

@Login_Blueprint.route("/idsearch")
def function_IDSearch():
    EMail = request.args.get("EMail")

    SQL = f"SELECT * FROM LoginData WHERE EMail = \"{EMail}\";"
    SELECT_LOGINDATA_WHERE_EMAIL = db_Class.excuteAll(SQL)

    if SELECT_LOGINDATA_WHERE_EMAIL:
        if SELECT_LOGINDATA_WHERE_EMAIL[0]["EMail"] == EMail:
            main_Class.sendMail(EMail, "FIFA4 미니저장소 아이디 찾기", f"아이디: {SELECT_LOGINDATA_WHERE_EMAIL[0]['ID']}")
            
            Success_Send = {
                "Result": "Send Ok"
            }
            return json.dumps(Success_Send)

        else:
            Error_Send = {
                "Result": "EMail Error"
            }
            return json.dumps(Error_Send)
    else:
        Error_Send = {
            "Result": "EMail Error"
        }
        return json.dumps(Error_Send)

@Login_Blueprint.route("/pwchange")
def function_PWChange():
    ID = request.args.get("ID")
    EMail = request.args.get("EMail")
    NewPW = request.args.get("NewPW")

    SQL = f"SELECT * FROM LoginData WHERE ID = \"{ID}\";"
    SELECT_LOGINDATA_WHERE_ID = db_Class.excuteAll(SQL)

    if SELECT_LOGINDATA_WHERE_ID:
        if SELECT_LOGINDATA_WHERE_ID[0]["EMail"] == EMail:
            SQL = f"UPDATE LoginData SET PW = \"{bcrypt.hashpw(password=NewPW.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')}\" WHERE ID = \"{ID}\";"
            db_Class.execute(SQL)
            db_Class.commit()
            main_Class.sendMail(EMail, "FIFA4 미니저장소 비밀번호 변경 알림", f"\"{SELECT_LOGINDATA_WHERE_ID[0]['ID']}\"의 비밀번호가 변경 되었습니다.")

            Success_Change = {
                "Result": "PW Change Ok"
            }
            return json.dumps(Success_Change)
        
        else:
            Error_Change = {
                "Result": "EMail Error"
            }
            return json.dumps(Error_Change)

    else:
        Error_Change = {
            "Result": "ID Error"
        }
        return json.dumps(Error_Change)