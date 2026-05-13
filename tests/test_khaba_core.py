import unittest

from khaba_core import KhabaCore


class KhabaCoreTests(unittest.TestCase):
    def test_master_keeps_final_authority_when_truth_is_at_risk(self) -> None:
        core = KhabaCore()
        decision = core.process(
            "Tenemos presion por dinero y queremos prometer resultados que no podemos demostrar."
        )

        self.assertEqual(decision.authority, "maestro_interior")
        self.assertIn("transparente", decision.final_action)
        self.assertGreaterEqual(len(decision.conflicts), 1)
        self.assertIn("ego", decision.trace)
        self.assertIn("subconsciente", decision.trace)
        self.assertIn("maestro_interior", decision.trace)

    def test_core_rejects_empty_situations(self) -> None:
        core = KhabaCore()

        with self.assertRaises(ValueError):
            core.process("   ")


if __name__ == "__main__":
    unittest.main()
