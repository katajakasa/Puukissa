# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,reverse_lazy
from django.db.models import Sum

from operator import itemgetter
from sandbox import Sandbox, SandboxConfig
from common.responses import JSONResponse
from cStringIO import StringIO
import sys

from puukissa.main.forms import LoginForm, ProfileForm
from puukissa.main.models import Lesson,Hint,HintUsage,Answer

def index(request):
    # Just print out index template. There is nothign else on this page.
    return render_to_response('main/index.html', {}, context_instance=RequestContext(request))

@login_required(login_url=reverse_lazy('main:login'))
def lessons(request):
    # Get lessons, prefoxmat some stuff
    lessons = []
    for lesson in Lesson.objects.all().order_by('number'):
        lesson.formatted_score = lesson.format_answer_score(request.user)
        lesson.formatted_status = lesson.format_status(request.user)
        lesson.status = lesson.get_status(request.user)
        lessons.append(lesson)
    
    # Render the template
    return render_to_response('main/lessons.html', {
        'lessons': lessons,
    }, context_instance=RequestContext(request))

@login_required(login_url=reverse_lazy('main:login'))
def top(request):
    # Get toplist to dict
    tmp = {}
    for a in Answer.objects.filter(status__in=[1,3]):
        if a.user.id in tmp:
            tmp[a.user.id]['score'] += a.get_score()
        else:
            tmp[a.user.id] = {
                'score': a.get_score(),
                'first_name': a.user.first_name,
                'last_name': a.user.last_name,
            }
    
    # Dump stuff to list
    top = []
    for k,v in tmp.items():
        top.append(v)
        
    # Sort by score
    top = sorted(top,key=itemgetter('score'))
    top.reverse()
    
    # Render the template
    return render_to_response('main/top.html', {
        'top': top,
    }, context_instance=RequestContext(request))

@login_required
def json_execute(request):
    # Make sure the request is in POST
    if request.method != "POST":
        raise Http404
    
    # Get vars
    answer_id = request.POST['answer_id']
    result = request.POST['content']
    
    # Find some objects
    answer = get_object_or_404(Answer, id=answer_id)
    
    # Make sure answer belongs to the user
    if answer.user != request.user:
        raise Http404

    # Run answer through sandbox, and capture stdout
    stdout_backup = sys.stdout
    sys.stdout = StringIO()
    sandbox = Sandbox(SandboxConfig('stdout','math'))
    try:
        sandbox.execute(result)
    except Exception, e:
        return JSONResponse({'output': str(e), 'done': 0})
    
    output = sys.stdout.getvalue()
    sys.stdout = stdout_backup
    
    # Save answer text to database, just in case
    answer.result = result
    answer.save()
    
    # Test string
    test = unicode(output.replace("\r", ""), "utf-8")
    expect = answer.lesson.expect.replace("\r","")
    
    # Test result against expected output
    done = 0
    if answer.lesson.type == 0 and test == expect:
        done = 1
    
    # Change linefeeds to html
    output = output.replace("\n","<br />")
    
    # Send stdout and other information to the user
    return JSONResponse({'output': output, 'done': done})

@login_required
def json_turnin(request):
    # Make sure the request is in POST
    if request.method != "POST":
        raise Http404
    
    # Get vars
    answer_id = request.POST['answer_id']
    result = request.POST['content']
    
    # Find some objects
    answer = get_object_or_404(Answer, id=answer_id)
    
    # Make sure answer belongs to the user
    if answer.user != request.user:
        raise Http404
    
    done = 0
    if answer.lesson.type == 0:
        # Run answer through sandbox, and capture stdout
        stdout_backup = sys.stdout
        sys.stdout = StringIO()
        sandbox = Sandbox(SandboxConfig('stdout'))
        sandbox.execute(result)
        output = sys.stdout.getvalue()
        sys.stdout = stdout_backup
        
        # Test string
        test = unicode(output.replace("\r", ""), "utf-8")
        expect = answer.lesson.expect.replace("\r","")
        
        # Test result against expected output
        if answer.lesson.type == 0 and test == expect:
            done = 1
    else:
        done = 1
    
    # Save answer text to database, just in case
    answer.result = result
    if done == 1:
        answer.status = 1
    answer.save()
    
    return JSONResponse({'done': done, 'redirect': reverse('main:lessons')})

@login_required
def json_hint(request):
    # Get objects
    hint = get_object_or_404(Hint, pk=request.POST['hint_id'])
    answer = get_object_or_404(Answer, pk=request.POST['answer_id'])
    
    # Make sure the user is correct
    if answer.user != request.user:
        raise Http404
    
    # Save usage of hint to database
    usage = HintUsage()
    usage.hint = hint
    usage.answer = answer
    usage.save()
    
    # Return response in JSON
    return JSONResponse({'error': 0, 'hint': hint.description})

@login_required(login_url=reverse_lazy('main:login'))
def perform(request, lesson_id):
    # Get lesson object
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    # Get or create Answer
    try:
        answer = Answer.objects.get(user=request.user,lesson=lesson)
    except Answer.DoesNotExist:
        answer = Answer()
        answer.user = request.user
        answer.lesson = lesson
        answer.result = u''
        answer.status = 0
        answer.save()
    
    # Make sure the lesson status is correct
    status = lesson.get_status(request.user)
    if status != 0 and status != 1 and status != 3:
        raise Http404
    
    # Get hints (if any), and see if they have already been used
    hints = []
    for hint in Hint.objects.filter(lesson=lesson).order_by('level'):
        try:
            HintUsage.objects.get(answer=answer,hint=hint)
            hint.is_used = True
        except HintUsage.DoesNotExist:
            hint.is_used = False
        hints.append(hint)
    
    # Render template
    return render_to_response('main/lesson.html', {
        'lesson': lesson,
        'hints': hints,
        'answer': answer,
    }, context_instance=RequestContext(request))
    
@login_required(login_url=reverse_lazy('main:login'))
def profile(request):
    # Handle profile form data
    if request.method == "POST":
        profileform = ProfileForm(request.POST, instance=request.user)
        if profileform.is_valid():
            profileform.save()
            return HttpResponseRedirect(reverse('main:profile'))
    else:
        profileform = ProfileForm(instance=request.user)
    
    # Render the template
    return render_to_response('main/profile.html', {
        'profileform': profileform,
    }, context_instance=RequestContext(request))

def m_login(request):
    loginform = LoginForm(next=reverse('main:index'))

    # Render response
    return render_to_response("main/login.html", {
        'loginform': loginform,
    }, context_instance=RequestContext(request))

def m_logout(request):
    # Do logout and redirect to index page.
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))
