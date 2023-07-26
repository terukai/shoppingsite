from flask import Flask, render_template, request, redirect, url_for, session, flash
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    if db.login(user_name, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('mypage'))
    else :
        error = 'ログインに失敗しました。'
        
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    
    
    if user_name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが入力されていません'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('register.html', error=error)

@app.route('/goods_register')
def goods_register_form():
    return render_template('goods_register.html')

@app.route('/goods_register_exe', methods=['POST'])
def goods_register_exe():
    goods_name = request.form.get('goods_name')
    detail = request.form.get('detail')
    price = request.form.get('price')
    stock = request.form.get('stock')
    
    if goods_name == '':
        error = '商品名が入力されてません。'
        return render_template('goods_register.html', error=error)
    if detail == '':
        error = '詳細が入力されてません。'
        return render_template('goods_register.html', error=error)
    if price == '':
        error = '価格が入力されてません。'
        return render_template('goods_register.html', error=error)
    if stock == '':
        error = '在庫が入力されてません。'
        return render_template('goods_register.html', error=error)
    
    count = db.insert_goods(goods_name, detail, price, stock)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('goods_register_success', msg=msg))
    else:
        error = '登録に失敗しました。'
        print()
        return render_template('goods_register.html', error=error)
    
@app.route('/goods_register_success')
def goods_register_success():
    return render_template('goods_register_success.html')

@app.route('/delete_goods')
def delete_goods():
    return render_template('delete_goods.html')

@app.route('/delete_goods_exe', methods=['POST'])
def delete_goods_exe():
    id = request.form.get('id')
    
    if id == '':
        error = '商品IDが入力されていません'
        return render_template('delete_user.html', error=error)
    
    count = db.delete_goods(id)
    
    if count == 1:
        msg = '対象の商品を削除しました'
        return redirect(url_for('delete_goods_success', msg=msg))
    else:
        error = '対象の商品の削除に失敗しました'
        return render_template('delete_goods.html', error=error )
    
@app.route('/delete_goods_success')
def delete_goods_success():
    return render_template('delete_goods_success.html')
    
@app.route('/update_goods')
def update_goods():
    return render_template('update_goods.html')

@app.route('/update_goods_exe', methods=['POST'])
def update_goods_exe():
   
    name = request.form.get('goods_name')
    detail = request.form.get('detail')
    price = request.form.get('price')
    stock = request.form.get('stock')
    id = request.form.get('id')
    
    if id == '':
        error = '商品IDが入力されていません'
        return render_template('update_goods.html', error=error)
    
    count = db.update_goods(id, name, detail, price, stock)
    
    if count == 1:
        msg = '商品情報を編集しました'
        return redirect(url_for('update_goods_success', msg=msg))
    else:
        error = '商品情報の編集に失敗しました'
        return render_template('update_goods.html', error=error)
    
@app.route('/update_goods_success')
def update_goods_success():
    return render_template('update_goods_success.html')

@app.route('/update_user')
def update_user():
    return render_template('update_user.html')

# @app.route('/update_user_exe', methods=['POST'])
# def update_user_exe():
    
    
@app.route('/search_goods')
def search_goods():
    return render_template('search_goods.html')

@app.route('/search_goods_exe', methods=['POST'])
def search_goods_exe():
    name = request.form.get('goods_name')
    goods_list = db.search_goods(name)
    return render_template('goods_list.html', goods=goods_list)

@app.route('/admin_goods_list')
def admin_goods_list():
    goods_list = db.select_all_goods()
    return render_template('admin_goods_list.html', goods=goods_list)

if __name__ == '__main__':
    app.run(debug=True)