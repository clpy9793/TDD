from lists.models import Item,List
from django.test import TestCase
from django.core.exceptions import ValidationError



class ItemModelTest(TestCase):

    def test_display_only_items_for_that_list(self):
        current_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=current_list)
        Item.objects.create(text='itemey 2',list=current_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1',list=other_list)
        Item.objects.create(text='other list item 2',list=other_list)        

        response = self.client.get('/lists/%d/'%(current_list.id,))

        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='',list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(text='i1',list=list1)
        item2 = Item.objects.create(text='i2',list=list1)
        item3 = Item.objects.create(text='i3',list=list1)
        self.assertEqual(
            list(Item.objects.all()),
            [item1,item2,item3]
        )

    def test_string_representation(self):
        item = Item(text='Some text')
        self.assertEqual(str(item),'Some text')

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text,'')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_,text='balabala')
        with self.assertRaises(ValidationError):
            item = Item(list=list_,text='balabala')
            item.full_clean()




class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(),'/lists/%d/'%(list_.id,))






