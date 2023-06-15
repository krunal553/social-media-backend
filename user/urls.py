from django.urls import path
from . import views

urlpatterns = [
    # signup and otp verification
    path("signup/", views.signupUser, name="signup"),
    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify/", views.verify, name="verify"),
    path("check_email/", views.check_email, name="check_email"),
    
    path("login/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("change_password/", views.change_password, name='change_password'),
    path("reset_password/", views.reset_password, name='reset_password'),
    path("current-user/", views.getCurrentUserProfile, name="user-profile"),
    path("", views.getUsers, name="user"),

    path('update_profile/', views.update_profile, name='update_profile'),


    path("following/", views.following, name="following"),

    path("<str:username>/follow/", views.follow_user, name="follow_user"),
    path("<str:username>/isfollowing/", views.getIsFollowing, name="isfollowing"),
    path("<str:username>/profile/", views.getUserProfile, name="user-profile"),
    path("search/", views.searchUser, name="search-user"),

    


]