"""
Unit tests for SentencePiece tokenizer.
"""

import unittest

import os
import tempfile

from texar.torch.utils.test import pretrained_test
from texar.torch.data.tokenizers.t5_tokenizer import T5Tokenizer
from texar.torch.data.data_utils import maybe_download


class T5TokenizerTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.SAMPLE_VOCAB = maybe_download(
            'https://github.com/google/sentencepiece/blob/master/'
            'python/test/test_model.model?raw=true', self.tmp_dir.name)

        self.tokenizer = T5Tokenizer.load(self.SAMPLE_VOCAB)

        self.tokenizer.save(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    @pretrained_test
    def test_model_loading(self):
        for pretrained_model_name in T5Tokenizer.available_checkpoints():
            tokenizer = T5Tokenizer(
                pretrained_model_name=pretrained_model_name)

            info = list(os.walk(tokenizer.pretrained_model_dir))
            _, _, files = info[0]

            self.assertIn('sentencepiece.model', files)

            _ = tokenizer.map_text_to_token(u"This is a test")

    def test_roundtrip(self):
        tokenizer = T5Tokenizer.load(self.tmp_dir.name)

        text = 'I saw a girl with a telescope.'
        ids = tokenizer.map_text_to_id(text)
        tokens = tokenizer.map_text_to_token(text)

        self.assertEqual(text, tokenizer.map_id_to_text(ids))
        self.assertEqual(text, tokenizer.map_token_to_text(tokens))

        text = '<extra_id_32> I saw a girl with a telescope.<extra_id_74>'
        ids = tokenizer.map_text_to_id(text)
        tokens = tokenizer.map_text_to_token(text)

        self.assertEqual(text, tokenizer.map_id_to_text(ids))
        self.assertEqual(text, tokenizer.map_token_to_text(tokens))


if __name__ == "__main__":
    unittest.main()
