from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    
    path('account/', views.accountSettings, name="account"),
    
    #path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    
    #path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    #path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    #path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    
    # Submit email form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    # Email sent success message
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    # Link to password Reset form in email
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    # Passw3ord successfully changed message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),


    # Baralhos
    path('baralho/<int:id>/', views.baralho_detail, name='baralho_detail'),
    path('baralho/create/', views.baralho_create, name='baralho_create'),
    path('baralho/update/<int:id>/', views.baralho_update, name='baralho_update'),
    path('baralho/delete/<int:id>/', views.baralho_delete, name='baralho_delete'),

    # Cards
    path('card/<int:id>/', views.card_detail, name='card_detail'),
    path('card/create/<int:baralho_id>/', views.card_create, name='card_create'),
    path('card/update/<int:id>/', views.card_update, name='card_update'),
    path('card/delete/<int:id>/', views.card_delete, name='card_delete'),

    # Foruns
    path('foruns/', views.foruns_home, name='foruns_home'),
    path('foruns/create/', views.forum_create, name='forum_create'),
    path('forum/update/<int:id>/', views.forum_update, name='forum_update'),
    path('forum/delete/<int:id>/', views.forum_delete, name='forum_delete'),
    
    # Foruns e Mensagens
    path('forum/<int:id>/', views.forum_detail, name='forum_details'),
    path('forum/<int:forum_id>/mensagem/create/', views.mensagem_create, name='mensagem_create'),
    path('forum/<int:forum_id>/mensagem/delete/<int:mensagem_id>/', views.mensagem_delete, name='mensagem_delete'),

]