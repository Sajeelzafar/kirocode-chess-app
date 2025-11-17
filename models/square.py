"""Square representation with algebraic notation conversion."""

from typing import Optional


class Square:
    """Represents a square on the chess board using file (0-7) and rank (0-7)."""
    
    def __init__(self, file: int, rank: int):
        """
        Initialize a square with file and rank coordinates.
        
        Args:
            file: Column index (0-7 representing a-h)
            rank: Row index (0-7 representing 1-8)
        
        Raises:
            ValueError: If file or rank is out of bounds
        """
        if not (0 <= file <= 7):
            raise ValueError(f"File must be between 0 and 7, got {file}")
        if not (0 <= rank <= 7):
            raise ValueError(f"Rank must be between 0 and 7, got {rank}")
        
        self.file = file
        self.rank = rank
    
    @classmethod
    def from_algebraic(cls, notation: str) -> 'Square':
        """
        Create a Square from algebraic notation (e.g., 'e4').
        
        Args:
            notation: Algebraic notation string (e.g., 'a1', 'h8')
        
        Returns:
            Square instance
        
        Raises:
            ValueError: If notation is invalid
        """
        if len(notation) != 2:
            raise ValueError(f"Algebraic notation must be 2 characters, got '{notation}'")
        
        file_char = notation[0].lower()
        rank_char = notation[1]
        
        if file_char not in 'abcdefgh':
            raise ValueError(f"File must be a-h, got '{file_char}'")
        if rank_char not in '12345678':
            raise ValueError(f"Rank must be 1-8, got '{rank_char}'")
        
        file = ord(file_char) - ord('a')
        rank = int(rank_char) - 1
        
        return cls(file, rank)
    
    def to_algebraic(self) -> str:
        """
        Convert square to algebraic notation.
        
        Returns:
            Algebraic notation string (e.g., 'e4')
        """
        file_char = chr(ord('a') + self.file)
        rank_char = str(self.rank + 1)
        return file_char + rank_char
    
    def __eq__(self, other) -> bool:
        """Check equality with another Square."""
        if not isinstance(other, Square):
            return False
        return self.file == other.file and self.rank == other.rank
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries."""
        return hash((self.file, self.rank))
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Square({self.to_algebraic()})"
