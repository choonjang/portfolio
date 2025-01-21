from flask import Flask, render_template, redirect, request, session, flash, send_file
from datetime import timedelta
import requests
import datetime
import pymysql
import os

app = Flask(__name__)

app.config['SESSION_COOKIE_HTTPONLY'] = False
app.secret_key = "My_key"
app.permanent_session_lifetime = timedelta(minutes=180)

question_list = ["태어난 곳은?", "첫 사랑은?", "부모님 성함은?", "MBTI는?", "성서영 자취방 월세는?", "이은주 자취방 월세는?", "장준하의 생일은?"]
attack_type_list = ["image/jpeg", "image/jpg", "image/gif", "image/png", "image/webp"]
attack_extension_list = [".jpeg", ".jpg", ".gif", ".png", ".webp"]

@app.route('/')
def index():
    return render_template('index.html')

# 회원가입
@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        make_name = request.form["make_name"]
        make_ID = request.form["make_ID"]
        make_cel = request.form["make_cel"]
        make_mail = request.form["make_mail"]
        make_PW = request.form["make_PW"]
        check_PW = request.form["check_PW"]
        address_num = request.form["address_num"]
        address = request.form["address"]
        address_detail = request.form["address_detail"]
        address_hub = request.form["address_hub"]
        PW_question = request.form["PW_question"]
        PW_answer = request.form["PW_answer"]
        query = "select ID from INFO_TABLE where ID='{}'".format(make_ID)
        cursor.execute(query)
        result = cursor.fetchall()
        if result == ():
            if make_PW == check_PW:
                query = "insert into INFO_TABLE (NAME, ID, phone_num, e_mail, PW, address_num, address, address_detail, question, answer) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(make_name, make_ID, make_cel, make_mail, make_PW, address_num, address, address_detail, PW_question, PW_answer)
                cursor.execute(query)
                db_conn.commit()
                db_conn.close()
                flash('회원가입이 완료되었습니다.')
                return redirect('/')
            else:
                flash('입력하신 비밀번호가 다릅니다.')
                return render_template('sign_up.html', question_list=question_list, make_name=make_name, make_ID=make_ID, make_cel=make_cel, make_mail=make_mail, address_num=address_num, address=address, address_detail=address_detail, address_hub=address_hub, PW_question=PW_question, PW_answer=PW_answer)
        else:
            flash('동일한 ID가 존재합니다.')
            return render_template('sign_up.html', question_list=question_list, make_name=make_name, make_ID=make_ID, address_num=address_num, address=address, address_detail=address_detail, address_hub=address_hub, PW_question=PW_question, PW_answer=PW_answer)
    else:
        return render_template('sign_up.html', question_list=question_list)

# 로그인
@app.route('/login', methods = ['POST'])
def login():
    db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
    cursor = db_conn.cursor()
    login_ID = request.form["login_ID"]
    login_PW = request.form["login_PW"]
    query = "select ID, NAME from INFO_TABLE where ID='{}' and PW='{}'".format(login_ID, login_PW)
    cursor.execute(query)
    result = cursor.fetchall()
    db_conn.close()
    if result == ():
        flash('아이디 혹은 비밀번호가 틀렸습니다.')
        return redirect('/')
    else:
        session['id'] = result[0][0] + "_"
        session['user'] = result[0][1]
        return redirect('/checkpoint?login_id={}'.format(session['id']))
    
@app.route('/checkpoint')
def checkpoint():
    global login_id_check
    global upload_address
    global packet
    login_id_check = request.args["login_id"]
    upload_address = "http://10.0.10.2/session_jail"
    packet = {
        "login_id":login_id_check,
        "session_id":session['id']
    }
    try:
        if session['id'] == login_id_check:
            return redirect("/main?page=1&search=")
        else:
            session.pop('id', None)
            session.pop('user', None)
            requests.post(upload_address, data=packet)
            return redirect('/session_jail?num=1')
    except:
        requests.post(upload_address, data=packet)
        return redirect('/session_jail?num=2')

# @app.route('/checkpoint')
# def checkpoint():
#     global login_id_check
#     global upload_address
#     global packet
#     login_id_check = request.args["login_id"]
#     upload_address = "http://10.0.10.2/session_jail"
#     packet = {
#         "login_id":login_id_check,
#         "session_id":session['id']
#     }
#     try:
#         if session['id'] == login_id_check:
#             return redirect("/main?page=1&search=")
#         else:
#             requests.post(upload_address, data=packet)
#             return redirect("/main?page=1&search=")
#     except:
#         requests.post(upload_address, data=packet)
#         return redirect("/main?page=1&search=")

