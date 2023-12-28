from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm, MyPasswordResetForm,MyPasswordChangeForm, MySetPasswordForm
from django.contrib.auth import views as auth_view
from django.contrib import admin
urlpatterns = [
    path("", views.home),
    path("about/", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("categorytitle/<val>", views.CategoryTitle.as_view(), name="categorytitle"),
    path("productdetail/<int:pk>", views.ProductDetail.as_view(), name="productdetail"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>", views.updateAddress.as_view(), name="updateAddress"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name="showcart"),
    path('checkout/',views.checkout.as_view(), name="checkout"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/',views.orders, name='orders'),
    path('pluswishlist/', views.plus_wishlist, name= 'plus_wishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minus_wishlist'),
    path('search/', views.search, name='search'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    

#login Authentication
    path('registraion/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm
                                                                 ,success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('logout/', auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header="Noor Dairy Products"
admin.site.site_title="Noor Dairy Products"
admin.site.site_index_title="Welcome to Noor Dairy Products"