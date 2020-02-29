from django.urls import reverse
from django.test import TestCase


class TestIndex(TestCase):
    def test_get(self):
        res = self.client.get(reverse('index'))
        self.assertTemplateUsed(res, 'app1/index.html')

    def test_post(self):
        pass


class TestProcess(TestCase):
    def test_get(self):
        pass

    def test_post(self):
        pass


class TestGray(TestCase):
    def test_grayed(self):
        pass

    def test_error(self):
        pass
