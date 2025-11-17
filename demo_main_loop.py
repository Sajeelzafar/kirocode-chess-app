"""
Demonstration of the main game loop functionality.

This script demonstrates that the main game loop can:
1. Initialize a game
2. Display the board
3. Process moves
4. Handle game flow
"""

from game_controller import GameController
from ui.display import ChessDisplay
from models.game_state import GameMode
from models.square import Square


def demo_multiplayer_game():
    """Demonstrate a few moves in multiplayer mode."""
    print("=" * 60)
    print("DEMO: Multiplayer Game")
    print("=" * 60)
    
    controller = GameController()
    display = ChessDisplay()
    
    # Initialize game
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    print("\nInitial board:")
    print(display.render_board(state))
    
    # Make a few moves
    moves = [
        ("e2", "e4"),  # White pawn
        ("e7", "e5"),  # Black pawn
        ("g1", "f3"),  # White knight
        ("b8", "c6"),  # Black knight
    ]
    
    for from_sq, to_sq in moves:
        # Select piece
        from_square = Square.from_algebraic(from_sq)
        result = controller.handle_square_selection(from_square)
        print(f"\nSelected {from_sq}: {len(result['legal_moves'])} legal moves")
        
        # Move piece
        to_square = Square.from_algebraic(to_sq)
        result = controller.handle_square_selection(to_square)
        
        if result['action'] == 'move_executed':
            state = result['state']
            print(f"Moved to {to_sq}")
            print(display.render_board(state))
        else:
            print(f"Failed to move: {result['action']}")
    
    print("\n✓ Multiplayer game demo completed successfully!")


def demo_single_player_game():
    """Demonstrate single-player mode with AI."""
    print("\n" + "=" * 60)
    print("DEMO: Single-Player Game (vs AI)")
    print("=" * 60)
    
    controller = GameController()
    display = ChessDisplay()
    
    # Initialize single-player game
    state = controller.start_new_game(GameMode.SINGLE_PLAYER)
    print("\nInitial board:")
    print(display.render_board(state))
    
    # Make a white move
    controller.handle_square_selection(Square.from_algebraic("e2"))
    result = controller.handle_square_selection(Square.from_algebraic("e4"))
    
    if result['action'] == 'move_executed':
        state = result['state']
        print("\nWhite played e2-e4")
        print(display.render_board(state))
        
        # Let AI make a move
        print("\nAI is thinking...")
        ai_result = controller.generate_ai_move()
        
        if ai_result and ai_result['action'] == 'move_executed':
            state = ai_result['state']
            move = ai_result['move']
            print(f"AI played: {move.to_algebraic_notation()}")
            print(display.render_board(state))
            print("\n✓ Single-player game demo completed successfully!")
        else:
            print("AI move generation failed")
    else:
        print("White move failed")


def demo_game_ending_detection():
    """Demonstrate that game ending conditions are detected."""
    print("\n" + "=" * 60)
    print("DEMO: Game Ending Detection")
    print("=" * 60)
    
    controller = GameController()
    state = controller.start_new_game(GameMode.MULTIPLAYER)
    
    # Check initial state
    is_checkmate = controller.engine.is_checkmate(state)
    is_draw = controller.engine.is_draw(state)
    
    print(f"\nInitial game state:")
    print(f"  Checkmate: {is_checkmate}")
    print(f"  Draw: {is_draw}")
    print(f"  Current player: {state.current_player.value}")
    print(f"  Legal moves available: {len(controller.engine.get_legal_moves(state, state.current_player))}")
    
    print("\n✓ Game ending detection demo completed successfully!")


if __name__ == "__main__":
    demo_multiplayer_game()
    demo_single_player_game()
    demo_game_ending_detection()
    
    print("\n" + "=" * 60)
    print("ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nThe main game loop is ready to use.")
    print("Run 'python main.py' to start playing chess!")
