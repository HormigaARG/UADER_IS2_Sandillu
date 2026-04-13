import unittest
from rpn import eval_rpn, RPNError
import math

class TestRPN(unittest.TestCase):

    # --- Básicos ---
    def test_basicos(self):
        self.assertEqual(eval_rpn("3 4 +"), 7)
        self.assertEqual(eval_rpn("5 1 2 + 4 * + 3 -"), 14)
        self.assertEqual(eval_rpn("2 3 4 * +"), 14)

    # --- Floats y negativos ---
    def test_floats(self):
        self.assertAlmostEqual(eval_rpn("2.5 2 *"), 5.0)
        self.assertEqual(eval_rpn("-3 -2 *"), 6)

    # --- Operaciones ---
    def test_division_cero(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 0 /")

    # --- Funciones matemáticas ---
    def test_funciones(self):
        self.assertEqual(eval_rpn("9 sqrt"), 3)
        self.assertEqual(eval_rpn("100 log"), 2)
        self.assertAlmostEqual(eval_rpn("1 ln"), 0)
        self.assertAlmostEqual(eval_rpn("1 ex"), math.e)
        self.assertEqual(eval_rpn("2 10x"), 100)
        self.assertEqual(eval_rpn("2 3 yx"), 8)

    def test_errores_matematicos(self):
        with self.assertRaises(RPNError):
            eval_rpn("-1 sqrt")
        with self.assertRaises(RPNError):
            eval_rpn("-1 log")
        with self.assertRaises(RPNError):
            eval_rpn("-1 ln")

    # --- Inversa ---
    def test_inversa(self):
        self.assertEqual(eval_rpn("2 1/x"), 0.5)
        with self.assertRaises(RPNError):
            eval_rpn("0 1/x")

    # --- Trigonometría ---
    def test_trig(self):
        self.assertAlmostEqual(eval_rpn("90 sin"), 1)
        self.assertAlmostEqual(eval_rpn("0 cos"), 1)
        self.assertAlmostEqual(eval_rpn("1 asin"), 90)

    def test_trig_error(self):
        with self.assertRaises(RPNError):
            eval_rpn("2 asin")  # fuera de dominio

    # --- Constantes ---
    def test_constantes(self):
        self.assertAlmostEqual(eval_rpn("p"), math.pi)
        self.assertAlmostEqual(eval_rpn("e"), math.e)
        self.assertAlmostEqual(eval_rpn("j"), (1 + 5**0.5)/2)

    # --- Pila ---
    def test_pila(self):
        self.assertEqual(eval_rpn("3 dup *"), 9)
        self.assertEqual(eval_rpn("3 4 swap -"), 1)
        self.assertEqual(eval_rpn("3 4 drop"), 3)

    def test_clear(self):
        self.assertEqual(eval_rpn("3 4 clear 5"), 5)

    # --- Memoria ---
    def test_memoria(self):
        self.assertEqual(eval_rpn("5 sto 0 rcl 0"), 5)

    def test_memoria_error(self):
        with self.assertRaises(RPNError):
            eval_rpn("5 sto 10")
        with self.assertRaises(RPNError):
            eval_rpn("5 sto")

    # --- Errores generales ---
    def test_token_invalido(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 4 foo")

    def test_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            eval_rpn("+")

    def test_pila_final(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 4")


if __name__ == "__main__":
    unittest.main()