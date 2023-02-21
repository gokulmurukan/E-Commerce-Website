from django.urls import path
from customer import views


urlpatterns=[
    path("register/",views.SignupView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("home/",views.HomeView.as_view(),name="home"),
    path("products/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/<int:id>/cart/add/",views.AddToCartView.as_view(),name="cart-add"),
    path("customer/cart/",views.CartListView.as_view(),name="cart"),
    path("carts/<int:id>/change/",views.CartRemoveView.as_view(),name='cart_change'),
    path('orders/add/<int:id>',views.MakeOrderView.as_view(),name='create-order'),
    path('order/all',views.MyOrderView.as_view(),name="order-list"),
    path('order/<int:id>/cancel',views.OrderRemoveView.as_view(),name="cancelled"),
    path("offer/all",views.DiscountProductView.as_view(),name="offer-list"),
    path("reviews/<int:id>/add",views.ReviewCreateView.as_view(),name="review-add"),
    path("logout",views.signout_view,name="signout")

]