"""Tests for algebraic notation generation."""

import pytest
from models.square import Square
from models.piece import Piece, PieceType, Color
from models.move import Move
from models.board import Board
from models.game_state import GameState
from models.castling_rights import CastlingRights
from engine.chess_engine import ChessEngine


def test_pawn_move():
    """Test basic pawn move notation."""
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    notation = move.to_algebraic_notation()
    assert notation == "e4"


def test_pawn_capture():
    """Test pawn capture notation."""
    move = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("d5"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    notation = move.to_algebraic_notation()
    assert notation == "exd5"


def test_knight_move():
    """Test knight move notation."""
    move = Move(
        from_square=Square.from_algebraic("g1"),
        to_square=Square.from_algebraic("f3"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    notation = move.to_algebraic_notation()
    assert notation == "Nf3"


def test_bishop_capture():
    """Test bishop capture notation."""
    move = Move(
        from_square=Square.from_algebraic("c1"),
        to_square=Square.from_algebraic("f4"),
        piece=Piece(PieceType.BISHOP, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    notation = move.to_algebraic_notation()
    assert notation == "Bxf4"


def test_castling_kingside():
    """Test kingside castling notation."""
    move = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("g1"),
        piece=Piece(PieceType.KING, Color.WHITE),
        is_castling=True
    )
    notation = move.to_algebraic_notation()
    assert notation == "O-O"


def test_castling_queenside():
    """Test queenside castling notation."""
    move = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("c1"),
        piece=Piece(PieceType.KING, Color.WHITE),
        is_castling=True
    )
    notation = move.to_algebraic_notation()
    assert notation == "O-O-O"


def test_pawn_promotion():
    """Test pawn promotion notation."""
    move = Move(
        from_square=Square.from_algebraic("e7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.QUEEN
    )
    notation = move.to_algebraic_notation()
    assert notation == "e8=Q"


def test_pawn_promotion_with_capture():
    """Test pawn promotion with capture notation."""
    move = Move(
        from_square=Square.from_algebraic("d7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.ROOK, Color.BLACK),
        promotion_piece=PieceType.QUEEN
    )
    notation = move.to_algebraic_notation()
    assert notation == "dxe8=Q"


def test_check_notation():
    """Test check notation."""
    move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("h5"),
        piece=Piece(PieceType.QUEEN, Color.WHITE)
    )
    notation = move.to_algebraic_notation(is_check=True)
    assert notation == "Qh5+"


def test_checkmate_notation():
    """Test checkmate notation."""
    move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("h5"),
        piece=Piece(PieceType.QUEEN, Color.WHITE)
    )
    notation = move.to_algebraic_notation(is_checkmate=True)
    assert notation == "Qh5#"


def test_en_passant():
    """Test en passant capture notation."""
    move = Move(
        from_square=Square.from_algebraic("e5"),
        to_square=Square.from_algebraic("d6"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        is_en_passant=True
    )
    notation = move.to_algebraic_notation()
    assert notation == "exd6"


def test_disambiguation_by_file():
    """Test disambiguation using file."""
    move = Move(
        from_square=Square.from_algebraic("a1"),
        to_square=Square.from_algebraic("d1"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    notation = move.to_algebraic_notation(disambiguate_file=True)
    assert notation == "Rad1"


def test_disambiguation_by_rank():
    """Test disambiguation using rank."""
    move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("d4"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    notation = move.to_algebraic_notation(disambiguate_rank=True)
    assert notation == "R1d4"


def test_disambiguation_by_both():
    """Test disambiguation using both file and rank."""
    move = Move(
        from_square=Square.from_algebraic("a1"),
        to_square=Square.from_algebraic("c3"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    notation = move.to_algebraic_notation(disambiguate_file=True, disambiguate_rank=True)
    assert notation == "Na1c3"


def test_engine_algebraic_notation_with_check():
    """Test engine's algebraic notation generation with check detection."""
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Move pawn e2-e4
    move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    
    notation = engine.get_algebraic_notation(state, move)
    assert notation == "e4"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
