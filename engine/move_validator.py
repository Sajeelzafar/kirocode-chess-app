"""Move validation for chess moves."""

from typing import List
from models.game_state import GameState
from models.move import Move
from models.square import Square
from models.piece import PieceType, Color
from engine.check_detector import CheckDetector


class MoveValidator:
    """
    Validates chess moves according to all rules.
    
    Filters pseudo-legal moves (which follow piece movement patterns) to only
    legal moves (which also don't leave the king in check and satisfy special
    move requirements like castling and en passant).
    """
    
    def __init__(self):
        """Initialize the move validator with a check detector."""
        self.check_detector = CheckDetector()
    
    def filter_legal_moves(self, state: GameState, pseudo_legal_moves: List[Move]) -> List[Move]:
        """
        Filter a list of pseudo-legal moves to only legal moves.
        
        A move is legal if:
        1. It doesn't leave the player's own king in check
        2. If castling, additional requirements are met
        3. If en passant, the move is valid
        
        Args:
            state: Current game state
            pseudo_legal_moves: List of pseudo-legal moves to filter
        
        Returns:
            List of legal moves
        """
        legal_moves = []
        
        for move in pseudo_legal_moves:
            if self.is_legal_move(state, move):
                legal_moves.append(move)
        
        return legal_moves
    
    def is_legal_move(self, state: GameState, move: Move) -> bool:
        """
        Check if a move is legal.
        
        Args:
            state: Current game state
            move: Move to validate
        
        Returns:
            True if the move is legal
        """
        # Special validation for castling
        if move.is_castling:
            return self.validate_castling(state, move)
        
        # Special validation for en passant
        if move.is_en_passant:
            return self.validate_en_passant(state, move)
        
        # General validation: move must not leave king in check
        return not self.would_leave_in_check(state, move)
    
    def would_leave_in_check(self, state: GameState, move: Move) -> bool:
        """
        Check if executing a move would leave the current player's king in check.
        
        Args:
            state: Current game state
            move: Move to check
        
        Returns:
            True if the move would leave the king in check
        """
        # Create a temporary state with the move applied
        temp_state = self._apply_move_temporarily(state, move)
        
        # Check if the current player's king is in check in the new state
        return self.check_detector.is_check(temp_state, move.piece.color)
    
    def validate_castling(self, state: GameState, move: Move) -> bool:
        """
        Validate that a castling move meets all requirements.
        
        Castling requirements:
        1. King and rook haven't moved (checked via castling rights)
        2. No pieces between king and rook (checked in move generation)
        3. King is not currently in check
        4. King doesn't move through check
        5. King doesn't end in check
        
        Args:
            state: Current game state
            move: Castling move to validate
        
        Returns:
            True if castling is legal
        """
        # Requirement 3: King must not be in check
        if self.check_detector.is_check(state, move.piece.color):
            return False
        
        # Requirement 4: King must not move through check
        # Determine which squares the king passes through
        king_file = move.from_square.file
        target_file = move.to_square.file
        rank = move.from_square.rank
        
        # King moves 2 squares, so it passes through one intermediate square
        if target_file > king_file:
            # Kingside castling: king passes through f-file
            intermediate_square = Square(king_file + 1, rank)
        else:
            # Queenside castling: king passes through d-file
            intermediate_square = Square(king_file - 1, rank)
        
        opponent_color = move.piece.color.opposite()
        if self.check_detector.is_square_attacked(state, intermediate_square, opponent_color):
            return False
        
        # Requirement 5: King must not end in check
        # This is checked by applying the move and checking for check
        return not self.would_leave_in_check(state, move)
    
    def validate_en_passant(self, state: GameState, move: Move) -> bool:
        """
        Validate that an en passant capture is legal.
        
        En passant is legal if:
        1. The target square matches the en passant target in the game state
        2. The move doesn't leave the king in check
        
        Args:
            state: Current game state
            move: En passant move to validate
        
        Returns:
            True if en passant is legal
        """
        # Requirement 1: Target must match en passant target
        if state.en_passant_target is None or move.to_square != state.en_passant_target:
            return False
        
        # Requirement 2: Must not leave king in check
        return not self.would_leave_in_check(state, move)
    
    def _apply_move_temporarily(self, state: GameState, move: Move) -> GameState:
        """
        Apply a move to a copy of the game state for validation purposes.
        
        This creates a temporary state to check if a move would leave the king in check.
        It only updates the board position, not other game state fields.
        
        Args:
            state: Current game state
            move: Move to apply
        
        Returns:
            New game state with the move applied
        """
        # Create a copy of the state
        temp_state = state.copy()
        
        # Remove piece from starting square
        temp_state.board.remove_piece(move.from_square)
        
        # Handle en passant capture (remove the captured pawn)
        if move.is_en_passant:
            # The captured pawn is on the same rank as the moving pawn
            captured_pawn_square = Square(move.to_square.file, move.from_square.rank)
            temp_state.board.remove_piece(captured_pawn_square)
        
        # Handle castling (move the rook as well)
        if move.is_castling:
            rank = move.from_square.rank
            if move.to_square.file == 6:  # Kingside
                # Move rook from h-file to f-file
                rook = temp_state.board.get_piece(Square(7, rank))
                temp_state.board.remove_piece(Square(7, rank))
                temp_state.board.set_piece(Square(5, rank), rook)
            else:  # Queenside (file == 2)
                # Move rook from a-file to d-file
                rook = temp_state.board.get_piece(Square(0, rank))
                temp_state.board.remove_piece(Square(0, rank))
                temp_state.board.set_piece(Square(3, rank), rook)
        
        # Place piece at destination square (handle promotion)
        if move.promotion_piece is not None:
            from models.piece import Piece
            promoted_piece = Piece(move.promotion_piece, move.piece.color)
            temp_state.board.set_piece(move.to_square, promoted_piece)
        else:
            temp_state.board.set_piece(move.to_square, move.piece)
        
        return temp_state
