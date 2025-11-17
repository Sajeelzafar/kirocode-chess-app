"""Tests for game ending detection (checkmate, stalemate, draws)."""

import pytest
from models.game_state import GameState
from models.board import Board
from models.piece import Piece, PieceType, Color
from models.square import Square
from models.castling_rights import CastlingRights
from models.move import Move
from engine.chess_engine import ChessEngine


def test_checkmate_back_rank():
    """Test checkmate detection with back rank mate."""
    engine = ChessEngine()
    board = Board()
    
    # Classic back rank mate: white king on h1, black rook on h1 giving check, white pawns blocking escape
    board.set_piece(Square.from_algebraic("h1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("g2"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("h2"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("a1"), Piece(PieceType.ROOK, Color.BLACK))  # Rook on first rank giving check
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # White is in checkmate
    assert engine.is_checkmate(state)
    assert not engine.is_stalemate(state)


def test_checkmate_queen_and_king():
    """Test checkmate with queen and king vs lone king."""
    engine = ChessEngine()
    board = Board()
    
    # Black king trapped in corner with queen giving check
    board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("g7"), Piece(PieceType.QUEEN, Color.WHITE))  # Queen on g7 gives check
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.KING, Color.WHITE))  # King controls escape squares
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    # Black is in checkmate
    assert engine.is_checkmate(state)


def test_not_checkmate_can_block():
    """Test that it's not checkmate if check can be blocked."""
    engine = ChessEngine()
    board = Board()
    
    # White king in check but can be blocked
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.ROOK, Color.BLACK))
    board.set_piece(Square.from_algebraic("d2"), Piece(PieceType.BISHOP, Color.WHITE))
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # White is in check but not checkmate (bishop can block)
    assert not engine.is_checkmate(state)


def test_not_checkmate_can_capture_attacker():
    """Test that it's not checkmate if the attacking piece can be captured."""
    engine = ChessEngine()
    board = Board()
    
    # White king in check but can capture attacker
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e5"), Piece(PieceType.QUEEN, Color.BLACK))
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # White is in check but not checkmate (king can capture queen)
    assert not engine.is_checkmate(state)


def test_not_checkmate_can_move_king():
    """Test that it's not checkmate if king can move to safety."""
    engine = ChessEngine()
    board = Board()
    
    # White king in check but has escape squares
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.ROOK, Color.BLACK))
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # White is in check but not checkmate (king can move to d3, d4, d5, f3, f4, f5)
    assert not engine.is_checkmate(state)


def test_stalemate_king_only():
    """Test stalemate with lone king having no moves."""
    engine = ChessEngine()
    board = Board()
    
    # Black king trapped but not in check
    board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("f7"), Piece(PieceType.QUEEN, Color.WHITE))
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    # Black is in stalemate
    assert engine.is_stalemate(state)
    assert not engine.is_checkmate(state)


