from django.urls import path
from . import views

urlpatterns = [
    # 將視圖函式改為 views.login_view，並保持別名為 name="login"
    path("login/", views.login_view, name="login"),
    
    # 登出路由
    path("logout/", views.logout_view, name="logout"),
]