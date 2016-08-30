from lists.models import Item,List
from django.test import TestCase
from django.core.exceptions import ValidationError



class ListAndItemModelTest(TestCase):

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


    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(),'/lists/%d/'%(list_.id,))