"""Comprehensive demonstration of all UI display features."""

from models.game_state import GameState, GameMode
from models.square import Square
from models.piece import Color, Piece, PieceType
from engine.chess_engine import ChessEngine
from ui.display import ChessDisplay


def demo_all_features():
    """Demonstrate all UI display features."""
    
    engine = ChessEngine()
    display = ChessDisplay()
    
    print("\n" + "=" * 70)
    print("COMPREHENSIVE UI DISPLAY DEMONSTRATION")
    print("=" * 70)
    
    # Feature 1: Initial board with all pieces
    print("\n" + "=" * 70)
    print("FEATURE 1: Display all pieces with clear white/black distinction")
    print("=" * 70)
    state = GameState.new_game(GameMode.MULTIPLAYER)
    print(display.render_board(state))
    input("\nPress Enter to continue...")
    
    # Feature 2: Current player's turn
    print("\n" + "=" * 70)
    print("FEATURE 2: Display current player's turn")
    print("=" * 70)
    print("Notice the 'Current Turn: WHITE' indicator at the top")
    print(display.render_board(state))
    input("\nPress Enter to continue...")
    
    # Feature 3: Highlight selected piece and legal moves
    print("\n" + "=" * 70)
    print("FEATURE 3: Highlight selected piece and legal move destinations")
    print("=" * 70)
    print("Selected piece shown in [brackets], legal moves shown with *asterisks*")
    selected_square = Square.from_algebraic("e2")
    legal_moves = engine.get_legal_moves(state, Color.WHITE)
    legal_moves_for_e2 = [m for m in legal_moves if m.from_square == selected_square]
    print(display.render_board(state, selected_square, legal_moves_for_e2))
    input("\nPress Enter to continue...")
    
    # Feature 4: Check indicator
    print("\n" + "=" * 70)
    print("FEATURE 4: Display check indicator")
    print("=" * 70)
    print("Creating a position where white is in check...")
    
    # Create a check position: Black rook on e8, White king on e1
    check_state = GameState.new_game(GameMode.MULTIPLAYER)
    check_state.board.grid = [[None for _ in range(8)] for _ in range(8)]
    check_state.board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    check_state.board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.ROOK, Color.BLACK))
    check_state.board.set_piece(Square.from_algebraic("a1"), Piece(PieceType.ROOK, Color.WHITE))
    check_state.board.set_piece(Square.from_algebraic("h8"), Piece(PieceType.KING, Color.BLACK))
    
    print(display.render_board(check_state))
    print("\nNotice the '*** CHECK! ***' indicator")
    input("\nPress Enter to continue...")
    
    # Feature 5: Move history
    print("\n" + "=" * 70)
    print("FEATURE 5: Display move history in algebraic notation")
    print("=" * 70)
    print("Playing the opening moves: 1. e4 e5 2. Nf3 Nc6 3. Bc4")
    
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    # 1. e4
    move = [m for m in engine.get_legal_moves(state, Color.WHITE) 
            if m.from_square == Square.from_algebraic("e2") 
            and m.to_square == Square.from_algebraic("e4")][0]
    state = engine.execute_move(state, move)
    
    # 1... e5
    move = [m for m in engine.get_legal_moves(state, Color.BLACK) 
            if m.from_square == Square.from_algebraic("e7") 
            and m.to_square == Square.from_algebraic("e5")][0]
    state = engine.execute_move(state, move)
    
    # 2. Nf3
    move = [m for m in engine.get_legal_moves(state, Color.WHITE) 
            if m.from_square == Square.from_algebraic("g1") 
            and m.to_square == Square.from_algebraic("f3")][0]
    state = engine.execute_move(state, move)
    
    # 2... Nc6
    move = [m for m in engine.get_legal_moves(state, Color.BLACK) 
            if m.from_square == Square.from_algebraic("b8") 
            and m.to_square == Square.from_algebraic("c6")][0]
    state = engine.execute_move(state, move)
    
    # 3. Bc4
    move = [m for m in engine.get_legal_moves(state, Color.WHITE) 
            if m.from_square == Square.from_algebraic("f1") 
            and m.to_square == Square.from_algebraic("c4")][0]
    state = engine.execute_move(state, move)
    
    print(display.render_board(state))
    print("\nNotice the 'Move History' section showing all moves in order")
    input("\nPress Enter to continue...")
    
    # Feature 6: Game result
    print("\n" + "=" * 70)
    print("FEATURE 6: Display game result (checkmate, stalemate, draw)")
    print("=" * 70)
    print("Simulating a game over state...")
    
    print(display.render_board(state, game_result="Checkmate! White wins!"))
    print("\nNotice the 'GAME OVER' banner with the result")
    input("\nPress Enter to continue...")
    
    # Additional UI elements
    print("\n" + "=" * 70)
    print("ADDITIONAL UI ELEMENTS")
    print("=" * 70)
    
    print("\nGame Mode Selection Prompt:")
    print(display.render_game_mode_prompt())
    
    print("\nPawn Promotion Prompt:")
    print(display.render_promotion_prompt())
    
    print("\nMove Input Prompt:")
    print(display.render_move_prompt(Color.WHITE))
    
    print("\nError Message:")
    print(display.render_error("Invalid move - that square is occupied by your own piece"))
    
    print("\nInfo Message:")
    print(display.render_info("Move executed successfully. It's now Black's turn."))
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nAll UI display features have been demonstrated:")
    print("✓ Display all pieces with clear white/black distinction")
    print("✓ Display current player's turn")
    print("✓ Highlight selected piece and legal move destinations")
    print("✓ Display check indicator when player is in check")
    print("✓ Display move history in algebraic notation")
    print("✓ Display game result (checkmate, stalemate, draw)")
    print("\nRequirements satisfied: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2, 8.3")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demo_all_features()
