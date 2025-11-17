"""Move representation with all necessary fields."""

from typing import Optional
from .square import Square
from .piece import Piece, PieceType


class Move:
    """Represents a chess move with all necessary information."""
    
    def __init__(
        self,
        from_square: Square,
        to_square: Square,
        piece: Piece,
        captured_piece: Optional[Piece] = None,
        promotion_piece: Optional[PieceType] = None,
        is_castling: bool = False,
        is_en_passant: bool = False
    ):
        """
        Initialize a move.
        
        Args:
            from_square: Starting position
            to_square: Destination position
            piece: Piece being moved
            captured_piece: Piece captured (if any)
            promotion_piece: Piece type for pawn promotion (if applicable)
            is_castling: Flag for castling moves
            is_en_passant: Flag for en passant captures
        """
        self.from_square = from_square
        self.to_square = to_square
        self.piece = piece
        self.captured_piece = captured_piece
        self.promotion_piece = promotion_piece
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
    
    def __eq__(self, other) -> bool:
        """Check equality with another Move."""
        if not isinstance(other, Move):
            return False
        return (
            self.from_square == other.from_square and
            self.to_square == other.to_square and
            self.piece == other.piece and
            self.captured_piece == other.captured_piece and
            self.promotion_piece == other.promotion_piece and
            self.is_castling == other.is_castling and
            self.is_en_passant == other.is_en_passant
        )
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries."""
        return hash((
            self.from_square,
            self.to_square,
            self.piece,
            self.captured_piece,
            self.promotion_piece,
            self.is_castling,
            self.is_en_passant
        ))
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"Move({self.from_square.to_algebraic()} -> {self.to_square.to_algebraic()}, "
            f"{self.piece})"
        )
    
    def to_algebraic_notation(self, game_state=None, is_check: bool = False, is_checkmate: bool = False, 
                              disambiguate_file: bool = False, disambiguate_rank: bool = False) -> str:
        """
        Convert move to standard algebraic notation.
        
        Handles:
        - Piece notation (K, Q, R, B, N, or empty for pawns)
        - Capture notation (x)
        - Check notation (+)
        - Checkmate notation (#)
        - Castling notation (O-O, O-O-O)
        - Pawn promotion notation (=Q, =R, =B, =N)
        - Disambiguation when multiple pieces can move to same square
        
        Args:
            game_state: Optional game state for determining check/checkmate
            is_check: Whether the move results in check
            is_checkmate: Whether the move results in checkmate
            disambiguate_file: Whether to include file for disambiguation
            disambiguate_rank: Whether to include rank for disambiguation
        
        Returns:
            Algebraic notation string (e.g., "e4", "Nf3", "O-O", "exd5+")
        
        Requirements: 8.2, 8.3, 8.4, 8.5
        """
        # Handle castling notation (Requirement 8.2)
        if self.is_castling:
            # Kingside castling: king moves to g-file
            if self.to_square.file == 6:
                notation = "O-O"
            # Queenside castling: king moves to c-file
            else:
                notation = "O-O-O"
            
            # Add check/checkmate notation (Requirement 8.5)
            if is_checkmate:
                notation += "#"
            elif is_check:
                notation += "+"
            
            return notation
        
        # Start building the notation
        notation = ""
        
        # Add piece notation (Requirement 8.2)
        # Pawns have no piece letter, other pieces use uppercase letter
        if self.piece.piece_type == PieceType.PAWN:
            # For pawn captures, include the starting file
            if self.captured_piece is not None or self.is_en_passant:
                notation += chr(ord('a') + self.from_square.file)
        else:
            # Map piece types to their notation letters
            piece_letters = {
                PieceType.KNIGHT: 'N',
                PieceType.BISHOP: 'B',
                PieceType.ROOK: 'R',
                PieceType.QUEEN: 'Q',
                PieceType.KING: 'K'
            }
            notation += piece_letters[self.piece.piece_type]
            
            # Add disambiguation if needed (Requirement 8.2)
            if disambiguate_file:
                notation += chr(ord('a') + self.from_square.file)
            if disambiguate_rank:
                notation += str(self.from_square.rank + 1)
        
        # Add capture notation (Requirement 8.4)
        if self.captured_piece is not None or self.is_en_passant:
            notation += "x"
        
        # Add destination square (Requirement 8.2)
        notation += self.to_square.to_algebraic()
        
        # Add promotion notation (Requirement 8.2)
        if self.promotion_piece is not None:
            promotion_letters = {
                PieceType.KNIGHT: 'N',
                PieceType.BISHOP: 'B',
                PieceType.ROOK: 'R',
                PieceType.QUEEN: 'Q'
            }
            notation += "=" + promotion_letters[self.promotion_piece]
        
        # Add check/checkmate notation (Requirement 8.5)
        if is_checkmate:
            notation += "#"
        elif is_check:
            notation += "+"
        
        return notation
