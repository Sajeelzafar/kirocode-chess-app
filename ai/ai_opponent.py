"""AI opponent for single-player chess games."""

import time
from typing import Optional
from models.game_state import GameState
from models.move import Move
from models.piece import PieceType, Color
from engine.chess_engine import ChessEngine


class AIOpponent:
    """
    Computer player that generates moves in single-player mode.
    
    The AI uses material evaluation and basic tactical awareness to select moves.
    It prioritizes checkmate opportunities and avoids losing material.
    
    Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
    """
    
    # Material values for position evaluation (Requirement 5.3)
    PIECE_VALUES = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 0  # King has no material value (can't be captured)
    }
    
    def __init__(self, engine: ChessEngine, time_limit: float = 5.0):
        """
        Initialize the AI opponent.
        
        Args:
            engine: Chess engine for move generation and validation
            time_limit: Maximum time in seconds for move selection
        """
        self.engine = engine
        self.time_limit = time_limit
    
    def select_move(self, state: GameState) -> Optional[Move]:
        """
        Choose the best move for the current position.
        
        Strategy:
        1. Check for checkmate in one move - if found, play it
        2. Evaluate all legal moves
        3. Avoid moves that lose material without compensation
        4. Select the move with the best evaluation
        
        Args:
            state: Current game state
        
        Returns:
            Selected move, or None if no legal moves available
        
        Requirements: 5.1, 5.2, 5.4
        """
        start_time = time.time()
        
        # Get all legal moves (Requirement 5.2)
        legal_moves = self.engine.get_legal_moves(state, state.current_player)
        
        # No legal moves available
        if not legal_moves:
            return None
        
        # Check for checkmate in one move (Requirement 5.5)
        checkmate_move = self.find_checkmate_in_one(state, legal_moves)
        if checkmate_move is not None:
            return checkmate_move
        
        # Check time limit
        if time.time() - start_time > self.time_limit:
            # Return first legal move if time runs out
            return legal_moves[0]
        
        # Evaluate all moves and select the best one
        best_move = None
        best_score = float('-inf')
        
        for move in legal_moves:
            # Check time limit
            if time.time() - start_time > self.time_limit:
                break
            
            # Execute move to get resulting position
            new_state = self.engine.execute_move(state, move)
            
            # Evaluate the position from AI's perspective
            score = self.evaluate_position(new_state)
            
            # Prefer moves that don't lose material (Requirement 5.4)
            # Check if this move loses material without compensation
            if move.captured_piece is None and self._is_hanging(new_state, move.to_square):
                # Penalize moves that leave pieces hanging
                score -= self.PIECE_VALUES[move.piece.piece_type] * 0.9
            
            if score > best_score:
                best_score = score
                best_move = move
        
        # Return best move found, or first legal move if evaluation incomplete
        return best_move if best_move is not None else legal_moves[0]
    
    def evaluate_position(self, state: GameState) -> float:
        """
        Assign a numeric score to a position based on material count.
        
        Positive scores favor the AI (current player), negative scores favor opponent.
        
        Args:
            state: Game state to evaluate
        
        Returns:
            Evaluation score (higher is better for current player)
        
        Requirement 5.3: Consider material value of pieces
        """
        # Get pieces for both colors
        current_pieces = state.board.get_all_pieces(state.current_player)
        opponent_pieces = state.board.get_all_pieces(state.current_player.opposite())
        
        # Calculate material count for current player
        current_material = sum(
            self.PIECE_VALUES[piece.piece_type]
            for piece in current_pieces.values()
        )
        
        # Calculate material count for opponent
        opponent_material = sum(
            self.PIECE_VALUES[piece.piece_type]
            for piece in opponent_pieces.values()
        )
        
        # Return material advantage (positive means AI is ahead)
        return current_material - opponent_material
    
    def find_checkmate_in_one(self, state: GameState, legal_moves: list[Move]) -> Optional[Move]:
        """
        Detect if there's a move that delivers immediate checkmate.
        
        Args:
            state: Current game state
            legal_moves: List of legal moves to check
        
        Returns:
            Move that delivers checkmate, or None if no such move exists
        
        Requirement 5.5: Execute checkmate in one move when available
        """
        for move in legal_moves:
            # Execute the move
            new_state = self.engine.execute_move(state, move)
            
            # Check if this results in checkmate
            if self.engine.is_checkmate(new_state):
                return move
        
        return None
    
    def _is_hanging(self, state: GameState, square) -> bool:
        """
        Check if a piece at a given square is hanging (undefended and attackable).
        
        This is a simple heuristic to avoid leaving pieces undefended.
        
        Args:
            state: Game state after a move
            square: Square to check
        
        Returns:
            True if the piece appears to be hanging
        """
        piece = state.board.get_piece(square)
        if piece is None:
            return False
        
        # Get all legal moves for the opponent
        opponent_moves = self.engine.get_legal_moves(state, state.current_player)
        
        # Check if any opponent move can capture this piece
        for move in opponent_moves:
            if move.to_square == square and move.captured_piece is not None:
                # The piece can be captured
                # Simple heuristic: it's hanging if it can be captured
                return True
        
        return False
