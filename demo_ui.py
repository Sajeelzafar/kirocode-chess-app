"""Demonstration of the UI display component."""

from models.game_state import GameState, GameMode
from models.square import Square
from models.piece import Color
from engine.chess_engine import ChessEngine
from ui.display import ChessDisplay


def main():
    """Demonstrate the UI display component."""
    
    # Initialize game and display
    engine = ChessEngine()
    display = ChessDisplay()
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    print("\n" + "=" * 60)
    print("CHESS UI DISPLAY DEMONSTRATION")
    print("=" * 60)
    
    # 1. Display initial board
    print("\n1. Initial Board Position:")
    print(display.render_board(state))
    
    # 2. Display board with selected piece
    print("\n2. Board with Selected Piece (e2 pawn):")
    selected_square = Square.from_algebraic("e2")
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    legal_moves_for_e2 = [m for m in legal_moves if m.from_square == selected_square]
    print(display.render_board(state, selected_square, legal_moves_for_e2))
    
    # 3. Make some moves and show move history
    print("\n3. After a few moves (e4, e5, Nf3, Nc6):")
    
    # e2-e4
    move = [m for m in engine.get_legal_moves(state, Color.WHITE) 
            if m.from_square == Square.from_algebraic("e2") 
            and m.to_square == Square.from_algebraic("e4")][0]
    state = engine.execute_move(state, move)
    
    # e7-e5
    move = [m for m in engine.get_legal_moves(state, Color.BLACK) 
            if m.from_square == Square.from_algebraic("e7") 
            and m.to_square == Square.from_algebraic("e5")][0]
    state = engine.execute_move(state, move)
    
    # Nf3
    move = [m for m in engine.get_legal_moves(state, Color.WHITE) 
            if m.from_square == Square.from_algebraic("g1") 
            and m.to_square == Square.from_algebraic("f3")][0]
    state = engine.execute_move(state, move)
    
    # Nc6
    move = [m for m in engine.get_legal_moves(state, Color.BLACK) 
            if m.from_square == Square.from_algebraic("b8") 
            and m.to_square == Square.from_algebraic("c6")][0]
    state = engine.execute_move(state, move)
    
    print(display.render_board(state))
    
    # 4. Show other UI elements
    print("\n4. Other UI Elements:")
    print(display.render_game_mode_prompt())
    print(display.render_promotion_prompt())
    print(display.render_move_prompt(Color.WHITE))
    print(display.render_error("Invalid move - piece cannot move there"))
    print(display.render_info("Move executed successfully"))
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
