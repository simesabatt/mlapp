from django.shortcuts import render,redirect # 追加
from .forms import InputForm, LoginForm, SignUpForm # 追加
import joblib
import numpy as np
from .models import Customer # 追加

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate # 追加
from django.contrib.auth.decorators import login_required # 追加

# モデルの読み込み
loaded_model = joblib.load('model/ml_model.pkl') 
# Create your views here.

def index(request):
    return render(request, 'mlapp/index.html')

@login_required
def input_form(request):
    # 下記の様に編集
    if request.method == "POST": # Formの入力があった時、
        form = InputForm(request.POST) # 入力データを取得する。
        if form.is_valid(): # Formの記載の検証を行い、
            form.save() # 問題なければ、入力データを保存
            return redirect('result') # /resultへ遷移するように変更
    else:
        form = InputForm()
        return render(request, 'mlapp/input_form.html', {'form':form})

def result(request):
    # 最新の登録者のデータを取得
    data = Customer.objects.order_by('id').reverse().values_list('limit_balance', 'education', 'marriage', 'age') # 学習させたカラムの順番

    # 推論の実行
    x = np.array([data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    y_proba = y_proba * 100  # 予測確率を*100
    y, y_proba = y[0], y_proba[0]  # それぞれ0番目を取り出す

  # --------------------------下記を追加-------------------------
  # 推論結果を保存
    customer = Customer.objects.order_by('id').reverse()[0] # Customerの切り出し
    customer.proba = y_proba[y]
    customer.result = y
    customer.save() # データを保存
  # ---------------------------------------------------------------
    # 推論結果をHTMLに渡す
    return render(request, 'mlapp/result.html', {'y':y, 'y_proba':round(y_proba[y], 2)})

def history(request):
    if request.method == 'POST': # POSTメソッドが送信された場合
        d_id = request.POST # POSTされた値を取得→顧客ID
        d_customer = Customer.objects.filter(id=d_id['d_id']) # filterメソッドでidが一致するCustomerのデータを取得
        d_customer.delete() # 取得した顧客データを消去
        customers = Customer.objects.all() # 顧客全データを取得
        return render(request, 'mlapp/history.html', {'customers':customers})
    else:
        customers = Customer.objects.all()
        return render(request, 'mlapp/history.html', {'customers':customers})

# ログインページ
class Login(LoginView):
    form_class = LoginForm
    template_name = 'mlapp/login.html'

# ログアウトページ
class Logout(LogoutView):
    template_name = 'mlapp/base.html'

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      #フォームから'username'を読み取る
      username = form.cleaned_data.get('username')
      #フォームから'password1'を読み取る
      password = form.cleaned_data.get('password1')
      # 読み取った情報をログインに使用する情報として new_user に格納
      new_user = authenticate(username=username, password=password)
      if new_user is not None:
         # new_user の情報からログイン処理を行う
        login(request, new_user)
        # ログイン後のリダイレクト処理
        return redirect('index')
  # POST で送信がなかった場合の処理
  else:
    form = SignUpForm()
    return render(request, 'mlapp/signup.html', {'form': form})