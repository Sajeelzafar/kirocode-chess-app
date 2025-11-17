"""Castling rights tracking."""

from .piece import Color, PieceType
from .square import Square


class CastlingRights:
    """Tracks which castling moves are still available for each player."""
    
    def __init__(
        self,
        white_kingside: bool = True,
        white_queenside: bool = True,
        black_kingside: bool = True,
        black_queenside: bool = True
    ):
        """
        Initialize castling rights.
        
        Args:
            white_kingside: Can white castle kingside
            white_queenside: Can white castle queenside
            black_kingside: Can black castle kingside
            black_queenside: Can black castle queenside
        """
        self.white_kingside = white_kingside
        self.white_queenside = white_queenside
        self.black_kingside = black_kingside
        self.black_queenside = black_queenside
    
    def revoke_for_piece(self, piece_type: PieceType, color: Color, square: Square) -> None:
        """
        Revoke castling rights when a king or rook moves.
        
        Args:
            piece_type: Type of piece that moved
            color: Color of the piece
            square: Square the piece moved from
        """
        if piece_type == PieceType.KING:
            # King moved - revoke both castling rights for that color
            if color == Color.WHITE:
                self.white_kingside = False
                self.white_queenside = False
            else:
                self.black_kingside = False
                self.black_queenside = False
        
        elif piece_type == PieceType.ROOK:
            # Rook moved - revoke castling on that side
            if color == Color.WHITE:
                if square.file == 0 and square.rank == 0:  # a1 - queenside
                    self.white_queenside = False
                elif square.file == 7 and square.rank == 0:  # h1 - kingside
                    self.white_kingside = False
            else:
                if square.file == 0 and square.rank == 7:  # a8 - queenside
                    self.black_queenside = False
                elif square.file == 7 and square.rank == 7:  # h8 - kingside
                    self.black_kingside = False
    
    def revoke_for_rook_capture(self, square: Square) -> None:
        """
        Revoke castling rights when a rook is captured.
        
        Args:
            square: Square where the rook was captured
        """
        # Check if a rook on a starting square was captured
        if square.file == 0 and square.rank == 0:  # a1 - white queenside
            self.white_queenside = False
        elif square.file == 7 and square.rank == 0:  # h1 - white kingside
            self.white_kingside = False
        elif square.file == 0 and square.rank == 7:  # a8 - black queenside
            self.black_queenside = False
        elif square.file == 7 and square.rank == 7:  # h8 - black kingside
            self.black_kingside = False
    
    def copy(self) -> 'CastlingRights':
        """
        Create a deep copy of castling rights.
        
        Returns:
            New CastlingRights instance with same values
        """
        return CastlingRights(
            white_kingside=self.white_kingside,
            white_queenside=self.white_queenside,
            black_kingside=self.black_kingside,
            black_queenside=self.black_queenside
        )
    
    def __eq__(self, other) -> bool:
        """Check equality with another CastlingRights."""
        if not isinstance(other, CastlingRights):
            return False
        return (
            self.white_kingside == other.white_kingside and
            self.white_queenside == other.white_queenside and
            self.black_kingside == other.black_kingside and
            self.black_queenside == other.black_queenside
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        rights = []
        if self.white_kingside:
            rights.append("K")
        if self.white_queenside:
            rights.append("Q")
        if self.black_kingside:
            rights.append("k")
        if self.black_queenside:
            rights.append("q")
        return f"CastlingRights({''.join(rights) if rights else '-'})"
