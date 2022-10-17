from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Project, Entry
from .forms import EntryForm#, CommentForm
from .support_functions import \
create_project_tree, get_entry_type_based_on_parent, generate_tree_SVG, add_requirement_to_tree, add_entry_to_tree, replace_project_tree
from .tree_svg import TreeSVG
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


# Create your views here.

@login_required
def home(request):
    projects = Project.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'main_app/home.html',{'projects':projects})

@login_required
def project_list(request):
    projects = Project.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'main_app/project_list.html',{'projects':projects})

@login_required
def project_view(request, pk):
    project=get_object_or_404(Project, pk=pk)
    this_tree_SVG=TreeSVG()
    project_tree_SVG=this_tree_SVG.draw_tree(project.project_tree)
    project_desc=get_object_or_404(Entry, entry_id="R"+str(pk)).short_desc
    return render(request, 'main_app/project_view.html',{'project':project, 'project_tree_SVG':project_tree_SVG, 'project_desc':project_desc}) # in template use: {{ your_context_entry|safe }}

@login_required
def project_new(request):
    if request.method=="POST":
        form=EntryForm(request.POST)
        if form.is_valid():
            project=Project()
            project.author = request.user
            project.save()
            project.project_tree = create_project_tree(project.pk)#creates the XML like text that defines the tree
            project.save()
            entry= form.save(commit=False)
            project.title=entry.title
            project.save()
            entry.author = request.user
            entry.project=project
            entry.entry_type= 'R'
            entry.entry_id= 'R'+str(project.pk)
            entry.save()

            return redirect('project_view', pk=project.pk)
    else:
        form=EntryForm()
        note="note: the project requirement title will be used as the project title"
    return render(request, 'main_app/entry_edit.html', {'form': form, 'entry_id': "Project requirement", 'entry_author': request.user, 'entry_project': 'none', 'note':note})

@login_required
def entry_view(request, pk):
    entry=get_object_or_404(Entry, pk=pk)
    main_entry=False
    if entry.entry_id=='R'+str(entry.project.pk):
        main_entry=True
    return render(request, 'main_app/entry_view.html',{'entry':entry, 'main_entry': main_entry})

@login_required
def show_entry_info(request):
    entry_pk=request.GET.get('entry_pk', None)
    entry=get_object_or_404(Entry, pk=entry_pk)

    data = {
        'entry_pk':entry_pk,
        'entry_id': entry.entry_id,
        'entry_title': entry.title,
        'entry_author': str(entry.author),
        'entry_date':entry.created_date,
        'entry_desc': entry.short_desc,
        'entry_type': entry.entry_type,
        'entry_published_date': entry.published_date,
    }
    return JsonResponse(data)

@login_required
def entry_new(request, pk):#where pk is parent's key
    parent_entry=get_object_or_404(Entry, pk=pk)
    if request.method=="POST":
        form=EntryForm(request.POST)
        #parent_entry=get_object_or_404(Entry, pk=pk)
        if form.is_valid():

            entry= form.save(commit=False)
            entry.author = request.user
            entry.project=parent_entry.project
            this_entry_type=get_entry_type_based_on_parent(parent_entry)
            entry.entry_type= this_entry_type
            entry.entry_id= add_entry_to_tree(pk)# receives parent pk, adds new entry to tree and returns new_entry_id
            entry.save()

            new_parent_number_of_children=parent_entry.number_of_children_entries+1
            parent_entry.number_of_children_entries=new_parent_number_of_children
            parent_entry.save()

            return redirect('project_view', pk=parent_entry.project.pk)

    else:
        form=EntryForm()
    return render(request, 'main_app/entry_edit.html', {'form': form, 'entry_id': "New entry", 'entry_author': request.user, 'entry_project': parent_entry.project.pk})

@login_required
def req_new(request, pk):#where pk is parent's key
    parent_entry=get_object_or_404(Entry, pk=pk)
    if request.method=="POST":
        form=EntryForm(request.POST)
        if form.is_valid():

            entry= form.save(commit=False)
            entry.author = request.user
            entry.project=parent_entry.project
            this_entry_type='R'
            entry.entry_type= this_entry_type
            entry.entry_id= add_requirement_to_tree(pk)# receives parent pk, adds new entry to tree and returns new_entry_id
            entry.save()

            new_parent_number_of_sub_requirements=parent_entry.number_of_sub_requirements+1
            parent_entry.number_of_sub_requirements=new_parent_number_of_sub_requirements
            parent_entry.save()

            return redirect('project_view', pk=parent_entry.project.pk)

    else:
        form=EntryForm()
    return render(request, 'main_app/entry_edit.html', {'form': form, 'entry_id': "New entry", 'entry_author': request.user, 'entry_project': parent_entry.project.pk})


@login_required
def entry_edit(request, pk):
    entry=get_object_or_404(Entry, pk=pk)
    if request.method=="POST":
        form=EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry= form.save(commit=False)
            entry.author = request.user
            #post.published_date=timezone.now()
            entry.save()
            return redirect('entry_view', pk=entry.pk)
    else:
        form=EntryForm(instance=entry)
    return render(request, 'main_app/entry_edit.html', {'form': form, 'entry_id': entry.entry_id, 'entry_author': entry.author, 'entry_project': entry.project.pk, 'note':''})

@login_required
def entry_publish(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    entry.publish()
    return redirect('entry_view', pk=pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'main_app/signup.html', {'form': form})

def learn(request):
    return render(request, 'main_app/learn.html')



#@login_required
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method=="POST":
#         form=CommentForm(request.POST)
#         if form.is_valid():
#             comment= form.save(commit=False)
#             comment.author = request.user
#             comment.post=post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form=CommentForm()
#     return render(request, 'blog2/add_comment_to_post.html', {'form': form})