@app.route('/session_jail')
def session_jail():
    return "세션 변경이 탐지되었습니다. 관리자에게 확인 바랍니다."

@app.route('/session_jail_')
def session_jail_():
    return "세션 변경이 탐지되었습니다. 관리자에게 확인 바랍니다."

@app.route('/fileupload_jail')
def fileupload_jail():
    return "파일 업로드 공격이 탐지되었습니다. 관리자에게 확인 바랍니다."

@app.route('/fileupload_jail_')
def fileupload_jail_():
    return "파일 업로드 공격이 탐지되었습니다. 관리자에게 확인 바랍니다."

@app.route('/directory_jail')
def directory_jail():
    return "디렉토리 이동 공격이 탐지되었습니다. 관리자에게 확인 바랍니다."

@app.route('/directory_jail_')
def directory_jail_():
    return "디렉토리 이동 공격이 탐지되었습니다. 관리자에게 확인 바랍니다."

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('user', None)
    return redirect('/')

# 비밀번호 찾기
@app.route('/find_PW', methods = ['GET', 'POST'])
def find_PW():
    if request.method == 'POST':
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        find_name = request.form["find_name"]
        find_ID = request.form["find_ID"]
        find_question = request.form["find_question"]
        find_answer = request.form["find_answer"]
        query = "select pw from INFO_TABLE where name='{}' and ID='{}' and question='{}' and answer='{}'".format(find_name, find_ID, find_question, find_answer)
        cursor.execute(query)
        password = cursor.fetchall()
        db_conn.close()
        if password == ():
            flash('입력하신 정보가 틀렸습니다.')
            return render_template('find_PW.html', question_list=question_list, find_name=find_name, find_ID=find_ID, find_question=find_question, find_answer=find_answer)
        else:
            flash("비밀번호는 {} 입니다.".format(password[0][0]))
            return redirect('/')
    else:
        return render_template('find_PW.html', question_list=question_list)

@app.route('/main')
def main():
    if 'id' in session and 'user' in session:
        if session['id'] != login_id_check:
            requests.post(upload_address, data=packet)
        page = request.args['page']
        search = request.args['search']
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        query = "select * from board_table where title like '%{}%' order by day".format(search)
        cursor.execute(query)
        board_tup = cursor.fetchall()
        board_list = []
        for board_count in range(len(board_tup) - 1, -1, -1):
            board_list_mat = []
            board_list_mat.append(str(board_count + 1))
            for board_result in board_tup[board_count]:
                board_list_mat.append(board_result)
            board_list.append(board_list_mat)
        page_max = len(board_list) // 10 + 2
        db_conn.close()
        return render_template('main.html', board_list=board_list[ 10 * ( int(page) - 1 ) : 10 * int(page) ], page_max=page_max, page=page, search=search)
    else:
        return "세션 값이 없습니다."

@app.route('/view', methods = ['GET', 'POST'])
def view():
    if 'id' in session and 'user' in session:
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        title = request.args["title"]
        writer = request.args["writer"]
        day = request.args["day"]
        query = "select * from board_table where title='{}' and writer='{}' and day='{}'".format(title, writer, day)
        cursor.execute(query)
        view_result = cursor.fetchall()
        query = "select ID from INFO_TABLE where NAME='{}'".format(writer)
        cursor.execute(query)
        user_ID = cursor.fetchall()
        db_conn.close()
        upload_id = user_ID[0][0]
        upload_file_name = view_result[0][3]
        if upload_file_name == "":
            upload_id = ""
            upload_file_name = ""
        file_path = "file/{}_{}".format(day, view_result[0][3])
        if file_path == "file/{}_".format(day):
            file_path = ""
        return render_template('view.html', view_result=view_result[0], file_path=file_path, upload_id=upload_id, upload_file_name=upload_file_name, days=day)
    else:
        return "세션 값이 없습니다."

