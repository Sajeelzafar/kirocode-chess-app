"""Tests for check detection functionality."""

from models.game_state import GameState
from models.piece import Color, PieceType, Piece
from models.square import Square
from models.board import Board
from engine.check_detector import CheckDetector


def test_find_king_position():
    """Test finding king positions on the board."""
    state = GameState.new_game()
    detector = CheckDetector()
    
    # Find white king
    white_king_pos = detector.find_king_position(state, Color.WHITE)
    assert white_king_pos is not None
    assert white_king_pos.to_algebraic() == 'e1'
    
    # Find black king
    black_king_pos = detector.find_king_position(state, Color.BLACK)
    assert black_king_pos is not None
    assert black_king_pos.to_algebraic() == 'e8'
    
    print("✓ Find king position test passed")


def test_no_check_initial_position():
    """Test that neither king is in check at the start."""
    state = GameState.new_game()
    detector = CheckDetector()
    
    assert not detector.is_check(state, Color.WHITE)
    assert not detector.is_check(state, Color.BLACK)
    
    print("✓ No check in initial position test passed")


def test_rook_check():
    """Test detection of check by a rook."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e1 and black rook on e8
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check from the rook
    assert detector.is_check(state, Color.WHITE)
    assert not detector.is_check(state, Color.BLACK)
    
    print("✓ Rook check test passed")


def test_bishop_check():
    """Test detection of check by a bishop."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e1 and black bishop on h4
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('h4'), Piece(PieceType.BISHOP, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check from the bishop
    assert detector.is_check(state, Color.WHITE)
    
    print("✓ Bishop check test passed")


def test_queen_check():
    """Test detection of check by a queen."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e4 and black queen on e8
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.QUEEN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a1'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check from the queen
    assert detector.is_check(state, Color.WHITE)
    
    print("✓ Queen check test passed")


def test_knight_check():
    """Test detection of check by a knight."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e4 and black knight on f6
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('f6'), Piece(PieceType.KNIGHT, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check from the knight
    assert detector.is_check(state, Color.WHITE)
    
    print("✓ Knight check test passed")


def test_pawn_check():
    """Test detection of check by a pawn."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e4 and black pawn on d5
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d5'), Piece(PieceType.PAWN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check from the pawn
    assert detector.is_check(state, Color.WHITE)
    
    print("✓ Pawn check test passed")


def test_blocked_check():
    """Test that a piece blocking the attack prevents check."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e1, black rook on e8, and white pawn on e4 (blocking)
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should NOT be in check (blocked by pawn)
    assert not detector.is_check(state, Color.WHITE)
    
    print("✓ Blocked check test passed")


def test_is_square_attacked():
    """Test the is_square_attacked method."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place black rook on e8
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('h8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # e1 should be attacked by the rook
    assert detector.is_square_attacked(state, Square.from_algebraic('e1'), Color.BLACK)
    
    # a1 should not be attacked
    assert not detector.is_square_attacked(state, Square.from_algebraic('a1'), Color.BLACK)
    
    print("✓ Is square attacked test passed")


def test_multiple_attackers():
    """Test check detection with multiple attacking pieces."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e4 with multiple black pieces attacking
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('h4'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should be in check (from either rook)
    assert detector.is_check(state, Color.WHITE)
    
    print("✓ Multiple attackers test passed")


def test_king_adjacent_not_check():
    """Test that adjacent kings don't cause check (illegal position but test the logic)."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place kings adjacent to each other
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e5'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # Each king attacks the other's square
    assert detector.is_square_attacked(state, Square.from_algebraic('e5'), Color.WHITE)
    assert detector.is_square_attacked(state, Square.from_algebraic('e4'), Color.BLACK)
    
    print("✓ King adjacent attack test passed")


def test_pawn_forward_not_attack():
    """Test that pawns don't attack the square directly in front."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white king on e5 and black pawn on e6
    state.board.set_piece(Square.from_algebraic('e5'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e6'), Piece(PieceType.PAWN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    detector = CheckDetector()
    
    # White king should NOT be in check (pawns don't attack forward)
    assert not detector.is_check(state, Color.WHITE)
    
    print("✓ Pawn forward not attack test passed")


if __name__ == '__main__':
    test_find_king_position()
    test_no_check_initial_position()
    test_rook_check()
    test_bishop_check()
    test_queen_check()
    test_knight_check()
    test_pawn_check()
    test_blocked_check()
    test_is_square_attacked()
    test_multiple_attackers()
    test_king_adjacent_not_check()
    test_pawn_forward_not_attack()
    
    print("\n✅ All check detection tests passed!")