def test_stalemate_with_pawns():
    """Test stalemate where pawns are blocked."""
    engine = ChessEngine()
    board = Board()
    
    # Position where black has only king and pawns, all blocked
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("a7"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("b7"), Piece(PieceType.PAWN, Color.BLACK))
    board.set_piece(Square.from_algebraic("b6"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("c7"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    # Black is in stalemate (king can't move, pawn is blocked)
    assert engine.is_stalemate(state)


def test_not_stalemate_has_legal_moves():
    """Test that it's not stalemate if there are legal moves."""
    engine = ChessEngine()
    board = Board()
    
    # Black king has moves available
    board.set_piece(Square.from_algebraic("e4"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("a1"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    # Black has many legal moves
    assert not engine.is_stalemate(state)


def test_not_stalemate_in_check():
    """Test that it's not stalemate if in check (would be checkmate)."""
    engine = ChessEngine()
    board = Board()
    
    # Black king in check with no moves
    board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("g7"), Piece(PieceType.QUEEN, Color.WHITE))  # Queen gives check
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    # This is checkmate, not stalemate
    assert not engine.is_stalemate(state)
    assert engine.is_checkmate(state)


def test_threefold_repetition():
    """Test threefold repetition detection."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Simulate moves that repeat the position three times
    # Move 1: Nf3
    move1 = Move(
        from_square=Square.from_algebraic("g1"),
        to_square=Square.from_algebraic("f3"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    state = engine.execute_move(state, move1)
    
    # Move 2: Nf6
    move2 = Move(
        from_square=Square.from_algebraic("g8"),
        to_square=Square.from_algebraic("f6"),
        piece=Piece(PieceType.KNIGHT, Color.BLACK)
    )
    state = engine.execute_move(state, move2)
    
    # Move 3: Ng1 (back)
    move3 = Move(
        from_square=Square.from_algebraic("f3"),
        to_square=Square.from_algebraic("g1"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    state = engine.execute_move(state, move3)
    
    # Move 4: Ng8 (back)
    move4 = Move(
        from_square=Square.from_algebraic("f6"),
        to_square=Square.from_algebraic("g8"),
        piece=Piece(PieceType.KNIGHT, Color.BLACK)
    )
    state = engine.execute_move(state, move4)
    
    # Not yet threefold (only 2 occurrences)
    assert not engine.is_threefold_repetition(state)
    
    # Repeat the sequence again
    state = engine.execute_move(state, move1)
    state = engine.execute_move(state, move2)
    state = engine.execute_move(state, move3)
    state = engine.execute_move(state, move4)
    
    # Now should be threefold repetition
    assert engine.is_threefold_repetition(state)


def test_not_threefold_repetition_different_positions():
    """Test that different positions don't trigger threefold repetition."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Make several different moves
    moves = [
        Move(Square.from_algebraic("e2"), Square.from_algebraic("e4"), Piece(PieceType.PAWN, Color.WHITE)),
        Move(Square.from_algebraic("e7"), Square.from_algebraic("e5"), Piece(PieceType.PAWN, Color.BLACK)),
        Move(Square.from_algebraic("g1"), Square.from_algebraic("f3"), Piece(PieceType.KNIGHT, Color.WHITE)),
        Move(Square.from_algebraic("b8"), Square.from_algebraic("c6"), Piece(PieceType.KNIGHT, Color.BLACK)),
    ]
    
    for move in moves:
        state = engine.execute_move(state, move)
    
    # No threefold repetition
    assert not engine.is_threefold_repetition(state)


def test_fifty_move_rule():
    """Test fifty-move rule detection."""
    engine = ChessEngine()
    board = Board()
    
    # Set up a simple position
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        halfmove_clock=100  # 50 full moves
    )
    
    # Should trigger fifty-move rule
    assert engine.is_fifty_move_rule(state)


def test_not_fifty_move_rule():
    """Test that fifty-move rule doesn't trigger prematurely."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Initial position, halfmove clock is 0
    assert not engine.is_fifty_move_rule(state)
    
    # Even with 99 halfmoves (49.5 full moves)
    state.halfmove_clock = 99
    assert not engine.is_fifty_move_rule(state)


def test_insufficient_material_king_vs_king():
    """Test insufficient material: king vs king."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_insufficient_material(state)


def test_insufficient_material_king_bishop_vs_king():
    """Test insufficient material: king + bishop vs king."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("c1"), Piece(PieceType.BISHOP, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_insufficient_material(state)


def test_insufficient_material_king_knight_vs_king():
    """Test insufficient material: king + knight vs king."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.KNIGHT, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_insufficient_material(state)


def test_insufficient_material_bishops_same_color():
    """Test insufficient material: king + bishop vs king + bishop (same color squares)."""
    engine = ChessEngine()
    board = Board()
    
    # Both bishops on light squares (sum of coordinates is even)
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("c1"), Piece(PieceType.BISHOP, Color.WHITE))  # c1: 2+0=2 (even)
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("f8"), Piece(PieceType.BISHOP, Color.BLACK))  # f8: 5+7=12 (even)
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_insufficient_material(state)


def test_sufficient_material_bishops_opposite_color():
    """Test sufficient material: king + bishop vs king + bishop (opposite color squares)."""
    engine = ChessEngine()
    board = Board()
    
    # Bishops on opposite color squares
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("c1"), Piece(PieceType.BISHOP, Color.WHITE))  # c1: 2+0=2 (even/light)
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("c8"), Piece(PieceType.BISHOP, Color.BLACK))  # c8: 2+7=9 (odd/dark)
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # Opposite color bishops can still mate
    assert not engine.is_insufficient_material(state)


def test_sufficient_material_with_pawn():
    """Test sufficient material when there's a pawn."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e2"), Piece(PieceType.PAWN, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # Pawn can promote, so sufficient material
    assert not engine.is_insufficient_material(state)


def test_sufficient_material_with_rook():
    """Test sufficient material with rook."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("a1"), Piece(PieceType.ROOK, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # Rook can checkmate
    assert not engine.is_insufficient_material(state)


def test_sufficient_material_with_queen():
    """Test sufficient material with queen."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("d1"), Piece(PieceType.QUEEN, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    # Queen can checkmate
    assert not engine.is_insufficient_material(state)


def test_is_draw_stalemate():
    """Test that is_draw returns True for stalemate."""
    engine = ChessEngine()
    board = Board()
    
    # Stalemate position
    board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square.from_algebraic("f7"), Piece(PieceType.QUEEN, Color.WHITE))
    board.set_piece(Square.from_algebraic("f6"), Piece(PieceType.KING, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_draw(state)


def test_is_draw_fifty_move_rule():
    """Test that is_draw returns True for fifty-move rule."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(),
        halfmove_clock=100
    )
    
    assert engine.is_draw(state)


def test_is_draw_insufficient_material():
    """Test that is_draw returns True for insufficient material."""
    engine = ChessEngine()
    board = Board()
    
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights()
    )
    
    assert engine.is_draw(state)


def test_not_draw_normal_position():
    """Test that is_draw returns False for normal positions."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    assert not engine.is_draw(state)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
