import unittest

from bitstring import ConstBitStream

from d7a.system_files.firmware_version import FirmwareVersionFile


class FirmwareVersionFileTest(unittest.TestCase):

  def test_default_constructor(self):
    f = FirmwareVersionFile()
    self.assertEqual(f.application_name, "")
    self.assertEqual(f.git_sha1, "")

  def test_invalid_app_name(self):
    def bad(): FirmwareVersionFile(application_name="toolongname") # can be max 6
    self.assertRaises(ValueError, bad)

  def test_parsing(self):
    file_contents = [
      0x74, 0x68, 0x72, 0x6f, 0x75, 0x67,           # app name: throug(hput_test)
      0x39, 0x61, 0x61, 0x62, 0x66, 0x61, 0x61      # git sha1
     ]

    f = FirmwareVersionFile.parse(ConstBitStream(bytes=file_contents))
    self.assertEqual(f.application_name, "throug")
    self.assertEqual(f.git_sha1, "9aabfaa")

  def test_byte_generation(self):
    expected = [
      0x74, 0x68, 0x72, 0x6f, 0x75, 0x67,           # app name: throug(hput_test)
      0x39, 0x61, 0x61, 0x62, 0x66, 0x61, 0x61      # git sha1
     ]

    bytes = bytearray(FirmwareVersionFile(application_name="throug", git_sha1="9aabfaa"))
    self.assertEqual(len(bytes), 13)
    for i in xrange(len(bytes)):
      self.assertEqual(bytes[i], expected[i])
