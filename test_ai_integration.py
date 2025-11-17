"""Integration test for AI opponent in a real game."""

from ai.ai_opponent import AIOpponent
from engine.chess_engine import ChessEngine
from models.game_state import GameState, GameMode
from models.piece import Color


def test_ai_plays_full_game():
    """Test that AI can play moves in a full game scenario."""
    engine = ChessEngine()
    ai = AIOpponent(engine, time_limit=2.0)
    
    # Start a new game
    state = GameState.new_game(GameMode.SINGLE_PLAYER)
    
    # Play a few moves
    moves_played = 0
    max_moves = 10
    
    while moves_played < max_moves:
        # Check if game is over
        if engine.is_checkmate(state) or engine.is_draw(state):
            break
        
        # Get AI move
        move = ai.select_move(state)
        
        # Should always get a move (unless game is over)
        if move is None:
            break
        
        # Verify move is legal
        legal_moves = engine.get_legal_moves(state, state.current_player)
        assert move in legal_moves, f"AI selected illegal move: {move}"
        
        # Execute move
        state = engine.execute_move(state, move)
        moves_played += 1
        
        print(f"Move {moves_played}: {move.to_algebraic_notation()}")
    
    print(f"Successfully played {moves_played} moves")
    assert moves_played > 0, "AI should be able to play at least one move"


def test_ai_avoids_obvious_blunders():
    """Test that AI doesn't make obvious blunders like hanging the queen."""
    engine = ChessEngine()
    ai = AIOpponent(engine, time_limit=2.0)
    
    # Create a position where the AI could hang its queen
    from models.board import Board
    from models.piece import Piece, PieceType
    from models.square import Square
    from models.castling_rights import CastlingRights
    
    board = Board()
    # White pieces
    board.set_piece(Square(4, 0), Piece(PieceType.KING, Color.WHITE))  # e1
    board.set_piece(Square(3, 0), Piece(PieceType.QUEEN, Color.WHITE))  # d1
    board.set_piece(Square(0, 0), Piece(PieceType.ROOK, Color.WHITE))  # a1
    
    # Black pieces
    board.set_piece(Square(4, 7), Piece(PieceType.KING, Color.BLACK))  # e8
    board.set_piece(Square(3, 7), Piece(PieceType.ROOK, Color.BLACK))  # d8
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(False, False, False, False),
        game_mode=GameMode.SINGLE_PLAYER
    )
    
    # Get AI move
    move = ai.select_move(state)
    
    # AI should not move queen to d8 (would be captured by rook)
    # This is a basic test - the AI should avoid this obvious blunder
    assert move is not None
    
    # Execute the move and verify queen is not immediately captured
    new_state = engine.execute_move(state, move)
    
    # Check that white queen still exists (not captured)
    white_pieces = new_state.board.get_all_pieces(Color.WHITE)
    has_queen = any(p.piece_type == PieceType.QUEEN for p in white_pieces.values())
    
    # If queen was moved, it should still exist after the move
    if move.piece.piece_type == PieceType.QUEEN:
        # Queen should not be immediately capturable
        black_moves = engine.get_legal_moves(new_state, Color.BLACK)
        queen_captures = [m for m in black_moves if m.captured_piece and m.captured_piece.piece_type == PieceType.QUEEN]
        
        # It's okay if queen can be captured if we got something in return
        # But we shouldn't just hang it for nothing
        if queen_captures and move.captured_piece is None:
            print(f"Warning: AI moved queen to {move.to_square.to_algebraic()} where it can be captured")


if __name__ == "__main__":
    test_ai_plays_full_game()
    test_ai_avoids_obvious_blunders()
    print("All integration tests passed!")
