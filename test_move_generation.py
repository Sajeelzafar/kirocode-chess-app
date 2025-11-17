"""Basic tests for move generation functionality."""

from models.game_state import GameState, GameMode
from models.piece import Color, PieceType, Piece
from models.square import Square
from models.board import Board
from engine.move_generator import MoveGenerator


def test_pawn_initial_moves():
    """Test that pawns can move one or two squares from starting position."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White pawn on e2
    e2_moves = generator.generate_piece_moves(state, Square.from_algebraic('e2'))
    
    # Should have 2 moves: e3 and e4
    assert len(e2_moves) == 2
    destinations = {move.to_square.to_algebraic() for move in e2_moves}
    assert destinations == {'e3', 'e4'}
    print("✓ Pawn initial moves test passed")


def test_knight_moves():
    """Test knight movement from starting position."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White knight on b1
    b1_moves = generator.generate_piece_moves(state, Square.from_algebraic('b1'))
    
    # Should have 2 moves: a3 and c3 (d2 is blocked by pawn)
    assert len(b1_moves) == 2
    destinations = {move.to_square.to_algebraic() for move in b1_moves}
    assert destinations == {'a3', 'c3'}
    print("✓ Knight moves test passed")


def test_bishop_blocked():
    """Test that bishops are blocked by pawns at start."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White bishop on c1 - should have no moves (blocked by pawns)
    c1_moves = generator.generate_piece_moves(state, Square.from_algebraic('c1'))
    assert len(c1_moves) == 0
    print("✓ Bishop blocked test passed")


def test_rook_blocked():
    """Test that rooks are blocked by pawns at start."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White rook on a1 - should have no moves (blocked by pawn)
    a1_moves = generator.generate_piece_moves(state, Square.from_algebraic('a1'))
    assert len(a1_moves) == 0
    print("✓ Rook blocked test passed")


def test_queen_blocked():
    """Test that queen is blocked at start."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White queen on d1 - should have no moves (blocked by pawns)
    d1_moves = generator.generate_piece_moves(state, Square.from_algebraic('d1'))
    assert len(d1_moves) == 0
    print("✓ Queen blocked test passed")


def test_king_initial_moves():
    """Test that king has no moves at start (blocked by pieces)."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    # White king on e1 - should have no moves (blocked by pieces)
    e1_moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    assert len(e1_moves) == 0
    print("✓ King initial moves test passed")


def test_bishop_open_board():
    """Test bishop moves on open board."""
    state = GameState.new_game()
    # Clear the board and place a bishop
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('d4'), Piece(PieceType.BISHOP, Color.WHITE))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('d4'))
    
    # Bishop on d4 should have 13 moves (all diagonal squares it can reach)
    assert len(moves) == 13
    print("✓ Bishop open board test passed")


def test_rook_open_board():
    """Test rook moves on open board."""
    state = GameState.new_game()
    # Clear the board and place a rook
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('d4'), Piece(PieceType.ROOK, Color.WHITE))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('d4'))
    
    # Rook on d4 should have 14 moves (7 horizontal + 7 vertical)
    assert len(moves) == 14
    print("✓ Rook open board test passed")


def test_queen_open_board():
    """Test queen moves on open board."""
    state = GameState.new_game()
    # Clear the board and place a queen
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('d4'), Piece(PieceType.QUEEN, Color.WHITE))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('d4'))
    
    # Queen on d4 should have 27 moves (13 diagonal + 14 orthogonal)
    assert len(moves) == 27
    print("✓ Queen open board test passed")


def test_pawn_capture():
    """Test pawn diagonal captures."""
    state = GameState.new_game()
    # Clear some squares and set up a capture scenario
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('e4'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d5'), Piece(PieceType.PAWN, Color.BLACK))
    state.board.set_piece(Square.from_algebraic('f5'), Piece(PieceType.PAWN, Color.BLACK))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('e4'))
    
    # Should have 3 moves: e5 (forward), d5 (capture), f5 (capture)
    assert len(moves) == 3
    destinations = {move.to_square.to_algebraic() for move in moves}
    assert destinations == {'e5', 'd5', 'f5'}
    
    # Check that captures are marked correctly
    capture_moves = [m for m in moves if m.captured_piece is not None]
    assert len(capture_moves) == 2
    print("✓ Pawn capture test passed")


def test_castling_kingside_white():
    """Test white kingside castling generation."""
    state = GameState.new_game()
    # Clear squares between king and rook
    state.board.remove_piece(Square.from_algebraic('f1'))
    state.board.remove_piece(Square.from_algebraic('g1'))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('e1'))
    
    # Should include castling move to g1
    castling_moves = [m for m in moves if m.is_castling]
    assert len(castling_moves) == 1
    assert castling_moves[0].to_square.to_algebraic() == 'g1'
    print("✓ White kingside castling test passed")


def test_en_passant():
    """Test en passant capture generation."""
    state = GameState.new_game()
    # Set up en passant scenario
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('e5'), Piece(PieceType.PAWN, Color.WHITE))
    state.board.set_piece(Square.from_algebraic('d5'), Piece(PieceType.PAWN, Color.BLACK))
    state.en_passant_target = Square.from_algebraic('d6')
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('e5'))
    
    # Should include en passant capture
    en_passant_moves = [m for m in moves if m.is_en_passant]
    assert len(en_passant_moves) == 1
    assert en_passant_moves[0].to_square.to_algebraic() == 'd6'
    print("✓ En passant test passed")


def test_pawn_promotion():
    """Test pawn promotion move generation."""
    state = GameState.new_game()
    # Place white pawn on 7th rank
    state.board = Board()
    state.board.set_piece(Square.from_algebraic('e7'), Piece(PieceType.PAWN, Color.WHITE))
    
    generator = MoveGenerator()
    moves = generator.generate_piece_moves(state, Square.from_algebraic('e7'))
    
    # Should have 4 moves (one for each promotion piece type)
    assert len(moves) == 4
    promotion_types = {m.promotion_piece for m in moves}
    assert promotion_types == {PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT}
    print("✓ Pawn promotion test passed")


def test_generate_all_moves_initial():
    """Test generating all moves for white at start."""
    state = GameState.new_game()
    generator = MoveGenerator()
    
    moves = generator.generate_pseudo_legal_moves(state, Color.WHITE)
    
    # At start, white has 20 possible moves:
    # 8 pawns × 2 moves each = 16
    # 2 knights × 2 moves each = 4
    assert len(moves) == 20
    print("✓ Generate all initial moves test passed")


if __name__ == '__main__':
    test_pawn_initial_moves()
    test_knight_moves()
    test_bishop_blocked()
    test_rook_blocked()
    test_queen_blocked()
    test_king_initial_moves()
    test_bishop_open_board()
    test_rook_open_board()
    test_queen_open_board()
    test_pawn_capture()
    test_castling_kingside_white()
    test_en_passant()
    test_pawn_promotion()
    test_generate_all_moves_initial()
    
    print("\n✅ All move generation tests passed!")
