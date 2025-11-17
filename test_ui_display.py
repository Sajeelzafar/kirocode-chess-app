"""Tests for UI display component."""

import pytest
from models.game_state import GameState, GameMode
from models.square import Square
from models.piece import Color, PieceType
from ui.display import ChessDisplay, render_board
from engine.chess_engine import ChessEngine


def test_render_board_initial_position():
    """Test rendering the board in initial position."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    display = ChessDisplay()
    
    output = display.render_board(state)
    
    # Check that output contains expected elements
    assert "CHESS GAME" in output
    assert "Current Turn: WHITE" in output
    assert "a  b  c  d  e  f  g  h" in output  # File labels
    
    # Check that pieces are displayed (using Unicode symbols)
    assert "♔" in output or "♚" in output  # Kings
    assert "♙" in output or "♟" in output  # Pawns


def test_render_board_with_selected_square():
    """Test rendering with a selected square highlighted."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    display = ChessDisplay()
    engine = ChessEngine()
    
    # Select e2 pawn
    selected_square = Square.from_algebraic("e2")
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    legal_moves_for_e2 = [m for m in legal_moves if m.from_square == selected_square]
    
    output = display.render_board(state, selected_square, legal_moves_for_e2)
    
    # Check that selected square is highlighted with brackets
    assert "[" in output and "]" in output
    
    # Check that legal move destinations are highlighted with asterisks
    assert "*" in output


def test_render_board_with_check():
    """Test rendering when a player is in check."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    display = ChessDisplay()
    
    # Create a position where white is in check
    # Clear the board and set up a simple check position
    state.board.grid = [[None for _ in range(8)] for _ in range(8)]
    
    # White king on e1
    state.board.set_piece(Square.from_algebraic("e1"), 
                          state.board.get_piece(Square(4, 0)) or 
                          type('obj', (object,), {'piece_type': PieceType.KING, 'color': Color.WHITE})())
    
    # Black rook on e8 (checking the king)
    from models.piece import Piece
    state.board.set_piece(Square.from_algebraic("e8"), 
                          Piece(PieceType.ROOK, Color.BLACK))
    state.board.set_piece(Square.from_algebraic("e1"), 
                          Piece(PieceType.KING, Color.WHITE))
    
    output = display.render_board(state)
    
    # Check that check indicator is displayed
    assert "CHECK" in output


def test_render_board_with_move_history():
    """Test rendering with move history."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    engine = ChessEngine()
    
    # Make a few moves
    # e2-e4
    move1 = [m for m in engine.get_legal_moves(state, Color.WHITE) 
             if m.from_square == Square.from_algebraic("e2") 
             and m.to_square == Square.from_algebraic("e4")][0]
    state = engine.execute_move(state, move1)
    
    # e7-e5
    move2 = [m for m in engine.get_legal_moves(state, Color.BLACK) 
             if m.from_square == Square.from_algebraic("e7") 
             and m.to_square == Square.from_algebraic("e5")][0]
    state = engine.execute_move(state, move2)
    
    display = ChessDisplay()
    output = display.render_board(state)
    
    # Check that move history is displayed
    assert "Move History" in output
    assert "e4" in output
    assert "e5" in output


def test_render_board_with_game_result():
    """Test rendering with game result."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    display = ChessDisplay()
    
    output = display.render_board(state, game_result="Checkmate! White wins!")
    
    # Check that game result is displayed
    assert "GAME OVER" in output
    assert "Checkmate! White wins!" in output


def test_render_promotion_prompt():
    """Test rendering promotion prompt."""
    display = ChessDisplay()
    output = display.render_promotion_prompt()
    
    assert "PAWN PROMOTION" in output
    assert "Queen" in output
    assert "Rook" in output
    assert "Bishop" in output
    assert "Knight" in output


def test_render_game_mode_prompt():
    """Test rendering game mode prompt."""
    display = ChessDisplay()
    output = display.render_game_mode_prompt()
    
    assert "MODE SELECTION" in output
    assert "Single Player" in output
    assert "Multiplayer" in output


def test_render_move_prompt():
    """Test rendering move prompt."""
    display = ChessDisplay()
    output = display.render_move_prompt(Color.WHITE)
    
    assert "WHITE" in output
    assert "move" in output.lower()


def test_render_error():
    """Test rendering error message."""
    display = ChessDisplay()
    output = display.render_error("Invalid move")
    
    assert "ERROR" in output
    assert "Invalid move" in output


def test_render_info():
    """Test rendering info message."""
    display = ChessDisplay()
    output = display.render_info("Move executed successfully")
    
    assert "Move executed successfully" in output


def test_convenience_render_board_function():
    """Test the convenience render_board function."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    output = render_board(state)
    
    assert "CHESS GAME" in output
    assert "Current Turn: WHITE" in output


def test_piece_symbols_white_and_black_distinction():
    """Test that white and black pieces are clearly distinguished."""
    state = GameState.new_game(GameMode.MULTIPLAYER)
    display = ChessDisplay()
    
    output = display.render_board(state)
    
    # Check that both white and black piece symbols are present
    # White pieces (filled symbols)
    assert "♔" in output or "♕" in output or "♖" in output
    
    # Black pieces (outlined symbols)
    assert "♚" in output or "♛" in output or "♜" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
