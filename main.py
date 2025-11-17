#!/usr/bin/env python3
"""
Main entry point for the chess game.

This module implements the main game loop that:
- Prompts user for game mode selection
- Initializes game with selected mode
- Displays board and gets user input
- Processes moves and checks for game end
- Handles AI turns in single-player mode
- Displays final game result

Requirements: 1.1, 1.2, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 4.5
"""

from game_controller import GameController
from ui.display import ChessDisplay
from models.game_state import GameMode
from models.square import Square
from models.piece import PieceType, Color


def get_game_mode() -> GameMode:
    """
    Prompt user to select game mode.
    
    Returns:
        Selected GameMode
    
    Requirements: 1.1, 1.2
    """
    display = ChessDisplay()
    
    while True:
        print(display.render_game_mode_prompt())
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            return GameMode.SINGLE_PLAYER
        elif choice == "2":
            return GameMode.MULTIPLAYER
        else:
            print(display.render_error("Invalid choice. Please enter 1 or 2."))


def parse_square_input(input_str: str) -> Square:
    """
    Parse user input into a Square.
    
    Args:
        input_str: User input (e.g., "e4")
    
    Returns:
        Square object
    
    Raises:
        ValueError: If input is invalid
    """
    input_str = input_str.strip().lower()
    
    if len(input_str) != 2:
        raise ValueError("Input must be exactly 2 characters (e.g., 'e4')")
    
    return Square.from_algebraic(input_str)


def get_promotion_choice() -> PieceType:
    """
    Prompt user to select pawn promotion piece.
    
    Returns:
        Selected PieceType for promotion
    
    Requirement 3.5: Handle pawn promotion
    """
    display = ChessDisplay()
    
    while True:
        print(display.render_promotion_prompt())
        choice = input("Enter your choice (Q/R/B/N): ").strip().upper()
        
        if choice == "Q":
            return PieceType.QUEEN
        elif choice == "R":
            return PieceType.ROOK
        elif choice == "B":
            return PieceType.BISHOP
        elif choice == "N":
            return PieceType.KNIGHT
        else:
            print(display.render_error("Invalid choice. Please enter Q, R, B, or N."))


def main():
    """
    Main game loop.
    
    Implements the complete game flow:
    1. Prompt for game mode
    2. Initialize game
    3. Loop: display board, get input, process move, check for game end
    4. Handle AI turns in single-player mode
    5. Display final result
    
    Requirements: 1.1, 1.2, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 4.5
    """
    controller = GameController()
    display = ChessDisplay()
    
    # Get game mode from user (Requirements 1.1, 1.2)
    mode = get_game_mode()
    
    # Initialize game with selected mode (Requirements 1.1, 1.2)
    state = controller.start_new_game(mode)
    
    print(display.render_info("Game started! Enter squares in algebraic notation (e.g., 'e2', 'e4')"))
    print(display.render_info("Type 'quit' to exit the game."))
    
    game_over = False
    game_result = None
    
    # Main game loop (Requirement 2.1, 2.2)
    while not game_over:
        # Handle AI turn in single-player mode (Requirement 1.1)
        if state.game_mode == GameMode.SINGLE_PLAYER and state.current_player == Color.BLACK:
            print(display.render_info("AI is thinking..."))
            
            result = controller.generate_ai_move()
            
            if result is None:
                print(display.render_error("AI failed to generate a move"))
                break
            
            if result['action'] == 'game_over':
                game_over = True
                game_result = result['result']
                state = result['state']
            elif result['action'] == 'move_executed':
                state = result['state']
                move = result['move']
                print(display.render_info(f"AI played: {move.to_algebraic_notation()}"))
            
            # Display board after AI move
            print(display.render_board(
                state,
                controller.get_selected_square(),
                controller.get_legal_moves_for_selected(),
                game_result
            ))
            
            # Check for game ending conditions after AI move (Requirements 4.1, 4.2, 4.3, 4.4, 4.5)
            if game_over:
                break
            
            continue
        
        # Display current board state (Requirement 2.1)
        print(display.render_board(
            state,
            controller.get_selected_square(),
            controller.get_legal_moves_for_selected(),
            game_result
        ))
        
        # Check if there's a pending promotion
        if controller.pending_promotion_move is not None:
            promotion_piece = get_promotion_choice()
            result = controller.handle_promotion_choice(promotion_piece)
            
            if result['action'] == 'game_over':
                game_over = True
                game_result = result['result']
                state = result['state']
            elif result['action'] == 'move_executed':
                state = result['state']
            
            continue
        
        # Get user input (Requirement 2.1)
        user_input = input(display.render_move_prompt(state.current_player)).strip().lower()
        
        # Check for quit command
        if user_input == 'quit':
            print(display.render_info("Thanks for playing!"))
            break
        
        # Parse square input
        try:
            square = parse_square_input(user_input)
        except ValueError as e:
            print(display.render_error(str(e)))
            continue
        
        # Handle square selection (Requirement 2.1, 2.2)
        result = controller.handle_square_selection(square)
        
        if result['action'] == 'selected':
            # Piece selected, show legal moves
            legal_moves = result['legal_moves']
            print(display.render_info(f"Selected piece at {square.to_algebraic()}. {len(legal_moves)} legal moves available."))
        
        elif result['action'] == 'cleared':
            # Invalid selection
            print(display.render_error("Invalid selection. Please select one of your pieces."))
        
        elif result['action'] == 'invalid_move':
            # Invalid move attempt (Requirement 2.4)
            print(display.render_error("Invalid move. Please try again."))
        
        elif result['action'] == 'move_executed':
            # Move executed successfully (Requirement 2.2)
            state = result['state']
            move = result['move']
            print(display.render_info(f"Move executed: {move.to_algebraic_notation()}"))
        
        elif result['action'] == 'promotion_required':
            # Pawn promotion needed (Requirement 3.5)
            print(display.render_info("Pawn promotion required!"))
        
        elif result['action'] == 'game_over':
            # Game ended (Requirements 4.1, 4.2, 4.3, 4.4, 4.5)
            game_over = True
            game_result = result['result']
            state = result['state']
    
    # Display final board and result (Requirements 4.1, 4.2, 4.3, 4.4, 4.5)
    if game_result:
        print(display.render_board(state, None, None, game_result))
        print(display.render_info("Thanks for playing!"))


if __name__ == "__main__":
    main()
