from lists.models import Item,List
from lists.forms import ItemForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string



# Create your views here.


def home_page(request):
    return render(request,'home.html',{'form':ItemForm()})

def view_list(request,list_id):
    '同时处理GET和POST请求'
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'],list=list_)
            return redirect('/lists/%d/'%(list_.id,))
    return render(request,'list.html',{'list':list_,'form':form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()

        form.save(for_list=list_)
        return redirect(list_)
    else:        
        return render(request,'home.html',{'form':form})