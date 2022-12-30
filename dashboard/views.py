from django.contrib import messages
from django.shortcuts import render, redirect
from . forms import *
from django.views import generic

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = Notes(user=request.user,title = request.POST['title'],desc=request.POST['desc'])
            note.save()
        messages.success(request,f' {request.user.username} Thêm ghi chú thành công !')
    else:
        form = NotesForm()
    note = Notes.objects.filter(user=request.user)
    context = {'notes':note,'form':form}
    return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NoteDetailView(generic.DetailView):
    model = Notes
