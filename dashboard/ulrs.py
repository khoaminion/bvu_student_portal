from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path('delete_note/<int:pk>',views.delete_note,name='delete-note'),
    path('note_detail/<int:pk>',views.NoteDetailView.as_view(),name='note-detail'),
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update-homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete-homework'),
    path('youtube',views.youtube,name='youtube'),
    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update-todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete-todo'),
    path('books',views.books,name='books'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wiki',views.wiki,name='wiki'),
    path('conversion',views.conversion,name='conversion'),
    path('register',views.register,name='register'),
    path('news',views.news,name='news'),
    path('update_todo_profile/<int:pk>',views.update_todo_profile,name='update-todo-profile'),
    path('update_homework_profile/<int:pk>',views.update_homework_profile,name='update-homework-profile'),
    path('delete_todo_profile/<int:pk>',views.delete_todo_profile,name='delete-todo-profile'),
    path('delete_homework_profile/<int:pk>',views.delete_homework_profile,name='delete-homework-profile'),
    path('reset_password/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]