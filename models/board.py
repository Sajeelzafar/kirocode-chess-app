"""Board component for managing the 8x8 chess board and piece positions."""

from typing import Optional, List, Dict
from copy import deepcopy
from .piece import Piece, PieceType, Color
from .square import Square


class Board:
    """Manages the 8x8 chess board and piece positions."""
    
    def __init__(self):
        """Initialize an empty 8x8 board."""
        # 8x8 grid where None represents empty square
        # grid[rank][file] corresponds to the square at (file, rank)
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
    
    def get_piece(self, square: Square) -> Optional[Piece]:
        """
        Get the piece at the given square.
        
        Args:
            square: The square to check
        
        Returns:
            The piece at the square, or None if empty
        """
        return self.grid[square.rank][square.file]
    
    def set_piece(self, square: Square, piece: Piece) -> None:
        """
        Place a piece at the given square.
        
        Args:
            square: The square to place the piece
            piece: The piece to place
        """
        self.grid[square.rank][square.file] = piece
    
    def remove_piece(self, square: Square) -> None:
        """
        Remove the piece from the given square.
        
        Args:
            square: The square to clear
        """
        self.grid[square.rank][square.file] = None
    
    def get_all_pieces(self, color: Color) -> Dict[Square, Piece]:
        """
        Get all pieces of a given color.
        
        Args:
            color: The color of pieces to retrieve
        
        Returns:
            Dictionary mapping squares to pieces for all pieces of the given color
        """
        pieces = {}
        for rank in range(8):
            for file in range(8):
                piece = self.grid[rank][file]
                if piece is not None and piece.color == color:
                    square = Square(file, rank)
                    pieces[square] = piece
        return pieces
    
    def copy(self) -> 'Board':
        """
        Create a deep copy of the board.
        
        Returns:
            A new Board instance with the same piece positions
        """
        new_board = Board()
        for rank in range(8):
            for file in range(8):
                piece = self.grid[rank][file]
                if piece is not None:
                    # Create new Piece instances to ensure deep copy
                    new_board.grid[rank][file] = Piece(piece.piece_type, piece.color)
                else:
                    new_board.grid[rank][file] = None
        return new_board
    
    def setup_standard_position(self) -> None:
        """
        Set up the board with all pieces in their standard starting positions.
        
        Standard chess starting position:
        - Rank 1 (white): Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        - Rank 2 (white): All pawns
        - Rank 7 (black): All pawns
        - Rank 8 (black): Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        """
        # Clear the board first
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        
        # Set up white pieces (rank 0 = rank 1 in chess notation)
        piece_order = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        
        for file, piece_type in enumerate(piece_order):
            # White pieces on rank 1 (index 0)
            self.grid[0][file] = Piece(piece_type, Color.WHITE)
            # Black pieces on rank 8 (index 7)
            self.grid[7][file] = Piece(piece_type, Color.BLACK)
        
        # Set up pawns
        for file in range(8):
            # White pawns on rank 2 (index 1)
            self.grid[1][file] = Piece(PieceType.PAWN, Color.WHITE)
            # Black pawns on rank 7 (index 6)
            self.grid[6][file] = Piece(PieceType.PAWN, Color.BLACK)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        lines = []
        for rank in range(7, -1, -1):  # Display from rank 8 to rank 1
            line = f"{rank + 1} "
            for file in range(8):
                piece = self.grid[rank][file]
                if piece is None:
                    line += ". "
                else:
                    line += piece.to_symbol() + " "
            lines.append(line)
        lines.append("  a b c d e f g h")
        return "\n".join(lines)
