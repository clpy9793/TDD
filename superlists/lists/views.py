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
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'],list=list_)
        return redirect('/lists/%d/'%(list_.id,))
    return render(request,'list.html',{'list':list_})

def new_list(request):
    list_ = List.objects.create()
    item_text = request.POST['item_text']
    item = Item(text=item_text,list=list_)
    error = None
    try:
        item.full_clean()
        item.save()
    except ValidationError as e:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request,'home.html',{'error':error})
    
    return redirect('view_list',list_.id)
