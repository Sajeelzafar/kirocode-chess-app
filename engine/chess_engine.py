"""Chess engine for orchestrating game logic and move execution."""

from typing import Optional, Tuple
from models.game_state import GameState, GameMode
from models.move import Move
from models.square import Square
from models.piece import Piece, PieceType, Color
from engine.move_generator import MoveGenerator
from engine.move_validator import MoveValidator
from engine.check_detector import CheckDetector


class ChessEngine:
    """
    Core chess engine that enforces rules and manages game state.
    
    Coordinates move generation, validation, and execution while maintaining
    game state consistency.
    """
    
    def __init__(self):
        """Initialize the chess engine with necessary components."""
        self.move_generator = MoveGenerator()
        self.move_validator = MoveValidator()
        self.check_detector = CheckDetector()
    
    def initialize_game(self, mode: GameMode) -> GameState:
        """
        Create a new game in single-player or multiplayer mode.
        
        Args:
            mode: Game mode (SINGLE_PLAYER or MULTIPLAYER)
        
        Returns:
            New GameState initialized for the specified mode
        
        Requirements: 1.1, 1.2
        """
        return GameState.new_game(mode)
    
    def execute_move(self, state: GameState, move: Move) -> GameState:
        """
        Execute a move and return the new game state.
        
        This method handles:
        - Normal piece moves
        - Pawn promotion
        - Castling (moving both king and rook)
        - En passant capture (removing captured pawn)
        - Updating castling rights when king or rook moves
        - Updating castling rights when rook is captured
        - Updating en passant target square
        - Updating halfmove clock and fullmove number
        - Adding move to move history
        - Adding position to position history
        - Switching current player
        
        Args:
            state: Current game state
            move: Move to execute
        
        Returns:
            New game state with the move applied
        
        Requirements: 2.2, 2.5, 3.5, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1
        """
        # Create a copy of the state to maintain immutability
        new_state = state.copy()
        
        # Remove piece from starting square
        new_state.board.remove_piece(move.from_square)
        
        # Handle special moves
        if move.is_castling:
            self._execute_castling(new_state, move)
        elif move.is_en_passant:
            self._execute_en_passant(new_state, move)
        else:
            # Normal move or capture
            self._execute_normal_move(new_state, move)
        
        # Update castling rights when king or rook moves (Requirement 7.4)
        new_state.castling_rights.revoke_for_piece(
            move.piece.piece_type,
            move.piece.color,
            move.from_square
        )
        
        # Update castling rights when rook is captured (Requirement 7.5)
        if move.captured_piece is not None and move.captured_piece.piece_type == PieceType.ROOK:
            new_state.castling_rights.revoke_for_rook_capture(move.to_square)
        
        # Update en passant target square (Requirement 7.2)
        new_state.en_passant_target = self._calculate_en_passant_target(move)
        
        # Update halfmove clock (Requirement 7.2, 7.3)
        # Reset on pawn move or capture, otherwise increment
        if move.piece.piece_type == PieceType.PAWN or move.captured_piece is not None:
            new_state.halfmove_clock = 0
        else:
            new_state.halfmove_clock += 1
        
        # Update fullmove number (increments after black's move)
        if state.current_player == Color.BLACK:
            new_state.fullmove_number += 1
        
        # Add move to move history (Requirement 8.1)
        new_state.move_history.append(move)
        
        # Switch current player (Requirement 2.5)
        new_state.current_player = state.current_player.opposite()
        
        # Add position to position history (for threefold repetition)
        new_state.position_history.append(new_state.compute_position_hash())
        
        return new_state
    
    def _execute_normal_move(self, state: GameState, move: Move) -> None:
        """
        Execute a normal move (including captures and promotions).
        
        Args:
            state: Game state to modify
            move: Move to execute
        """
        # Handle pawn promotion (Requirement 3.5)
        if move.promotion_piece is not None:
            promoted_piece = Piece(move.promotion_piece, move.piece.color)
            state.board.set_piece(move.to_square, promoted_piece)
        else:
            # Normal move - place piece at destination
            state.board.set_piece(move.to_square, move.piece)
    
    def _execute_castling(self, state: GameState, move: Move) -> None:
        """
        Execute a castling move (move both king and rook).
        
        Args:
            state: Game state to modify
            move: Castling move to execute
        
        Requirement 7.1: Move both king and rook to their castling positions
        """
        # Place king at destination
        state.board.set_piece(move.to_square, move.piece)
        
        # Determine rook positions based on king's destination
        rank = move.from_square.rank
        
        if move.to_square.file == 6:  # Kingside castling (king to g-file)
            # Move rook from h-file to f-file
            rook = state.board.get_piece(Square(7, rank))
            state.board.remove_piece(Square(7, rank))
            state.board.set_piece(Square(5, rank), rook)
        else:  # Queenside castling (king to c-file)
            # Move rook from a-file to d-file
            rook = state.board.get_piece(Square(0, rank))
            state.board.remove_piece(Square(0, rank))
            state.board.set_piece(Square(3, rank), rook)
    
    def _execute_en_passant(self, state: GameState, move: Move) -> None:
        """
        Execute an en passant capture (remove captured pawn).
        
        Args:
            state: Game state to modify
            move: En passant move to execute
        
        Requirement 7.3: Remove the captured pawn from the board
        """
        # Place capturing pawn at destination
        state.board.set_piece(move.to_square, move.piece)
        
        # Remove the captured pawn (on the same rank as the capturing pawn)
        captured_pawn_square = Square(move.to_square.file, move.from_square.rank)
        state.board.remove_piece(captured_pawn_square)
    
    def _calculate_en_passant_target(self, move: Move) -> Optional[Square]:
        """
        Calculate the en passant target square after a move.
        
        En passant is available when a pawn moves two squares forward.
        The target square is the square the pawn passed through.
        
        Args:
            move: Move that was just executed
        
        Returns:
            En passant target square, or None if not applicable
        
        Requirement 7.2: Enable en passant capture for opponent's next move only
        """
        # Only pawns moving two squares forward create en passant opportunities
        if move.piece.piece_type != PieceType.PAWN:
            return None
        
        rank_diff = abs(move.to_square.rank - move.from_square.rank)
        if rank_diff != 2:
            return None
        
        # The en passant target is the square the pawn passed through
        if move.piece.color == Color.WHITE:
            # White pawn moved from rank 1 to rank 3, target is rank 2
            return Square(move.from_square.file, move.from_square.rank + 1)
        else:
            # Black pawn moved from rank 6 to rank 4, target is rank 5
            return Square(move.from_square.file, move.from_square.rank - 1)
    
    def get_legal_moves(self, state: GameState, color: Color) -> list[Move]:
        """
        Get all legal moves for a given color.
        
        Args:
            state: Current game state
            color: Color to get legal moves for
        
        Returns:
            List of all legal moves
        
        Requirements: 2.1
        """
        # Generate pseudo-legal moves
        pseudo_legal_moves = self.move_generator.generate_pseudo_legal_moves(state, color)
        
        # Filter to only legal moves (those that don't leave king in check)
        legal_moves = []
        for move in pseudo_legal_moves:
            if self.move_validator.is_legal_move(state, move):
                legal_moves.append(move)
        
        return legal_moves
    
    def is_legal_move(self, state: GameState, move: Move) -> bool:
        """
        Check if a specific move is legal in the current game state.
        
        Args:
            state: Current game state
            move: Move to validate
        
        Returns:
            True if the move is legal
        
        Requirements: 2.3, 2.4
        """
        return self.move_validator.is_legal_move(state, move)
    
    def is_checkmate(self, state: GameState) -> bool:
        """
        Determine if the current player is in checkmate.
        
        Checkmate occurs when:
        1. The current player's king is in check
        2. The current player has no legal moves to escape check
        
        Args:
            state: Current game state
        
        Returns:
            True if the current player is in checkmate
        
        Requirement 4.1: Detect checkmate (in check with no legal moves)
        """
        # Must be in check for checkmate
        if not self.check_detector.is_check(state, state.current_player):
            return False
        
        # Check if there are any legal moves
        legal_moves = self.get_legal_moves(state, state.current_player)
        return len(legal_moves) == 0
    
    def is_stalemate(self, state: GameState) -> bool:
        """
        Determine if the game is in stalemate.
        
        Stalemate occurs when:
        1. The current player is NOT in check
        2. The current player has no legal moves
        
        Args:
            state: Current game state
        
        Returns:
            True if the game is in stalemate
        
        Requirement 4.2: Detect stalemate (no legal moves, not in check)
        """
        # Must NOT be in check for stalemate
        if self.check_detector.is_check(state, state.current_player):
            return False
        
        # Check if there are any legal moves
        legal_moves = self.get_legal_moves(state, state.current_player)
        return len(legal_moves) == 0
    
    def is_threefold_repetition(self, state: GameState) -> bool:
        """
        Determine if the current position has occurred three times.
        
        The same position is defined as:
        - Same piece positions
        - Same player to move
        - Same castling rights
        - Same en passant availability
        
        Args:
            state: Current game state
        
        Returns:
            True if the current position has occurred three times
        
        Requirement 4.3: Detect threefold repetition
        """
        if len(state.position_history) < 3:
            return False
        
        current_position_hash = state.compute_position_hash()
        
        # Count how many times this position has occurred
        count = state.position_history.count(current_position_hash)
        
        return count >= 3
    
    def is_fifty_move_rule(self, state: GameState) -> bool:
        """
        Determine if the fifty-move rule applies.
        
        The fifty-move rule states that a draw can be claimed if 50 consecutive
        moves have been made without any pawn move or capture.
        
        Args:
            state: Current game state
        
        Returns:
            True if 50 moves have occurred without pawn move or capture
        
        Requirement 4.4: Detect fifty-move rule
        """
        return state.halfmove_clock >= 100  # 100 halfmoves = 50 full moves
    
    def is_insufficient_material(self, state: GameState) -> bool:
        """
        Determine if there is insufficient material for either side to checkmate.
        
        Insufficient material scenarios:
        - King vs King
        - King + Bishop vs King
        - King + Knight vs King
        - King + Bishop vs King + Bishop (same color bishops)
        
        Args:
            state: Current game state
        
        Returns:
            True if neither side has sufficient material to checkmate
        
        Requirement 4.5: Detect insufficient material
        """
        white_pieces = state.board.get_all_pieces(Color.WHITE)
        black_pieces = state.board.get_all_pieces(Color.BLACK)
        
        # Count pieces by type for each color
        white_counts = self._count_pieces_by_type(white_pieces)
        black_counts = self._count_pieces_by_type(black_pieces)
        
        # King vs King
        if (white_counts['total'] == 1 and black_counts['total'] == 1):
            return True
        
        # King + Bishop vs King
        if (white_counts['total'] == 2 and white_counts[PieceType.BISHOP] == 1 and
            black_counts['total'] == 1):
            return True
        
        if (black_counts['total'] == 2 and black_counts[PieceType.BISHOP] == 1 and
            white_counts['total'] == 1):
            return True
        
        # King + Knight vs King
        if (white_counts['total'] == 2 and white_counts[PieceType.KNIGHT] == 1 and
            black_counts['total'] == 1):
            return True
        
        if (black_counts['total'] == 2 and black_counts[PieceType.KNIGHT] == 1 and
            white_counts['total'] == 1):
            return True
        
        # King + Bishop vs King + Bishop (same color bishops)
        if (white_counts['total'] == 2 and white_counts[PieceType.BISHOP] == 1 and
            black_counts['total'] == 2 and black_counts[PieceType.BISHOP] == 1):
            # Check if bishops are on same color squares
            white_bishop_square = self._find_piece_square(white_pieces, PieceType.BISHOP)
            black_bishop_square = self._find_piece_square(black_pieces, PieceType.BISHOP)
            
            if white_bishop_square and black_bishop_square:
                # Bishops are on same color if sum of coordinates has same parity
                white_square_color = (white_bishop_square.file + white_bishop_square.rank) % 2
                black_square_color = (black_bishop_square.file + black_bishop_square.rank) % 2
                
                if white_square_color == black_square_color:
                    return True
        
        return False
    
    def _count_pieces_by_type(self, pieces: dict) -> dict:
        """
        Count pieces by type.
        
        Args:
            pieces: Dictionary mapping squares to pieces
        
        Returns:
            Dictionary with counts for each piece type and total count
        """
        counts = {
            PieceType.PAWN: 0,
            PieceType.KNIGHT: 0,
            PieceType.BISHOP: 0,
            PieceType.ROOK: 0,
            PieceType.QUEEN: 0,
            PieceType.KING: 0,
            'total': 0
        }
        
        for piece in pieces.values():
            counts[piece.piece_type] += 1
            counts['total'] += 1
        
        return counts
    
    def _find_piece_square(self, pieces: dict, piece_type: PieceType) -> Optional[Square]:
        """
        Find the square of a specific piece type.
        
        Args:
            pieces: Dictionary mapping squares to pieces
            piece_type: Type of piece to find
        
        Returns:
            Square where the piece is located, or None if not found
        """
        for square, piece in pieces.items():
            if piece.piece_type == piece_type:
                return square
        return None
    
    def is_draw(self, state: GameState) -> bool:
        """
        Check if the game is a draw by any condition.
        
        Draw conditions:
        - Stalemate
        - Threefold repetition
        - Fifty-move rule
        - Insufficient material
        
        Args:
            state: Current game state
        
        Returns:
            True if any draw condition is met
        
        Requirements: 4.2, 4.3, 4.4, 4.5
        """
        return (self.is_stalemate(state) or
                self.is_threefold_repetition(state) or
                self.is_fifty_move_rule(state) or
                self.is_insufficient_material(state))
    
    def get_algebraic_notation(self, state: GameState, move: Move) -> str:
        """
        Generate algebraic notation for a move with proper disambiguation.
        
        This method determines:
        - Whether the move results in check or checkmate
        - Whether disambiguation is needed (file, rank, or both)
        
        Args:
            state: Game state before the move
            move: Move to convert to algebraic notation
        
        Returns:
            Algebraic notation string
        
        Requirements: 8.2, 8.3, 8.4, 8.5
        """
        # Execute the move to check for check/checkmate
        new_state = self.execute_move(state, move)
        
        # Determine if the move results in check or checkmate
        is_check = self.check_detector.is_check(new_state, new_state.current_player)
        is_checkmate = False
        
        if is_check:
            # Check if it's checkmate (no legal moves to escape)
            is_checkmate = self.is_checkmate(new_state)
        
        # Determine disambiguation needs
        disambiguate_file, disambiguate_rank = self._get_disambiguation(state, move)
        
        # Generate the notation
        return move.to_algebraic_notation(
            game_state=new_state,
            is_check=is_check,
            is_checkmate=is_checkmate,
            disambiguate_file=disambiguate_file,
            disambiguate_rank=disambiguate_rank
        )
    
    def _get_disambiguation(self, state: GameState, move: Move) -> Tuple[bool, bool]:
        """
        Determine if disambiguation is needed for a move.
        
        Disambiguation is needed when multiple pieces of the same type
        can move to the same destination square.
        
        Args:
            state: Current game state
            move: Move to check for disambiguation
        
        Returns:
            Tuple of (disambiguate_file, disambiguate_rank)
        """
        # Pawns and kings never need disambiguation (except pawn captures, handled separately)
        if move.piece.piece_type in [PieceType.PAWN, PieceType.KING]:
            return (False, False)
        
        # Castling never needs disambiguation
        if move.is_castling:
            return (False, False)
        
        # Get all legal moves for the current player
        all_legal_moves = self.get_legal_moves(state, state.current_player)
        
        # Find other pieces of the same type that can move to the same square
        same_destination_moves = []
        for other_move in all_legal_moves:
            if (other_move.piece.piece_type == move.piece.piece_type and
                other_move.to_square == move.to_square and
                other_move.from_square != move.from_square):
                same_destination_moves.append(other_move)
        
        # No disambiguation needed if no other pieces can move there
        if not same_destination_moves:
            return (False, False)
        
        # Check if file disambiguation is sufficient
        file_unique = True
        for other_move in same_destination_moves:
            if other_move.from_square.file == move.from_square.file:
                file_unique = False
                break
        
        if file_unique:
            return (True, False)
        
        # Check if rank disambiguation is sufficient
        rank_unique = True
        for other_move in same_destination_moves:
            if other_move.from_square.rank == move.from_square.rank:
                rank_unique = False
                break
        
        if rank_unique:
            return (False, True)
        
        # Need both file and rank for full disambiguation
        return (True, True)