@app.route('/write', methods = ['GET', 'POST'])
def write():
    if 'id' in session and 'user' in session:
        today = datetime.datetime.now()
        writer = session['user']
        if request.method == 'POST':
            count = 0
            db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
            cursor = db_conn.cursor()
            title = request.form["title"]
            upload_file = request.files["upload_file"]
            content = request.form["content"]
            today_time = request.form["today_time"]
            upload_address = "http://10.0.10.2/fileupload_jail"
            packet = {
                "filename":upload_file.filename,
                "content_type":upload_file.content_type,
            }
            if upload_file.filename != "":
                for attack_type in attack_type_list:
                    if attack_type in upload_file.content_type:
                        count += 1
                for attack_extension in attack_extension_list:
                    if "../" in today_time:
                        packet = {
                            "upload_path":today_time,
                            "filename":upload_file.filename,
                            "content_type":upload_file.content_type,
                        }
                        upload_address = "http://10.0.10.2/directory_jail"
                        requests.post(upload_address, data=packet)
                        return redirect('/directory_jail_')
                    elif upload_file.filename.count(".") == 0 or upload_file.filename.count(".") > 1 or ";" in upload_file.filename or ":" in upload_file.filename:
                        requests.post(upload_address, data=packet)
                        return redirect('/fileupload_jail_')
                    elif attack_extension in upload_file.filename:
                        count += 1
                    else:
                        count += 1
                if count == 6:
                    upload_file.save("var/www/html/file/{}{}".format(today_time, upload_file.filename))
                else:
                    requests.post(upload_address, data=packet)
                    return redirect('/fileupload_jail')
            query = "insert into board_table (title, writer, day, file_name, content) values ('{}', '{}', '{}', '{}', '{}')".format(title, writer, str(today_time), upload_file.filename, content)
            cursor.execute(query)
            db_conn.commit()
            db_conn.close()
            flash('글 작성 완료')
            return redirect('/main?page=1&search=')
        else:
            return render_template('write.html', writer=writer, day=str(today).split('.')[0], today=str(today) + "_")
    else:
        return "세션 값이 없습니다."
    
@app.route('/download/file')
def download():
    if 'id' in session and 'user' in session:
        id = request.args["id"]
        files = request.args["files"]
        file_path = "file/{}{}".format(id, files)
        return send_file(file_path, as_attachment=True)
    else:
        return "세션 값이 없습니다."

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    if 'id' in session and 'user' in session:
        title = request.args["title"]
        writer = request.args["writer"]
        day = request.args["day"]
        content = request.args["content"]
        file_name = request.args["file_name"]
        file_path = request.args["file_path"]
        if writer == session['user'] or session['id'] == "admin_":
            today = datetime.datetime.now()
            if request.method == 'POST':
                db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
                cursor = db_conn.cursor()
                try:
                    if file_name != "":
                        os.remove("var/www/html/{}".format(file_path))
                except:
                    pass
                edit_title = request.form["edit_title"]
                edit_file = request.files["edit_file"]
                edit_content = request.form["edit_content"]
                if edit_file.filename != "":
                    edit_file.save("var/www/html/file/{}{}".format(session['id'], edit_file.filename))
                query = "update board_table set title = '{}', day = '{}', file_name = '{}', content = '{}' where title = '{}' and writer = '{}' and file_name = '{}' and content = '{}'".format(edit_title, today, edit_file.filename, edit_content, title, writer, file_name, content)
                cursor.execute(query)
                db_conn.commit()
                db_conn.close()
                flash('글 수정 완료')
                return redirect('/main?page=1&search=')
            else:
                return render_template('edit.html', title=title, writer=writer, day=str(today).split(" ")[0], content=content, file_name=file_name, file_path=file_path)
        else:
            flash('본인만 수정 가능합니다')
            return redirect('/view?title={}&writer={}&day={}'.format(title, writer, day))
    else:
        return "세션 값이 없습니다."

@app.route('/delete')
def delete():
    if 'id' in session and 'user' in session:
        title = request.args["title"]
        writer = request.args["writer"]
        day = request.args["day"]
        content = request.args["content"]
        file_path = request.args["file_paths"]
        if writer == session['user'] or session['id'] == "admin_":
            db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
            cursor = db_conn.cursor()
            query = "delete from board_table where title='{}' and writer='{}' and day='{}' and content='{}'".format(title, writer, day, content)
            try:
                if file_path != "":
                    os.remove("var/www/html/{}".format(file_path))
            except:
                pass
            cursor.execute(query)
            db_conn.commit()
            db_conn.close()
            flash('글 삭제 완료')
            return redirect('/main?page=1&search=')
        else:
            flash('본인만 삭제 가능합니다')
            return redirect('/view?title={}&writer={}&day={}'.format(title, writer, day))
    else:
        return "세션 값이 없습니다."

@app.route('/confirm_user', methods = ['GET', 'POST'])
def confirm_user():
    if session['id'] == "admin_":
        return redirect('/admin_page?page=1')
    if 'id' in session and 'user' in session:
        if request.method == 'POST':
            confirm_question = request.form["confirm_question"]
            confirm_answer = request.form["confirm_answer"]
            confirm_PW = request.form["confirm_PW"]
            db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
            cursor = db_conn.cursor()
            query = "select NAME from INFO_TABLE where NAME='{}' and ID='{}' and question='{}' and answer='{}' and PW='{}'".format(session['user'], str(session['id']).replace("_", ""), confirm_question, confirm_answer, confirm_PW)
            cursor.execute(query)
            check_user = cursor.fetchall()
            db_conn.close()
            if check_user == ():
                flash('입력하신 정보가 틀렸습니다.')
                return redirect('/confirm_user')
            else:
                session['permission'] = confirm_PW
                return redirect('/change_info')
        else:
            return render_template('confirm_user.html', question_list=question_list)
    else:
        return "세션 값이 없습니다."

