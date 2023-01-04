from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@csrf_exempt
@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = Notes(user=request.user,title = request.POST['title'],desc=request.POST['desc'])
            note.save()
            messages.success(request,f' {request.user.username} Thêm ghi chú thành công !')
            return HttpResponseRedirect('/notes')           
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NoteDetailView(generic.DetailView):
    model = Notes

csrf_exempt
@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                desc = request.POST['desc'],
                due = request.POST['due'],
                is_finished = finished
            )
            homework.save()
            messages.success(request,f' {request.user.username} Thêm bài tập thành công !')
            return HttpResponseRedirect('/homework')
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks':homeworks,'homeworks_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return HttpResponseRedirect('/homework')

@login_required
def update_homework_profile(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return HttpResponseRedirect('/profile')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return HttpResponseRedirect('/homework')

@login_required
def delete_homework_profile(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return HttpResponseRedirect('/profile')

csrf_exempt
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'embedlink':i['link'].replace('watch?v=','embed/'),
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            print(i['link'].replace('watch?v=','embed/'))
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/youtube.html',context)


csrf_exempt
@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todo.save()
            messages.success(request,f' {request.user.username} Thêm công việc thành công !')
            return HttpResponseRedirect('/todo')
    else:
        form = TodoForm
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos':todos,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return HttpResponseRedirect('/todo')

@login_required
def update_todo_profile(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return HttpResponseRedirect('/profile')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return HttpResponseRedirect('/todo')

@login_required
def delete_todo_profile(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return HttpResponseRedirect('/profile')

csrf_exempt
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/books.html',context)

csrf_exempt
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics': phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form ,
                'input':''
            }
        return render(request,'dashboard/dictionary.html', context)
    else:
        print('fail')
        form = DashboardForm()
        context = {'form':form}
    return render(request, 'dashboard/dictionary.html', context)

csrf_exempt
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary

        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/wiki.html',context)

csrf_exempt
def conversion(request):
    if request.method =='POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measrurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form': measrurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int (input) >=0:
                    if first == 'yard' and second == 'feet':
                        answer = f'{input} yard = {int(input)*3} feet'
                    if first == 'yard' and second == 'mile':
                        answer = f'{input} yard = {int(input)*0.0005681818} mile'
                    
                    if first == 'feet' and second == 'yard':
                        answer = f'{input} feet = {int(input)*0.33333333} yard'
                    if first == 'feet' and second == 'mile':
                        answer = f'{input} feet = {int(input)*0.0001893939} mile'

                    if first == 'mile' and second == 'feet':
                        answer = f'{input} mile = {int(input)*5280} feet'
                    if first == 'mile' and second == 'yard':
                        answer = f'{input} mile = {int(input)*1760} yard'
                context = {
                    'form':form,
                    'm_form':measrurement_form,
                    'input': True,
                    'answer':answer                    
                }    
        if request.POST['measurement'] == 'speed':
            measrurement_form = ConversionSpeedForm()
            context = {
                'form':form,
                'm_form': measrurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int (input) >=0:
                    if first == 'kmh' and second == 'mph':
                        answer = f'{input} Km/h = {int(input)*0.621371192} mph'
                    if first == 'mph' and second == 'kmh':
                        answer = f'{input} mph = {int(input)*1.609344} Km/h'

                    if first == 'ms' and second == 'mph':
                        answer = f'{input} m/s = {int(input)*2.2369362921} mph'
                    if first == 'ms' and second == 'kmh':
                        answer = f'{input} m/s = {int(input)*3.6} Km/h'

                    if first == 'kmh' and second == 'ms':
                        answer = f'{input} Km/h = {int(input)*0.2777777778} m/s'
                    if first == 'mph' and second == 'ms':
                        answer = f'{input} mph = {int(input)*0.44704} m/s'
                context = {
                    'form':form,
                    'm_form':measrurement_form,
                    'input': True,
                    'answer':answer                    
                }                        
        if request.POST['measurement'] == 'mass':
            measrurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form': measrurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int (input) >=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                    
                    if first == 'pound' and second == 'stone':
                        answer = f'{input} pound = {int(input)*0.0714285714} stone'
                    if first == 'kilogram' and second == 'stone':
                        answer = f'{input} kilogram = {int(input)*0.1574730444} stone'
                    
                    if first == 'stone' and second == 'kilogram':
                        answer = f'{input} stone = {int(input)*6.35029318} kilogram'
                    if first == 'stone' and second == 'pound':
                        answer = f'{input} stone = {int(input)*14} pound'
                context = {
                    'form':form,
                    'm_form':measrurement_form,
                    'input': True,
                    'answer':answer                    
                }
    else:
        form = ConversionForm()
        context ={
            'form':form,
            'input':False
        }
    return render(request,'dashboard/conversion.html',context)

csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Tạo thành công tài khoản {username}')
            return HttpResponseRedirect('/login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }

    return render (request,'dashboard/profile.html',context)

csrf_exempt
def news(request):
        form = DashboardForm(request.POST)
        query_params = {
	    "source": "bbc-news",
	    "sortBy": "top",
	    "apiKey": "c1c3ae80c7b3423395da423f4f9ddfdd"
	    }
        url = 'https://newsapi.org/v1/articles'
        r = requests.get(url,params=query_params)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['articles'][i]['title'],
                'desc':answer['articles'][i]['description'],
                'thumbnail':answer['articles'][i]['urlToImage'],
                'link':answer['articles'][i]['url'],
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }      
        return render(request,'dashboard/news.html',context)