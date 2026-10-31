import json
import os
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


class HoldoutRegressionTests(unittest.TestCase):
    def test_model_selection_never_receives_holdout_rows(self):
        cells = json.loads((ROOT / "Veri_Madenciligi_Proje.ipynb").read_text(encoding="utf-8"))["cells"]
        namespace = {}
        original = Path.cwd()
        try:
            os.chdir(ROOT)
            for index in (0, 2, 4):
                exec("".join(cells[index]["source"]), namespace)

            calls = []

            def cross_validation(estimator, features, target, **kwargs):
                self.assertTrue(set(features.index).isdisjoint(namespace["X_test_raw"].index))
                self.assertEqual(set(features.index), set(target.index))
                calls.append(len(features))
                return np.ones(5)

            namespace["cross_val_score"] = cross_validation
            exec("".join(cells[5]["source"]), namespace)
            self.assertGreater(len(calls), 0)
        finally:
            os.chdir(original)


if __name__ == "__main__":
    unittest.main()
