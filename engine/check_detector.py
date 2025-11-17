"""Check detection for chess positions."""

from typing import Optional
from models.game_state import GameState
from models.square import Square
from models.piece import Piece, PieceType, Color


class CheckDetector:
    """
    Detects check conditions in chess positions.
    
    Provides methods to:
    - Find king positions
    - Determine if a square is under attack
    - Detect if a king is in check
    """
    
    def find_king_position(self, state: GameState, color: Color) -> Optional[Square]:
        """
        Find the position of the king for a given color.
        
        Args:
            state: Current game state
            color: Color of the king to find
        
        Returns:
            Square where the king is located, or None if not found
        """
        for rank in range(8):
            for file in range(8):
                square = Square(file, rank)
                piece = state.board.get_piece(square)
                if piece is not None and piece.piece_type == PieceType.KING and piece.color == color:
                    return square
        return None
    
    def is_square_attacked(self, state: GameState, square: Square, by_color: Color) -> bool:
        """
        Determine if a square is under attack by a given color.
        
        A square is under attack if any piece of the attacking color can move to it
        (following piece movement rules, ignoring whether the move would leave the
        attacking side's king in check).
        
        Args:
            state: Current game state
            square: Square to check
            by_color: Color of the attacking side
        
        Returns:
            True if the square is under attack by the given color
        """
        # Check all pieces of the attacking color
        pieces = state.board.get_all_pieces(by_color)
        
        for piece_square, piece in pieces.items():
            if self._can_piece_attack_square(state, piece_square, piece, square):
                return True
        
        return False
    
    def _can_piece_attack_square(
        self,
        state: GameState,
        from_square: Square,
        piece: Piece,
        target_square: Square
    ) -> bool:
        """
        Check if a piece can attack a specific square.
        
        Args:
            state: Current game state
            from_square: Square where the attacking piece is located
            piece: The attacking piece
            target_square: Square to check if it can be attacked
        
        Returns:
            True if the piece can attack the target square
        """
        if piece.piece_type == PieceType.PAWN:
            return self._can_pawn_attack(from_square, piece, target_square)
        elif piece.piece_type == PieceType.KNIGHT:
            return self._can_knight_attack(from_square, target_square)
        elif piece.piece_type == PieceType.BISHOP:
            return self._can_bishop_attack(state, from_square, target_square)
        elif piece.piece_type == PieceType.ROOK:
            return self._can_rook_attack(state, from_square, target_square)
        elif piece.piece_type == PieceType.QUEEN:
            return self._can_queen_attack(state, from_square, target_square)
        elif piece.piece_type == PieceType.KING:
            return self._can_king_attack(from_square, target_square)
        
        return False
    
    def _can_pawn_attack(self, from_square: Square, piece: Piece, target_square: Square) -> bool:
        """
        Check if a pawn can attack a target square.
        
        Pawns attack diagonally forward one square.
        """
        direction = 1 if piece.color == Color.WHITE else -1
        
        # Check if target is one rank forward and one file to the side
        rank_diff = target_square.rank - from_square.rank
        file_diff = abs(target_square.file - from_square.file)
        
        return rank_diff == direction and file_diff == 1
    
    def _can_knight_attack(self, from_square: Square, target_square: Square) -> bool:
        """
        Check if a knight can attack a target square.
        
        Knights move in an L-shape: 2 squares in one direction, 1 square perpendicular.
        """
        file_diff = abs(target_square.file - from_square.file)
        rank_diff = abs(target_square.rank - from_square.rank)
        
        return (file_diff == 2 and rank_diff == 1) or (file_diff == 1 and rank_diff == 2)
    
    def _can_bishop_attack(self, state: GameState, from_square: Square, target_square: Square) -> bool:
        """
        Check if a bishop can attack a target square.
        
        Bishops move diagonally, and the path must be clear.
        """
        file_diff = target_square.file - from_square.file
        rank_diff = target_square.rank - from_square.rank
        
        # Must be on a diagonal
        if abs(file_diff) != abs(rank_diff) or file_diff == 0:
            return False
        
        # Check if path is clear
        return self._is_path_clear(state, from_square, target_square)
    
    def _can_rook_attack(self, state: GameState, from_square: Square, target_square: Square) -> bool:
        """
        Check if a rook can attack a target square.
        
        Rooks move horizontally or vertically, and the path must be clear.
        """
        file_diff = target_square.file - from_square.file
        rank_diff = target_square.rank - from_square.rank
        
        # Must be on same file or same rank (but not both)
        if not ((file_diff == 0 and rank_diff != 0) or (file_diff != 0 and rank_diff == 0)):
            return False
        
        # Check if path is clear
        return self._is_path_clear(state, from_square, target_square)
    
    def _can_queen_attack(self, state: GameState, from_square: Square, target_square: Square) -> bool:
        """
        Check if a queen can attack a target square.
        
        Queens move like both bishops and rooks.
        """
        return (self._can_bishop_attack(state, from_square, target_square) or
                self._can_rook_attack(state, from_square, target_square))
    
    def _can_king_attack(self, from_square: Square, target_square: Square) -> bool:
        """
        Check if a king can attack a target square.
        
        Kings move one square in any direction.
        """
        file_diff = abs(target_square.file - from_square.file)
        rank_diff = abs(target_square.rank - from_square.rank)
        
        return file_diff <= 1 and rank_diff <= 1 and (file_diff != 0 or rank_diff != 0)
    
    def _is_path_clear(self, state: GameState, from_square: Square, to_square: Square) -> bool:
        """
        Check if the path between two squares is clear (no pieces in between).
        
        Args:
            state: Current game state
            from_square: Starting square
            to_square: Ending square
        
        Returns:
            True if all squares between from_square and to_square are empty
        """
        file_diff = to_square.file - from_square.file
        rank_diff = to_square.rank - from_square.rank
        
        # Determine direction
        file_step = 0 if file_diff == 0 else (1 if file_diff > 0 else -1)
        rank_step = 0 if rank_diff == 0 else (1 if rank_diff > 0 else -1)
        
        # Check each square along the path (excluding start and end)
        current_file = from_square.file + file_step
        current_rank = from_square.rank + rank_step
        
        while current_file != to_square.file or current_rank != to_square.rank:
            square = Square(current_file, current_rank)
            if state.board.get_piece(square) is not None:
                return False
            
            current_file += file_step
            current_rank += rank_step
        
        return True
    
    def is_check(self, state: GameState, color: Color) -> bool:
        """
        Determine if the king of the given color is in check.
        
        A king is in check if it is under attack by any opponent piece.
        
        Args:
            state: Current game state
            color: Color of the king to check
        
        Returns:
            True if the king is in check
        """
        king_square = self.find_king_position(state, color)
        
        # If king not found, cannot be in check (shouldn't happen in valid game)
        if king_square is None:
            return False
        
        # Check if the king's square is under attack by the opponent
        opponent_color = color.opposite()
        return self.is_square_attacked(state, king_square, opponent_color)
