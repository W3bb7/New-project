import unittest

from khaba_core import CognitiveProfile, KhabaCore, KeywordSignalSet, MemoryPattern


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
        self.assertIn("execution_log", decision.trace)
        self.assertEqual(decision.trace["execution_log"][-1].layer, "maestro_interior")
        self.assertGreaterEqual(len(decision.resolved_conflicts), 1)
        self.assertEqual(decision.resolved_conflicts[0].ruling_layer, "maestro_interior")
        self.assertIn("verdad", decision.resolved_conflicts[0].ruling)
        self.assertTrue(any("separar hechos verificables" in step for step in decision.action_plan))

    def test_core_rejects_empty_situations(self) -> None:
        core = KhabaCore()

        with self.assertRaises(ValueError):
            core.process("   ")

    def test_metadata_is_preserved_in_trace(self) -> None:
        core = KhabaCore()
        decision = core.process(
            "Responder a una propuesta comercial con calma.",
            metadata={"domain": "ventas", "actor": "fundador"},
        )

        self.assertEqual(decision.trace["context"].metadata["domain"], "ventas")
        self.assertEqual(decision.trace["context"].metadata["actor"], "fundador")

    def test_custom_profile_changes_memory_bias_without_changing_core(self) -> None:
        profile = CognitiveProfile(
            signals=KeywordSignalSet(
                benefit_words=("inversion",),
                risk_words=("bloqueo",),
                impulse_words=("hoy",),
                truth_risk_words=("falso",),
            ),
            memory_patterns=(
                MemoryPattern(
                    name="fatiga ejecutiva",
                    markers=("sobrecarga",),
                    bias="boundary",
                    weight=0.9,
                    lesson="La sobrecarga exige reducir compromiso.",
                ),
            ),
        )
        core = KhabaCore(profile=profile)

        decision = core.process("Hay sobrecarga, pero quieren cerrar la inversion hoy.")

        self.assertEqual(decision.trace["subconsciente"].bias, "boundary")
        self.assertIn("proteger energia", decision.trace["subconsciente"].modulation)

    def test_trace_exposes_action_plan_and_conflict_resolution(self) -> None:
        core = KhabaCore()
        decision = core.process(
            "Quieren lanzar hoy una oferta urgente para ganar un cliente, "
            "pero hay presion y dudas sobre resultados."
        )

        maestro_trace = decision.trace["maestro_interior"]
        final_log = decision.trace["execution_log"][-1]

        self.assertIn("action_plan", maestro_trace)
        self.assertIn("resolved_conflicts", maestro_trace)
        self.assertEqual(final_log.data["action_plan"], decision.action_plan)
        self.assertEqual(final_log.data["resolved_conflicts"][0]["ruling_layer"], "maestro_interior")


if __name__ == "__main__":
    unittest.main()
