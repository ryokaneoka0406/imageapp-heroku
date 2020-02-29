from django.urls import reverse
from django.test import TestCase


class TestIndex(TestCase):
    def test_get(self):
        res = self.client.get(reverse('index'))
        self.assertTemplateUsed(res, 'app1/index.html')
