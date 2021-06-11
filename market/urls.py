from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path(
        'product-detail/<int:pk>',
        views.ProductDetailView.as_view(),
        name='product-detail'
    ),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='market/password-change.html',
            form_class=MyPasswordChangeForm,
            success_url='/password-change-done/'
        ),
        name='password-change'
    ),

    path(
        'password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='market/password-change-done.html',
        ),
        name='password-change-done'
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='market/password-reset.html',
            form_class=MyPasswordResetForm,
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='market/password-reset-done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='market/password-reset-confirm.html',
            form_class=MySetPasswordForm,
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='market/password-reset-complete.html'
        ),
        name='password_reset_complete',
    ),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('product/', views.product, name='product'),
    path('product/<slug:data>', views.product, name='product'),

    # path('login/', views.login, name='login'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='market/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),

    # path('register/', views.register, name='register'),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
