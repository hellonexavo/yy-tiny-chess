"""Offline smoke tests for Tiny Chess. No make.fun credentials required."""
import ast
import os
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).with_name("main.py").read_text()
TREE = ast.parse(SOURCE)
FUNCTIONS = [node for node in TREE.body if isinstance(node, ast.FunctionDef) and node.name in ("board_of", "choose")]
NAMESPACE = {}
exec(compile(ast.Module(body=FUNCTIONS, type_ignores=[]), "<tiny-chess-functions>", "exec"), NAMESPACE)

class TinyChessTests(unittest.TestCase):
    def test_opening_returns_legal_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        legal = ["e2e4", "d2d4", "g1f3", "b1c3"]
        self.assertIn(NAMESPACE["choose"](fen, legal), legal)
    def test_black_turn_returns_legal_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        legal = ["e7e5", "c7c5", "g8f6"]
        self.assertIn(NAMESPACE["choose"](fen, legal), legal)
    def test_board_parsing(self):
        self.assertEqual(NAMESPACE["board_of"]("8/8/8/3k4/8/8/8/4K3 w - - 0 1"), {"d5":"k","e1":"K"})
    def test_deterministic_choice(self):
        fen = "8/8/8/3k4/8/8/8/4K3 w - - 0 1"
        legal = ["e1e2", "e1d1", "e1f1"]
        self.assertEqual(NAMESPACE["choose"](fen, legal), NAMESPACE["choose"](fen, legal))

if __name__ == "__main__":
    unittest.main()
