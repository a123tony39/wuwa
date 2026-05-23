from django.shortcuts import render, redirect
from django.contrib.auth import logout, login as auth_login # 將內建的 login 重新命名，避免跟你的 views 名稱衝突
from django.contrib.auth.forms import AuthenticationForm  # Django 內建的標準登入表單
from django.conf import settings

def login_view(request): # 建議改名為 login_view，避免跟 django 內建的 login 撞名
    # 如果使用者已經登入過，直接送他回首頁，不用再看登入頁
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # 1. 接收前端送來的 POST 表單數據
        form = AuthenticationForm(request, data=request.POST)
        
        # 2. 驗證帳號密碼是否正確
        if form.is_valid():
            # 取得驗證成功的 user 物件
            user = form.get_user()
            
            # 3. 真正執行 Django 登入，寫入 Session 狀態
            auth_login(request, user)
            
            # 4. 登入成功！跳轉到 settings.py 設定的 LOGIN_REDIRECT_URL (首頁)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # 如果是 GET 請求（普通瀏覽網頁），就給他一個空的表單
        form = AuthenticationForm()
        
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')