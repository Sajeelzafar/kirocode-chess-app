"""Tests for move execution in the chess engine."""

import pytest
from models.game_state import GameState, GameMode
from models.board import Board
from models.move import Move
from models.piece import Piece, PieceType, Color
from models.square import Square
from models.castling_rights import CastlingRights
from engine.chess_engine import ChessEngine


def test_execute_normal_move():
    """Test executing a normal piece move."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Move white pawn from e2 to e4
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check piece moved
    assert new_state.board.get_piece(Square.from_algebraic("e2")) is None
    assert new_state.board.get_piece(Square.from_algebraic("e4")) is not None
    assert new_state.board.get_piece(Square.from_algebraic("e4")).piece_type == PieceType.PAWN
    
    # Check turn switched
    assert new_state.current_player == Color.BLACK
    
    # Check move added to history
    assert len(new_state.move_history) == 1
    assert new_state.move_history[0] == move


def test_execute_capture():
    """Test executing a capture move."""
    engine = ChessEngine()
    board = Board()
    
    # Set up a simple position with a capture
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("d5"), Piece(PieceType.PAWN, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        halfmove_clock=5
    )
    
    # White pawn captures black pawn
    move = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("d5"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check capture occurred
    assert new_state.board.get_piece(Square.from_algebraic("e4")) is None
    assert new_state.board.get_piece(Square.from_algebraic("d5")).color == Color.WHITE
    
    # Check halfmove clock reset on capture
    assert new_state.halfmove_clock == 0


def test_execute_pawn_promotion():
    """Test executing a pawn promotion."""
    engine = ChessEngine()
    board = Board()
    
    # White pawn on 7th rank ready to promote
    board.set_piece(Square.from_algebraic("e7"), Piece(PieceType.PAWN, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # Promote to queen
    move = Move(
        from_square=Square.from_algebraic("e7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.QUEEN
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check promotion occurred
    promoted_piece = new_state.board.get_piece(Square.from_algebraic("e8"))
    assert promoted_piece is not None
    assert promoted_piece.piece_type == PieceType.QUEEN
    assert promoted_piece.color == Color.WHITE


def test_execute_castling_kingside():
    """Test executing kingside castling."""
    engine = ChessEngine()
    board = Board()
    
    # Set up position for white kingside castling
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("h1"), Piece(PieceType.ROOK, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(white_kingside=True)
    )
    
    # Castle kingside
    move = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("g1"),
        piece=Piece(PieceType.KING, Color.WHITE),
        is_castling=True
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check king moved
    assert new_state.board.get_piece(Square.from_algebraic("e1")) is None
    assert new_state.board.get_piece(Square.from_algebraic("g1")).piece_type == PieceType.KING
    
    # Check rook moved
    assert new_state.board.get_piece(Square.from_algebraic("h1")) is None
    assert new_state.board.get_piece(Square.from_algebraic("f1")).piece_type == PieceType.ROOK


def test_execute_castling_queenside():
    """Test executing queenside castling."""
    engine = ChessEngine()
    board = Board()
    
    # Set up position for black queenside castling
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.ROOK, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights(black_queenside=True)
    )
    
    # Castle queenside
    move = Move(
        from_square=Square.from_algebraic("e8"),
        to_square=Square.from_algebraic("c8"),
        piece=Piece(PieceType.KING, Color.BLACK),
        is_castling=True
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check king moved
    assert new_state.board.get_piece(Square.from_algebraic("e8")) is None
    assert new_state.board.get_piece(Square.from_algebraic("c8")).piece_type == PieceType.KING
    
    # Check rook moved
    assert new_state.board.get_piece(Square.from_algebraic("a8")) is None
    assert new_state.board.get_piece(Square.from_algebraic("d8")).piece_type == PieceType.ROOK


def test_execute_en_passant():
    """Test executing an en passant capture."""
    engine = ChessEngine()
    board = Board()
    
    # Set up position for en passant
    # White pawn on e5, black pawn on d5 (just moved two squares)
    board.set_piece(Square.from_algebraic("e5"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("d5"), Piece(PieceType.PAWN, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        en_passant_target=Square.from_algebraic("d6")  # En passant available
    )
    
    # Execute en passant capture
    move = Move(
        from_square=Square.from_algebraic("e5"),
        to_square=Square.from_algebraic("d6"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK),
        is_en_passant=True
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check white pawn moved to d6
    assert new_state.board.get_piece(Square.from_algebraic("e5")) is None
    assert new_state.board.get_piece(Square.from_algebraic("d6")).color == Color.WHITE
    
    # Check black pawn on d5 was removed
    assert new_state.board.get_piece(Square.from_algebraic("d5")) is None


def test_castling_rights_revoked_on_king_move():
    """Test that castling rights are revoked when king moves."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(white_kingside=True, white_queenside=True)
    )
    
    # Move king
    move = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("e2"),
        piece=Piece(PieceType.KING, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check both castling rights revoked
    assert new_state.castling_rights.white_kingside is False
    assert new_state.castling_rights.white_queenside is False


def test_castling_rights_revoked_on_rook_move():
    """Test that castling rights are revoked when rook moves."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("h1"), Piece(PieceType.ROOK, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(white_kingside=True, white_queenside=True)
    )
    
    # Move kingside rook
    move = Move(
        from_square=Square.from_algebraic("h1"),
        to_square=Square.from_algebraic("h2"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check only kingside castling revoked
    assert new_state.castling_rights.white_kingside is False
    assert new_state.castling_rights.white_queenside is True


def test_castling_rights_revoked_on_rook_capture():
    """Test that castling rights are revoked when rook is captured."""
    engine = ChessEngine()
    board = Board()
    
    # Black rook on h8, white bishop can capture it
    board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.ROOK, Color.BLACK))
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.BISHOP, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(black_kingside=True, black_queenside=True)
    )
    
    # Capture black rook
    move = Move(
        from_square=Square.from_algebraic("f6"),
        to_square=Square.from_algebraic("h8"),
        piece=Piece(PieceType.BISHOP, Color.WHITE),
        captured_piece=Piece(PieceType.ROOK, Color.BLACK)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check only kingside castling revoked for black
    assert new_state.castling_rights.black_kingside is False
    assert new_state.castling_rights.black_queenside is True


def test_en_passant_target_set_on_two_square_pawn_move():
    """Test that en passant target is set when pawn moves two squares."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Move white pawn two squares
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check en passant target is set to e3
    assert new_state.en_passant_target == Square.from_algebraic("e3")


def test_en_passant_target_cleared_on_other_moves():
    """Test that en passant target is cleared on non-two-square pawn moves."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.KNIGHT, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        en_passant_target=Square.from_algebraic("d6")  # Previous en passant
    )
    
    # Move knight
    move = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("f6"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check en passant target cleared
    assert new_state.en_passant_target is None


def test_halfmove_clock_increments():
    """Test that halfmove clock increments on non-pawn, non-capture moves."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.KNIGHT, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        halfmove_clock=3
    )
    
    # Move knight
    move = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("f6"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check halfmove clock incremented
    assert new_state.halfmove_clock == 4


def test_halfmove_clock_resets_on_pawn_move():
    """Test that halfmove clock resets on pawn moves."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Manually set halfmove clock
    state.halfmove_clock = 10
    
    # Move pawn
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check halfmove clock reset
    assert new_state.halfmove_clock == 0


def test_fullmove_number_increments_after_black_move():
    """Test that fullmove number increments after black's move."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.PAWN, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights(),
        fullmove_number=5
    )
    
    # Black moves
    move = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("e3"),
        piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check fullmove number incremented
    assert new_state.fullmove_number == 6


def test_fullmove_number_unchanged_after_white_move():
    """Test that fullmove number doesn't increment after white's move."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # White moves
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check fullmove number unchanged
    assert new_state.fullmove_number == 1


def test_position_history_updated():
    """Test that position history is updated after move."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    initial_history_length = len(state.position_history)
    
    # Move pawn
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    new_state = engine.execute_move(state, move)
    
    # Check position added to history
    assert len(new_state.position_history) == initial_history_length + 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