@app.route('/change_info', methods = ['GET', 'POST'])
def change_info():
    if 'id' in session and 'user' in session and 'permission' in session or session['id'] == "admin_":
        if request.method == 'POST':
            new_password = request.form["new_password"]
            check_new_password = request.form["check_new_password"]
            if new_password == check_new_password:
                db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
                cursor = db_conn.cursor()
                query = "update INFO_TABLE set PW='{}' where NAME='{}' and ID='{}'".format(new_password, session['user'], str(session['id']).replace("_", ""))
                cursor.execute(query)
                db_conn.commit()
                db_conn.close()
                session.pop('permission', None)
                flash('비밀번호 변경 완료')
                return redirect('/main?page=1&search=')
            else:
                flash('입력하신 비밀번호가 다릅니다.')
                return redirect('/change_info')
        else:
            return render_template('change_info.html', id=str(session['id']).replace("_", ""))
    else:
        return "세션 값이 없습니다."

@app.route('/user_delete')
def user_delete():
    if 'id' in session and 'user' in session and 'permission' in session or session['id'] == "admin_":
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        query = "delete from INFO_TABLE where NAME='{}' and ID='{}'".format(session['user'], str(session['id']).replace("_", ""))
        cursor.execute(query)
        db_conn.commit()
        db_conn.close()
        flash('회원 탈퇴되었습니다.')
        return redirect('/')
    else:
        return "세션 값이 없습니다."
    
@app.route('/admin_page', methods = ['GET', 'POST'])
def admin_page():
    if session['id'] == "admin_" and 'user' in session:
        if request.method == 'POST':
            flash("전체 글이 삭제됩니다. 정말 글 삭제를 하시겠습니까????")
            return redirect('/admin_page?page=1')
        else:
            page = request.args['page']
            db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
            cursor = db_conn.cursor()
            query = "select * from INFO_TABLE where NAME not in ('admin')"
            cursor.execute(query)
            admin_board_tup = cursor.fetchall()
            admin_board_list = []
            for admin_board_count in range(len(admin_board_tup) - 1, -1, -1):
                admin_board_list_mat = []
                admin_board_list_mat.append(str(admin_board_count + 1))
                for admin_board_result in admin_board_tup[admin_board_count]:
                    admin_board_list_mat.append(admin_board_result)
                admin_board_list.append(admin_board_list_mat)
            page_max = len(admin_board_list) // 10 + 2
            db_conn.close()
            return render_template('admin.html', admin_board_list=admin_board_list[ 10 * ( int(page) - 1 ) : 10 * int(page) ], page_max=page_max, page=page)
    else:
        return '''
        <p>이곳은 관리자 페이지다.</p>
        <p>나가라</p>
        '''

@app.route('/delete_all_board')
def delete_all_board():
    if session['id'] == "admin_" and 'user' in session:
        db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
        cursor = db_conn.cursor()
        query = "TRUNCATE TABLE board_table"
        cursor.execute(query)
        db_conn.commit()
        db_conn.close()
        flash('전체 글 삭제 완료!')
        return redirect('/admin_page?page=1')
    else:
        return '''
        <p>이곳은 게시물 전체 삭제하는 페이지이다.</p>
        <p>실수로 2회 날려버렸으니 똑같은 실수를 하기 싫으면</p>
        <p>나가라</p>
        '''

@app.route('/admin_delete_user', methods = ['POST'])
def admin_delete_user():
    if session['id'] == "admin_" and 'user' in session:
        if request.method == 'POST':
            delete_name = request.form['name']
            delete_ID = request.form['ID']
            delete_PW = request.form['PW']
            db_conn = pymysql.connect(host='localhost', port=3306, user='skrookies', password='a13243546!', db='skrookies', charset='utf8')
            cursor = db_conn.cursor()
            query = "delete from INFO_TABLE where NAME='{}' and ID='{}' and PW='{}'".format(delete_name, delete_ID, delete_PW)
            cursor.execute(query)
            db_conn.commit()
            db_conn.close()
            flash('{} 삭제 완료!'.format(delete_name))
            return redirect('/admin_page?page=1')
    else:
        return '''
        <p>이곳은 어드민이 유저를 삭제하는 페이지 입니다.</p>
        <p>나가주세요</p>
        '''

if __name__ == '__main__':
    app.run(host="", port=5000, debug=False)