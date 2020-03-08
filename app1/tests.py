from django.urls import reverse
from django.test import TestCase
from app1.views import encodeId, decodeCryptedId, gray, mosaic


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
        test_input_pass = 'https://storage.googleapis.com/imageapp_ryopenguin/documents/test.jpg'
        test_output_pass = 'https://storage.googleapis.com/imageapp_ryopenguin/processed/test_processed.jpg'
        self.assertEqual(gray(test_input_pass), test_output_pass)

    def test_error(self):
        pass


class TestMosaic(TestCase):
    def test_mosaiced(self):
        test_input_pass = 'https://storage.googleapis.com/imageapp_ryopenguin/documents/test.jpg'
        test_output_pass = 'https://storage.googleapis.com/imageapp_ryopenguin/processed/test_processed.jpg'
        self.assertEqual(mosaic(test_input_pass), test_output_pass)

    def test_error(self):
        pass


class TestEncodeId(TestCase):
    def test_encode(self):
        # id = 1
        randomized1 = 'MTdmNWRhZTBmNWI3NzJhZGJlOWIyMTJmZDA3YTZiZDNh'
        # id = 100
        randomized100 = 'MTAwN2Y1ZGFlMGY1Yjc3MmFkYmU5YjIxMmZkMDdhNmJkM2E='
        self.assertEqual(encodeId(1), randomized1)
        self.assertEqual(encodeId(100), randomized100)


class TestDecodeCryptedId(TestCase):
    def test_decode(self):
        # id = 1
        randomized1 = 'MTdmNWRhZTBmNWI3NzJhZGJlOWIyMTJmZDA3YTZiZDNh'
        # id = 100
        randomized100 = 'MTAwN2Y1ZGFlMGY1Yjc3MmFkYmU5YjIxMmZkMDdhNmJkM2E='
        self.assertEqual(decodeCryptedId(randomized1), 1)
        self.assertEqual(decodeCryptedId(randomized100), 100)


class TestAbout(TestCase):
    def test_get(self):
        res = self.client.get(reverse('about'))
        self.assertTemplateUsed(res, 'app1/about.html')


class TestExample(TestCase):
    def test_get(self):
        res = self.client.get(reverse('example'))
        self.assertTemplateUsed(res, 'app1/example.html')
