from django.shortcuts import render, redirect
from django.contrib.auth import logout, login as auth_login 
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # 接收前端送來的 POST 表單數據
        form = AuthenticationForm(request, data=request.POST)
        
        # 驗證帳號密碼是否正確
        if form.is_valid():
            # 取得驗證成功的 user 物件
            user = form.get_user()
            
            # 真正執行 Django 登入，寫入 Session 狀態
            auth_login(request, user)
            
            # 登入成功跳轉到 settings.py 設定的 LOGIN_REDIRECT_URL (首頁)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # GET 請求（普通瀏覽網頁），給一個空的表單
        form = AuthenticationForm()
        
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')