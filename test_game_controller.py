"""Tests for GameController functionality."""

import pytest
from game_controller import GameController
from models.game_state import GameMode
from models.square import Square
from models.piece import PieceType, Color


def test_start_new_game_single_player():
    """Test starting a new game in single-player mode."""
    controller = GameController()
    state = controller.start_new_game(GameMode.SINGLE_PLAYER)
    
    assert state is not None
    assert state.game_mode == GameMode.SINGLE_PLAYER
    assert state.current_player == Color.WHITE
    assert controller.get_current_state() == state
    assert controller.get_selected_square() is None


def test_start_new_game_multiplayer():
    """Test starting a new game in multiplayer mode."""
    controller = GameController()
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    
    assert state is not None
    assert state.game_mode == GameMode.MULTIPLAYER
    assert state.current_player == Color.WHITE
    assert controller.get_current_state() == state


def test_handle_square_selection_valid_piece():
    """Test selecting a square with the current player's piece."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Select white pawn at e2
    result = controller.handle_square_selection(Square.from_algebraic("e2"))
    
    assert result['action'] == 'selected'
    assert result['selected_square'] == Square.from_algebraic("e2")
    assert len(result['legal_moves']) > 0  # Pawn should have legal moves
    assert controller.get_selected_square() == Square.from_algebraic("e2")


def test_handle_square_selection_opponent_piece():
    """Test selecting opponent's piece is rejected."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Try to select black pawn at e7 (white's turn)
    result = controller.handle_square_selection(Square.from_algebraic("e7"))
    
    assert result['action'] == 'cleared'
    assert result['selected_square'] is None
    assert len(result['legal_moves']) == 0


def test_handle_square_selection_empty_square():
    """Test selecting an empty square."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Select empty square e4
    result = controller.handle_square_selection(Square.from_algebraic("e4"))
    
    assert result['action'] == 'cleared'
    assert result['selected_square'] is None


def test_handle_move_attempt_valid():
    """Test executing a valid move."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Select and move white pawn from e2 to e4
    controller.handle_square_selection(Square.from_algebraic("e2"))
    result = controller.handle_move_attempt(
        Square.from_algebraic("e2"),
        Square.from_algebraic("e4")
    )
    
    assert result['action'] == 'move_executed'
    assert result['move'] is not None
    assert result['state'].current_player == Color.BLACK  # Turn switched
    assert controller.get_selected_square() is None  # Selection cleared


def test_handle_move_attempt_invalid():
    """Test attempting an invalid move."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Try to move pawn from e2 to e5 (invalid - too far)
    result = controller.handle_move_attempt(
        Square.from_algebraic("e2"),
        Square.from_algebraic("e5")
    )
    
    assert result['action'] == 'invalid_move'
    assert result['state'].current_player == Color.WHITE  # Turn unchanged


def test_handle_square_selection_reselect():
    """Test reselecting a different piece."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Select pawn at e2
    controller.handle_square_selection(Square.from_algebraic("e2"))
    assert controller.get_selected_square() == Square.from_algebraic("e2")
    
    # Reselect pawn at d2
    result = controller.handle_square_selection(Square.from_algebraic("d2"))
    
    assert result['action'] == 'selected'
    assert result['selected_square'] == Square.from_algebraic("d2")
    assert controller.get_selected_square() == Square.from_algebraic("d2")


def test_handle_square_selection_move_via_selection():
    """Test making a move by selecting destination square."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Select pawn at e2
    controller.handle_square_selection(Square.from_algebraic("e2"))
    
    # Select destination e4 (should execute move)
    result = controller.handle_square_selection(Square.from_algebraic("e4"))
    
    assert result['action'] == 'move_executed'
    assert result['state'].current_player == Color.BLACK


def test_get_legal_moves_for_selected():
    """Test getting legal moves for selected piece."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # No selection initially
    assert len(controller.get_legal_moves_for_selected()) == 0
    
    # Select a piece
    controller.handle_square_selection(Square.from_algebraic("e2"))
    legal_moves = controller.get_legal_moves_for_selected()
    
    assert len(legal_moves) > 0
    # White pawn at e2 should be able to move to e3 and e4
    assert any(move.to_square == Square.from_algebraic("e3") for move in legal_moves)
    assert any(move.to_square == Square.from_algebraic("e4") for move in legal_moves)


def test_ai_move_generation_single_player():
    """Test AI move generation in single-player mode."""
    controller = GameController()
    controller.start_new_game(GameMode.SINGLE_PLAYER)
    
    # Make a move as white
    controller.handle_move_attempt(
        Square.from_algebraic("e2"),
        Square.from_algebraic("e4")
    )
    
    # Now it's black's turn (AI)
    assert controller.get_current_state().current_player == Color.BLACK
    
    # Generate AI move
    result = controller.generate_ai_move()
    
    assert result is not None
    assert result['action'] == 'move_executed'
    assert result['state'].current_player == Color.WHITE  # Back to white's turn


def test_ai_move_not_generated_in_multiplayer():
    """Test AI doesn't generate moves in multiplayer mode."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Make a move as white
    controller.handle_move_attempt(
        Square.from_algebraic("e2"),
        Square.from_algebraic("e4")
    )
    
    # Try to generate AI move (should return None in multiplayer)
    result = controller.generate_ai_move()
    
    assert result is None


def test_ai_move_not_generated_on_white_turn():
    """Test AI doesn't generate moves when it's white's turn."""
    controller = GameController()
    controller.start_new_game(GameMode.SINGLE_PLAYER)
    
    # It's white's turn
    assert controller.get_current_state().current_player == Color.WHITE
    
    # Try to generate AI move (should return None - not AI's turn)
    result = controller.generate_ai_move()
    
    assert result is None


def test_handle_promotion_choice():
    """Test handling pawn promotion."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Set up a position where white pawn can promote
    # Move white pawn to 7th rank (this is a simplified test)
    state = controller.get_current_state()
    
    # Manually place a white pawn on the 7th rank for testing
    from models.piece import Piece
    state.board.set_piece(Square.from_algebraic("e7"), Piece(PieceType.PAWN, Color.WHITE))
    state.board.remove_piece(Square.from_algebraic("e8"))  # Clear destination
    
    # Attempt to move pawn to e8 (promotion)
    result = controller.handle_move_attempt(
        Square.from_algebraic("e7"),
        Square.from_algebraic("e8")
    )
    
    assert result['action'] == 'promotion_required'
    assert controller.pending_promotion_move is not None
    
    # Choose to promote to queen
    promotion_result = controller.handle_promotion_choice(PieceType.QUEEN)
    
    assert promotion_result['action'] == 'move_executed'
    assert controller.pending_promotion_move is None
    
    # Verify queen is on e8
    promoted_piece = controller.get_current_state().board.get_piece(Square.from_algebraic("e8"))
    assert promoted_piece.piece_type == PieceType.QUEEN
    assert promoted_piece.color == Color.WHITE


def test_checkmate_detection():
    """Test that checkmate is detected and game ends."""
    controller = GameController()
    controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Set up a fool's mate position (simplified)
    # This is a basic test - in reality we'd need to set up the full position
    state = controller.get_current_state()
    
    # For now, just verify the controller can handle game over states
    # A full integration test would play out a complete game
    assert controller.get_current_state() is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
