"""Tests for AI opponent functionality."""

import pytest
from ai.ai_opponent import AIOpponent
from engine.chess_engine import ChessEngine
from models.game_state import GameState, GameMode
from models.piece import Color, PieceType, Piece
from models.square import Square
from models.board import Board


def test_ai_selects_legal_move():
    """Test that AI only selects from legal moves."""
    engine = ChessEngine()
    ai = AIOpponent(engine)
    
    # Create a new game
    state = GameState.new_game(GameMode.SINGLE_PLAYER)
    
    # Get AI move
    move = ai.select_move(state)
    
    # Verify move is not None
    assert move is not None
    
    # Verify move is in legal moves
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    assert move in legal_moves


def test_ai_evaluates_material():
    """Test that AI correctly evaluates material."""
    engine = ChessEngine()
    ai = AIOpponent(engine)
    
    # Create a position where white has more material
    board = Board()
    board.set_piece(Square(4, 4), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square(4, 0), Piece(PieceType.KING, Color.BLACK))
    board.set_piece(Square(3, 3), Piece(PieceType.QUEEN, Color.WHITE))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=None,
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    # White should have positive evaluation (queen = 9 points)
    score = ai.evaluate_position(state)
    assert score == 9
    
    # Switch to black's perspective
    state.current_player = Color.BLACK
    score = ai.evaluate_position(state)
    assert score == -9


def test_ai_finds_checkmate_in_one():
    """Test that AI finds checkmate in one move."""
    engine = ChessEngine()
    ai = AIOpponent(engine)
    
    # Set up a position where white can checkmate in one
    # Back rank mate: white queen on d8, black king on e8, black rook on a8
    board = Board()
    board.set_piece(Square(4, 7), Piece(PieceType.KING, Color.BLACK))  # e8
    board.set_piece(Square(5, 6), Piece(PieceType.PAWN, Color.BLACK))  # f7
    board.set_piece(Square(6, 6), Piece(PieceType.PAWN, Color.BLACK))  # g7
    board.set_piece(Square(7, 6), Piece(PieceType.PAWN, Color.BLACK))  # h7
    board.set_piece(Square(3, 6), Piece(PieceType.QUEEN, Color.WHITE))  # d7
    board.set_piece(Square(4, 0), Piece(PieceType.KING, Color.WHITE))  # e1
    
    from models.castling_rights import CastlingRights
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(False, False, False, False),
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    # Get legal moves
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    
    # Find checkmate move
    checkmate_move = ai.find_checkmate_in_one(state, legal_moves)
    
    # Should find the checkmate move (Qd8# or Qe8#)
    if checkmate_move:
        # Verify it's actually checkmate
        new_state = engine.execute_move(state, checkmate_move)
        assert engine.is_checkmate(new_state)


def test_ai_returns_none_when_no_legal_moves():
    """Test that AI returns None when there are no legal moves."""
    engine = ChessEngine()
    ai = AIOpponent(engine)
    
    # Set up a stalemate position
    board = Board()
    board.set_piece(Square(0, 0), Piece(PieceType.KING, Color.BLACK))  # a1
    board.set_piece(Square(1, 2), Piece(PieceType.KING, Color.WHITE))  # b3
    board.set_piece(Square(2, 1), Piece(PieceType.QUEEN, Color.WHITE))  # c2
    
    from models.castling_rights import CastlingRights
    state = GameState(
        board=board,
        current_player=Color.BLACK,
        castling_rights=CastlingRights(False, False, False, False),
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    # AI should return None (no legal moves)
    move = ai.select_move(state)
    assert move is None


def test_ai_material_evaluation_consistency():
    """Test that positions with more material have higher evaluation."""
    engine = ChessEngine()
    ai = AIOpponent(engine)
    
    # Position 1: King only
    board1 = Board()
    board1.set_piece(Square(4, 4), Piece(PieceType.KING, Color.WHITE))
    board1.set_piece(Square(4, 0), Piece(PieceType.KING, Color.BLACK))
    
    from models.castling_rights import CastlingRights
    state1 = GameState(
        board=board1,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(False, False, False, False),
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    # Position 2: King + Rook vs King
    board2 = Board()
    board2.set_piece(Square(4, 4), Piece(PieceType.KING, Color.WHITE))
    board2.set_piece(Square(4, 0), Piece(PieceType.KING, Color.BLACK))
    board2.set_piece(Square(0, 0), Piece(PieceType.ROOK, Color.WHITE))
    
    state2 = GameState(
        board=board2,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(False, False, False, False),
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    score1 = ai.evaluate_position(state1)
    score2 = ai.evaluate_position(state2)
    
    # Position 2 should have higher score (rook = 5 points)
    assert score2 > score1
    assert score2 == score1 + 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
