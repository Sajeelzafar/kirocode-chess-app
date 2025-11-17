"""Tests for move validation functionality."""

from models.game_state import GameState
from models.piece import Color, PieceType, Piece
from models.square import Square
from models.board import Board
from models.move import Move
from engine.move_generator import MoveGenerator
from engine.move_validator import MoveValidator


def test_filter_legal_moves_initial():
    """Test filtering legal moves from initial position."""
    state = GameState.new_game()
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate pseudo-legal moves for white
    pseudo_legal = generator.generate_pseudo_legal_moves(state, Color.WHITE)
    
    # Filter to legal moves
    legal = validator.filter_legal_moves(state, pseudo_legal)
    
    # At start, all pseudo-legal moves are legal (no checks)
    assert len(legal) == len(pseudo_legal)
    assert len(legal) == 20  # 16 pawn moves + 4 knight moves
    
    print("✓ Filter legal moves initial test passed")


def test_cannot_move_into_check():
    """Test that moves leaving king in check are rejected."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e1, white rook on e2, black rook on e8
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e2'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate moves for white rook
    rook_moves = generator.generate_piece_moves(state, Square.from_algebraic('e2'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, rook_moves)
    
    # Rook cannot move off the e-file (would expose king to check)
    for move in legal_moves:
        assert move.to_square.file == 4  # e-file
    
    print("✓ Cannot move into check test passed")


def test_must_block_check():
    """Test that when in check, only moves that block/escape are legal."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e1 in check from black rook on e8
    # White rook on d1 can block
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d1'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate all pseudo-legal moves for white
    pseudo_legal = generator.generate_pseudo_legal_moves(state, Color.WHITE)
    
    # Filter to legal moves
    legal = validator.filter_legal_moves(state, pseudo_legal)
    
    # Only moves that escape/block check should be legal
    # King can move to d1, d2, f1, f2
    # Rook can block on e2, e3, e4, e5, e6, e7 or capture on e8
    assert len(legal) > 0  # Should have some legal moves
    
    # Verify all legal moves either move the king or block/capture on e-file
    for move in legal:
        if move.piece.piece_type == PieceType.KING:
            # King moves are ok
            pass
        else:
            # Other pieces must block or capture on e-file
            assert move.to_square.file == 4
    
    print("✓ Must block check test passed")


def test_king_cannot_move_into_check():
    """Test that king cannot move into an attacked square."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e4, black rook on e8
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate king moves
    king_moves = generator.generate_piece_moves(state, Square.from_algebraic('e4'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, king_moves)
    
    # King cannot move to e3, e5 (on the e-file, attacked by rook)
    illegal_squares = {'e3', 'e5'}
    for move in legal_moves:
        assert move.to_square.to_algebraic() not in illegal_squares
    
    print("✓ King cannot move into check test passed")


def test_castling_not_in_check():
    """Test that castling is not allowed when king is in check."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e1, white rook on h1, black rook on e8
    # King is in check from black rook
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('h1'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate king moves (includes castling)
    king_moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, king_moves)
    
    # Castling should not be legal (king in check)
    castling_moves = [m for m in legal_moves if m.is_castling]
    assert len(castling_moves) == 0
    
    print("✓ Castling not in check test passed")


def test_castling_not_through_check():
    """Test that castling is not allowed when king moves through check."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e1, white rook on h1, black rook on f8
    # f1 is attacked by black rook (square king passes through)
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('h1'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('f8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate king moves (includes castling)
    king_moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, king_moves)
    
    # Kingside castling should not be legal (moves through check)
    castling_moves = [m for m in legal_moves if m.is_castling and m.to_square.to_algebraic() == 'g1']
    assert len(castling_moves) == 0
    
    print("✓ Castling not through check test passed")


def test_castling_not_into_check():
    """Test that castling is not allowed when king ends in check."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position: white king on e1, white rook on h1, black rook on g8
    # g1 is attacked by black rook (destination square)
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('h1'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('g8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate king moves (includes castling)
    king_moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, king_moves)
    
    # Kingside castling should not be legal (ends in check)
    castling_moves = [m for m in legal_moves if m.is_castling and m.to_square.to_algebraic() == 'g1']
    assert len(castling_moves) == 0
    
    print("✓ Castling not into check test passed")


def test_castling_legal():
    """Test that castling is legal when all conditions are met."""
    state = GameState.new_game()
    # Clear squares for both castling directions
    state.board.remove_piece(Square.from_algebraic('f1'))
    state.board.remove_piece(Square.from_algebraic('g1'))
    state.board.remove_piece(Square.from_algebraic('d1'))
    state.board.remove_piece(Square.from_algebraic('c1'))
    state.board.remove_piece(Square.from_algebraic('b1'))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate king moves
    king_moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, king_moves)
    
    # Both castling moves should be legal
    castling_moves = [m for m in legal_moves if m.is_castling]
    assert len(castling_moves) == 2
    
    destinations = {m.to_square.to_algebraic() for m in castling_moves}
    assert destinations == {'g1', 'c1'}
    
    print("✓ Castling legal test passed")


