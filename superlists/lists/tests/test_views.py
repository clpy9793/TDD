from unittest import skip

from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item,List
from lists.forms import ItemForm




# Create your tests here.

EMPTY_LIST_ERROR = "You can't have an empty list item"


class HomePageTest(TestCase):
    '首页测试'
    maxDiff = None
        

    def test_home_page_renders_home_template(self):        
        '确认首页是否使用模板'
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_home_page_user_item_form(self):
        '确认视图是否使用了正确的表单类'
        response = self.client.get('/')        
        self.assertIsInstance(response.context['form'],ItemForm)


    
class NewListTest(TestCase):
    '先建待办清单测试'
    

    def test_saving_a_POST_request(self):
        'POST请求提交的数据能正确存储'
        self.client.post('/lists/new',data={'text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
    
    def test_redirects_after_POST(self):
        '指向/lists/new的请求能重定向到/lists/%d/'

        response = self.client.post('/lists/new',data={'text':'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response,'/lists/%d/'%(new_list.id))

    def test_can_save_a_POST_request_to_an_existing_list(self):
        'post请求提交后 Item与List的关联正确'
        other_lsit = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/'%(correct_list.id,),
            data={'text':'A new item for an existing list'}            
        )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        '指向/lists/xx/的请求回重定向当当前页面'
        other_lsit = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/'%(correct_list.id),
            data={'text':'A new item for an existing list'}            
        )
        self.assertRedirects(response,'/lists/%d/'%(correct_list.id))


    def test_validation_errors_are_sent_back_to_home_page_template(self):
        '提交空事项应返回错误'        
        response = self.client.post('/lists/new',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response,expected_error)
    
    def test_invalid_list_item_arent_saved(self):
        '提交无效的事项 无法通过验证时不保存'
        self.client.post('/lists/new',data={'text':''})
        self.assertEqual(Item.objects.count(),0)
        self.assertEqual(List.objects.count(),0)

    def test_for_invalid_input_renders_home_template(self):
        '测试提交无效表单时返回的页面是否使用了模板'
        response = self.client.post('/lists/new',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        '测试提交无效表单时,返回的页面带有错误提示'
        response = self.client.post('/lists/new',{'text':''})
        self.assertContains(response,escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        '测试提交无效表单时返回的页面中的表单由指定的表单类生成'
        response = self.client.post('/lists/new',{'text':''})
        self.assertIsInstance(response.context['form'],ItemForm)



class ListViewTest(TestCase):
    '待办清单测试'


    def test_for_invalid_input_nothing_saved_to_db(self):
        '测试无效提交  不会保存到数据库'
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    def test_for_invalid_input_renders_list_template(self):
        '测试无效提交是否返回指定的模板和状态码'
        'Code:200'
        'Template:list.htlm'
        response = self.post_invalid_input()
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'list.html')        

    def test_passes_correct_list_to_template(self):
        '测试list页面请求与返回一致'
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/'%correct_list.id)
        self.assertEqual(response.context['list'],correct_list)
     

    def test_saving_and_retrieving_items(self):
        '测试List和Item能正确保存以及正确的关联性'
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.list,list_)


    def test_diplays_item_form(self):
        '测试GET请求返回结果包含指定的表单和name'
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/'%(list_.id,))
        self.assertIsInstance(response.context['form'],ItemForm)
        self.assertContains(response,'name="text"')

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1,text='text')
        response = self.client.post(
            '/lists/%d/'%(list1.id,),
            data={'text':'text'}
        )
        expected_error = escape('You already got this in your list')
        self.assertContains(response,expected_error)
        self.assertTemplateUsed(response,'list.html')
        self.assertEqual(Item.objects.count(),1)


    def post_invalid_input(self):
        '辅助测试 提交无效表单'
        list_ = List.objects.create()
        return self.client.post('/lists/%d/'%(list_.id,),data={'text':''})




