"""GameState component representing the complete state of a chess game."""

from typing import Optional, List, Tuple
from enum import Enum
from .board import Board
from .piece import Color
from .castling_rights import CastlingRights
from .square import Square
from .move import Move


class GameMode(Enum):
    """Enumeration for game types."""
    SINGLE_PLAYER = "single_player"  # Human vs AI
    MULTIPLAYER = "multiplayer"      # Human vs Human


class GameState:
    """
    Represents the complete state of a chess game at any point in time.
    
    This includes the board position, whose turn it is, castling rights,
    en passant availability, move counters, and game history.
    """
    
    def __init__(
        self,
        board: Board,
        current_player: Color,
        castling_rights: CastlingRights,
        en_passant_target: Optional[Square] = None,
        halfmove_clock: int = 0,
        fullmove_number: int = 1,
        move_history: Optional[List[Move]] = None,
        position_history: Optional[List[int]] = None,
        game_mode: GameMode = GameMode.MULTIPLAYER
    ):
        """
        Initialize a game state.
        
        Args:
            board: The 8x8 chess board with piece positions
            current_player: Color of the player whose turn it is
            castling_rights: Available castling options for both players
            en_passant_target: Square where en passant capture is possible (if any)
            halfmove_clock: Number of halfmoves since last pawn move or capture
            fullmove_number: Number of full moves (increments after black's move)
            move_history: Complete list of moves played in the game
            position_history: List of position hashes for threefold repetition detection
            game_mode: Single-player or multiplayer mode
        """
        self.board = board
        self.current_player = current_player
        self.castling_rights = castling_rights
        self.en_passant_target = en_passant_target
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number
        self.move_history = move_history if move_history is not None else []
        self.position_history = position_history if position_history is not None else []
        self.game_mode = game_mode
    
    @classmethod
    def new_game(cls, mode: GameMode = GameMode.MULTIPLAYER) -> 'GameState':
        """
        Create a new game state with standard starting position.
        
        Args:
            mode: Game mode (single-player or multiplayer)
        
        Returns:
            GameState initialized for a new game
        """
        board = Board()
        board.setup_standard_position()
        
        castling_rights = CastlingRights(
            white_kingside=True,
            white_queenside=True,
            black_kingside=True,
            black_queenside=True
        )
        
        state = cls(
            board=board,
            current_player=Color.WHITE,
            castling_rights=castling_rights,
            en_passant_target=None,
            halfmove_clock=0,
            fullmove_number=1,
            move_history=[],
            position_history=[],
            game_mode=mode
        )
        
        # Add initial position to history
        state.position_history.append(state.compute_position_hash())
        
        return state
    
    def compute_position_hash(self) -> int:
        """
        Compute a hash of the current position for threefold repetition detection.
        
        The hash includes:
        - All piece positions on the board
        - Current player to move
        - Castling rights
        - En passant target square
        
        Returns:
            Integer hash representing the position
        """
        # Start with a base hash
        hash_value = 0
        
        # Hash piece positions
        for rank in range(8):
            for file in range(8):
                piece = self.board.grid[rank][file]
                if piece is not None:
                    # Combine square position, piece type, and color into hash
                    square_hash = (rank * 8 + file)
                    piece_hash = hash((piece.piece_type, piece.color))
                    hash_value ^= (square_hash * 31 + piece_hash)
        
        # Hash current player
        hash_value ^= hash(self.current_player) * 17
        
        # Hash castling rights
        castling_hash = (
            (1 if self.castling_rights.white_kingside else 0) |
            (2 if self.castling_rights.white_queenside else 0) |
            (4 if self.castling_rights.black_kingside else 0) |
            (8 if self.castling_rights.black_queenside else 0)
        )
        hash_value ^= castling_hash * 13
        
        # Hash en passant target
        if self.en_passant_target is not None:
            ep_hash = self.en_passant_target.rank * 8 + self.en_passant_target.file
            hash_value ^= ep_hash * 19
        
        return hash_value
    
    def copy(self) -> 'GameState':
        """
        Create a deep copy of the game state.
        
        Returns:
            New GameState instance with copied values
        """
        return GameState(
            board=self.board.copy(),
            current_player=self.current_player,
            castling_rights=self.castling_rights.copy(),
            en_passant_target=self.en_passant_target,  # Square is immutable
            halfmove_clock=self.halfmove_clock,
            fullmove_number=self.fullmove_number,
            move_history=self.move_history.copy(),  # Shallow copy of list
            position_history=self.position_history.copy(),  # Shallow copy of list
            game_mode=self.game_mode
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"GameState(\n"
            f"  current_player={self.current_player.value},\n"
            f"  fullmove={self.fullmove_number},\n"
            f"  halfmove_clock={self.halfmove_clock},\n"
            f"  castling={self.castling_rights},\n"
            f"  en_passant={self.en_passant_target.to_algebraic() if self.en_passant_target else None},\n"
            f"  mode={self.game_mode.value}\n"
            f")"
        )