def test_en_passant_legal():
    """Test that en passant is legal when conditions are met."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up en passant scenario
    state.board.set_piece(Square.from_algebraic('e5'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d5'), Piece(PieceType.PAWN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.KING, Color.BLACK))
    state.en_passant_target = Square.from_algebraic('d6')
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate pawn moves
    pawn_moves = generator.generate_piece_moves(state, Square.from_algebraic('e5'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, pawn_moves)
    
    # En passant should be legal
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    assert len(en_passant_moves) == 1
    assert en_passant_moves[0].to_square.to_algebraic() == 'd6'
    
    print("✓ En passant legal test passed")


def test_en_passant_would_expose_check():
    """Test that en passant is illegal if it would expose king to check."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up position where en passant would expose king to check
    # White king on e5, white pawn on d5, black pawn on c5, black rook on a5
    state.board.set_piece(Square.from_algebraic('e5'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d5'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('c5'), Piece(PieceType.PAWN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a5'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.KING, Color.BLACK))
    state.en_passant_target = Square.from_algebraic('c6')
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate pawn moves
    pawn_moves = generator.generate_piece_moves(state, Square.from_algebraic('d5'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, pawn_moves)
    
    # En passant should not be legal (would expose king to check from rook)
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    assert len(en_passant_moves) == 0
    
    print("✓ En passant would expose check test passed")


def test_pinned_piece_cannot_move():
    """Test that a pinned piece cannot move off the pin line."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up pin: white king on e1, white bishop on e4, black rook on e8
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.BISHOP, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate bishop moves
    bishop_moves = generator.generate_piece_moves(state, Square.from_algebraic('e4'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, bishop_moves)
    
    # Bishop is pinned and cannot move (bishops move diagonally, pin is vertical)
    assert len(legal_moves) == 0
    
    print("✓ Pinned piece cannot move test passed")


def test_pinned_piece_can_move_along_pin():
    """Test that a pinned piece can move along the pin line."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up pin: white king on e1, white rook on e4, black rook on e8
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate rook moves
    rook_moves = generator.generate_piece_moves(state, Square.from_algebraic('e4'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, rook_moves)
    
    # Rook can move along the e-file (pin line) but not horizontally
    assert len(legal_moves) > 0
    for move in legal_moves:
        assert move.to_square.file == 4  # e-file
    
    print("✓ Pinned piece can move along pin test passed")


def test_promotion_legal():
    """Test that pawn promotion moves are legal."""
    state = GameState.new_game()
    state.board = Board()
    
    # Place white pawn on 7th rank
    state.board.set_piece(Square.from_algebraic('e7'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e1'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate pawn moves
    pawn_moves = generator.generate_piece_moves(state, Square.from_algebraic('e7'))
    
    # Filter to legal moves
    legal_moves = validator.filter_legal_moves(state, pawn_moves)
    
    # All 4 promotion moves should be legal
    assert len(legal_moves) == 4
    promotion_types = {m.promotion_piece for m in legal_moves}
    assert promotion_types == {PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT}
    
    print("✓ Promotion legal test passed")


def test_double_check_only_king_moves():
    """Test that in double check, only king moves are legal."""
    state = GameState.new_game()
    state.board = Board()
    
    # Set up double check: white king on e4, black rook on e8, black bishop on h1
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('e8'), Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('h1'), Piece(PieceType.BISHOP, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('d1'), Piece(PieceType.ROOK, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('a8'), Piece(PieceType.KING, Color.BLACK))
    
    generator = MoveGenerator()
    validator = MoveValidator()
    
    # Generate all white moves
    pseudo_legal = generator.generate_pseudo_legal_moves(state, Color.WHITE)
    
    # Filter to legal moves
    legal = validator.filter_legal_moves(state, pseudo_legal)
    
    # Only king moves should be legal in double check
    for move in legal:
        assert move.piece.piece_type == PieceType.KING
    
    print("✓ Double check only king moves test passed")


if __name__ == '__main__':
    test_filter_legal_moves_initial()
    test_cannot_move_into_check()
    test_must_block_check()
    test_king_cannot_move_into_check()
    test_castling_not_in_check()
    test_castling_not_through_check()
    test_castling_not_into_check()
    test_castling_legal()
    test_en_passant_legal()
    test_en_passant_would_expose_check()
    test_pinned_piece_cannot_move()
    test_pinned_piece_can_move_along_pin()
    test_promotion_legal()
    test_double_check_only_king_moves()
    
    print("\n✅ All move validation tests passed!")
