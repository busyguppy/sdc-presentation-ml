import unittest

from mp3tagger.classes.feature_tool import FeatureTool


class TestFeatureTool(unittest.TestCase):

    def test_feature_vectors(self):
        title = ' band X, 卡式帶樂團 - 某日 ( 某日)'
        ft = FeatureTool()
        fvs = ft.feature_vectors(title)



if __name__ == '__main__':
    unittest.main()