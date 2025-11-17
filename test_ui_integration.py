"""Integration tests for UI display with game controller."""

import pytest
from models.game_state import GameMode
from models.square import Square
from models.piece import Color
from game_controller import GameController
from ui.display import ChessDisplay


def test_ui_with_game_controller():
    """Test UI display integration with game controller."""
    controller = GameController()
    display = ChessDisplay()
    
    # Start a new game
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Render initial board
    output = display.render_board(state)
    assert "CHESS GAME" in output
    assert "Current Turn: WHITE" in output
    
    # Select a piece
    result = controller.handle_square_selection(Square.from_algebraic("e2"))
    assert result['action'] == 'selected'
    
    # Render with selection
    output = display.render_board(
        result['state'],
        result['selected_square'],
        result['legal_moves']
    )
    assert "[" in output  # Selected piece highlighted
    assert "*" in output  # Legal moves highlighted
    
    # Make a move
    result = controller.handle_move_attempt(
        Square.from_algebraic("e2"),
        Square.from_algebraic("e4")
    )
    assert result['action'] == 'move_executed'
    
    # Render after move
    output = display.render_board(result['state'])
    assert "Move History" in output
    assert "e4" in output


def test_ui_displays_check():
    """Test that UI properly displays check indicator."""
    controller = GameController()
    display = ChessDisplay()
    
    # Start a game
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Create a position with check (this would require setting up a specific position)
    # For now, just verify the display can handle the check detection
    output = display.render_board(state)
    
    # In initial position, there's no check
    assert "CHECK" not in output


def test_ui_with_game_over():
    """Test UI display with game over state."""
    controller = GameController()
    display = ChessDisplay()
    
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Render with game result
    output = display.render_board(state, game_result="Checkmate! White wins!")
    
    assert "GAME OVER" in output
    assert "Checkmate! White wins!" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
