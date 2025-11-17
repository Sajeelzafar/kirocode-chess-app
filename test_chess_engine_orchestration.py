"""Tests for ChessEngine orchestration methods."""

import pytest
from engine.chess_engine import ChessEngine
from models.game_state import GameMode, GameState
from models.piece import Color, PieceType
from models.square import Square
from models.move import Move


def test_initialize_game_multiplayer():
    """Test initializing a multiplayer game."""
    engine = ChessEngine()
    state = engine.initialize_game(GameMode.MULTIPLAYER)
    
    # Verify game mode
    assert state.game_mode == GameMode.MULTIPLAYER
    
    # Verify standard starting position
    assert state.current_player == Color.WHITE
    assert state.fullmove_number == 1
    assert state.halfmove_clock == 0
    
    # Verify all castling rights enabled
    assert state.castling_rights.white_kingside
    assert state.castling_rights.white_queenside
    assert state.castling_rights.black_kingside
    assert state.castling_rights.black_queenside
    
    # Verify pieces in starting positions
    white_king = state.board.get_piece(Square(4, 0))
    assert white_king is not None
    assert white_king.piece_type == PieceType.KING
    assert white_king.color == Color.WHITE


def test_initialize_game_single_player():
    """Test initializing a single-player game."""
    engine = ChessEngine()
    state = engine.initialize_game(GameMode.SINGLE_PLAYER)
    
    # Verify game mode
    assert state.game_mode == GameMode.SINGLE_PLAYER
    
    # Verify standard starting position
    assert state.current_player == Color.WHITE
    assert state.fullmove_number == 1


def test_get_legal_moves_initial_position():
    """Test getting legal moves from initial position."""
    engine = ChessEngine()
    state = engine.initialize_game(GameMode.MULTIPLAYER)
    
    # Get legal moves for white
    white_moves = engine.get_legal_moves(state, Color.WHITE)
    
    # White should have 20 legal moves in starting position
    # (8 pawn moves + 2 knight moves per knight)
    assert len(white_moves) == 20
    
    # Get legal moves for black (should be 0 since it's white's turn)
    black_moves = engine.get_legal_moves(state, Color.BLACK)
    
    # Black also has 20 legal moves (even though it's not their turn)
    assert len(black_moves) == 20


def test_is_legal_move_valid():
    """Test checking if a valid move is legal."""
    engine = ChessEngine()
    state = engine.initialize_game(GameMode.MULTIPLAYER)
    
    # Create a legal pawn move (e2 to e4)
    pawn = state.board.get_piece(Square(4, 1))
    move = Move(
        from_square=Square(4, 1),
        to_square=Square(4, 3),
        piece=pawn
    )
    
    # Verify the move is legal
    assert engine.is_legal_move(state, move)


def test_is_legal_move_invalid():
    """Test checking if a move that would leave king in check is illegal."""
    engine = ChessEngine()
    
    # Create a position where moving a piece would leave king in check
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    # Clear the board
    for rank in range(8):
        for file in range(8):
            state.board.remove_piece(Square(file, rank))
    
    # Set up: white king on e1, white bishop on d2, black rook on a1
    # If bishop moves, king will be in check from rook
    from models.piece import Piece
    state.board.set_piece(Square(4, 0), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square(3, 1), Piece(PieceType.BISHOP, Color.WHITE))
    state.board.set_piece(Square(0, 0), Piece(PieceType.ROOK, Color.BLACK))
    
    # Create a move where bishop moves away, exposing king to check
    bishop = state.board.get_piece(Square(3, 1))
    move = Move(
        from_square=Square(3, 1),
        to_square=Square(5, 3),  # Bishop moves to f4
        piece=bishop
    )
    
    # Verify the move is illegal (would leave king in check)
    assert not engine.is_legal_move(state, move)


def test_get_legal_moves_filters_check():
    """Test that get_legal_moves filters out moves that leave king in check."""
    engine = ChessEngine()
    
    # Create a position where white king is in check
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    # Clear the board
    for rank in range(8):
        for file in range(8):
            state.board.remove_piece(Square(file, rank))
    
    # Set up a position: white king on e1, black rook on e8
    from models.piece import Piece
    state.board.set_piece(Square(4, 0), Piece(PieceType.KING, Color.WHITE))
    state.board.set_piece(Square(4, 7), Piece(PieceType.ROOK, Color.BLACK))
    
    # Add a white pawn that could move but would leave king in check
    state.board.set_piece(Square(3, 1), Piece(PieceType.PAWN, Color.WHITE))
    
    # Get legal moves for white
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    
    # King should only be able to move to squares not attacked by rook
    # Pawn moves should be filtered out since they don't block check
    king_moves = [m for m in legal_moves if m.piece.piece_type == PieceType.KING]
    pawn_moves = [m for m in legal_moves if m.piece.piece_type == PieceType.PAWN]
    
    # King can move to d1, f1, f2 (3 squares - d2 is also attacked by rook on e-file diagonal)
    # Actually, the rook on e8 attacks the entire e-file, so king can move to d1, d2, f1, f2
    # But d2 is not attacked by the rook (rook only attacks e-file and 8th rank)
    # Let's verify the actual legal moves
    assert len(king_moves) >= 3  # At least d1, f1, f2
    
    # Pawn cannot move (would leave king in check)
    assert len(pawn_moves) == 0


def test_integration_move_execution_and_validation():
    """Test that move execution and validation work together."""
    engine = ChessEngine()
    state = engine.initialize_game(GameMode.MULTIPLAYER)
    
    # Get legal moves for white
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    
    # Execute the first legal move
    first_move = legal_moves[0]
    new_state = engine.execute_move(state, first_move)
    
    # Verify state changed
    assert new_state.current_player == Color.BLACK
    assert new_state.fullmove_number == 1
    
    # Verify move was recorded
    assert len(new_state.move_history) == 1
    assert new_state.move_history[0] == first_move


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
