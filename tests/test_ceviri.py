import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from ceviri import (
    _cevirilmez_mi,
    _yer_tutucular_uyumlu,
    _ceviri_gecerli,
    _yer_tutucular_cikar
)
from helpers import bosluklari_koru


class TestCevirilmezMetin(unittest.TestCase):

    def test_url_algilandi(self):
        self.assertTrue(_cevirilmez_mi("https://example.com"))
        self.assertTrue(_cevirilmez_mi("http://test.org"))

    def test_email_algilandi(self):
        self.assertTrue(_cevirilmez_mi("test@example.com"))

    def test_hex_renk_algilandi(self):
        self.assertTrue(_cevirilmez_mi("#FF5733"))
        self.assertTrue(_cevirilmez_mi("#FFF"))

    def test_versiyon_algilandi(self):
        self.assertTrue(_cevirilmez_mi("v2.1.8"))
        self.assertTrue(_cevirilmez_mi("1.0.0"))

    def test_yol_algilandi(self):
        self.assertTrue(_cevirilmez_mi("/usr/local/bin"))
        self.assertTrue(_cevirilmez_mi("C:\\Windows\\System32"))

    def test_normal_metin_cevrilmeli(self):
        self.assertFalse(_cevirilmez_mi("Hello world"))
        self.assertFalse(_cevirilmez_mi("Merhaba dünya"))

    def test_tek_kelime_ui_metni_cevrilmeli(self):
        self.assertFalse(_cevirilmez_mi("Save"))
        self.assertFalse(_cevirilmez_mi("Login"))
        self.assertFalse(_cevirilmez_mi("Submit"))

    def test_teknik_sabitler_cevrilmemeli(self):
        self.assertTrue(_cevirilmez_mi("API_KEY"))
        self.assertTrue(_cevirilmez_mi("USER_ID"))
        self.assertTrue(_cevirilmez_mi("config.yml"))


class TestYerTutucular(unittest.TestCase):

    def test_yer_tutucular_cikar(self):
        metin = "Hello %s, you have %d messages"
        sonuc = _yer_tutucular_cikar(metin)
        self.assertEqual(sonuc, {"%s", "%d"})

    def test_yer_tutucu_uyumlulugu(self):
        self.assertTrue(_yer_tutucular_uyumlu(
            "Hello %s",
            "Merhaba %s"
        ))
        self.assertFalse(_yer_tutucular_uyumlu(
            "Hello %s",
            "Merhaba %d"
        ))
        self.assertFalse(_yer_tutucular_uyumlu(
            "Hello %s",
            "Merhaba"
        ))

    def test_html_etiketleri_korundu(self):
        metin = "Click <b>here</b> to continue"
        yer_tutucular = _yer_tutucular_cikar(metin)
        self.assertIn("<b>", yer_tutucular)
        self.assertIn("</b>", yer_tutucular)


class TestBoslukKoruma(unittest.TestCase):

    def test_bas_ve_son_bosluk_korunur(self):
        kaynak = "  Save changes  "
        hedef = "Değişiklikleri kaydet"
        sonuc = bosluklari_koru(kaynak, hedef)
        self.assertEqual(sonuc, "  Değişiklikleri kaydet  ")

    def test_sadece_bas_bosluk(self):
        kaynak = "   Save"
        hedef = "Kaydet"
        sonuc = bosluklari_koru(kaynak, hedef)
        self.assertEqual(sonuc, "   Kaydet")

    def test_sadece_son_bosluk(self):
        kaynak = "Save   "
        hedef = "Kaydet"
        sonuc = bosluklari_koru(kaynak, hedef)
        self.assertEqual(sonuc, "Kaydet   ")

    def test_bos_hedef_dokunulmaz(self):
        self.assertEqual(bosluklari_koru(" Save ", ""), "")


class TestModelCikti(unittest.TestCase):

    def test_gecerli_cikti(self):
        self.assertTrue(_ceviri_gecerli(
            "Save file",
            "Dosyayı kaydet"
        ))

    def test_bos_cikti_gecersiz(self):
        self.assertFalse(_ceviri_gecerli("Save file", ""))

    def test_ayni_cikti_gecersiz(self):
        self.assertFalse(_ceviri_gecerli("Save", "Save"))
        self.assertFalse(_ceviri_gecerli("Login", "Login"))

    def test_kotu_desenler_algilandi(self):
        self.assertFalse(_ceviri_gecerli(
            "Save",
            "Translation: Kaydet"
        ))
        self.assertFalse(_ceviri_gecerli(
            "Save",
            "Here is the translated text: Kaydet"
        ))


if __name__ == "__main__":
    unittest.main()
