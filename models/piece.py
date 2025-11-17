"""Piece representation with type and color."""

from enum import Enum


class PieceType(Enum):
    """Enumeration of chess piece types."""
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class Color(Enum):
    """Enumeration of piece colors."""
    WHITE = "white"
    BLACK = "black"
    
    def opposite(self) -> 'Color':
        """Return the opposite color."""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class Piece:
    """Represents a chess piece with type and color."""
    
    def __init__(self, piece_type: PieceType, color: Color):
        """
        Initialize a piece.
        
        Args:
            piece_type: Type of the piece
            color: Color of the piece
        """
        self.piece_type = piece_type
        self.color = color
    
    def __eq__(self, other) -> bool:
        """Check equality with another Piece."""
        if not isinstance(other, Piece):
            return False
        return self.piece_type == other.piece_type and self.color == other.color
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries."""
        return hash((self.piece_type, self.color))
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Piece({self.color.value} {self.piece_type.value})"
    
    def to_symbol(self) -> str:
        """
        Convert piece to a single character symbol.
        
        Returns:
            Single character representing the piece (uppercase for white, lowercase for black)
        """
        symbols = {
            PieceType.PAWN: 'P',
            PieceType.KNIGHT: 'N',
            PieceType.BISHOP: 'B',
            PieceType.ROOK: 'R',
            PieceType.QUEEN: 'Q',
            PieceType.KING: 'K'
        }
        symbol = symbols[self.piece_type]
        return symbol if self.color == Color.WHITE else symbol.lower()
