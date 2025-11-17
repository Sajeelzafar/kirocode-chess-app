"""GameController for orchestrating chess game flow and user interactions."""

from typing import Optional, List
from models.game_state import GameState, GameMode
from models.square import Square
from models.move import Move
from models.piece import PieceType, Color
from engine.chess_engine import ChessEngine
from ai.ai_opponent import AIOpponent


class GameController:
    """
    Orchestrates game flow and coordinates between engine, AI, and UI.
    
    Manages:
    - Game initialization for different modes
    - User interactions (square selection, move attempts)
    - AI move generation in single-player mode
    - Pawn promotion handling
    - Game state tracking
    
    Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.5
    """
    
    def __init__(self):
        """Initialize the game controller with engine and AI components."""
        self.engine = ChessEngine()
        self.ai_opponent = AIOpponent(self.engine)
        self.state: Optional[GameState] = None
        self.selected_square: Optional[Square] = None
        self.pending_promotion_move: Optional[Move] = None
    
    def start_new_game(self, mode: GameMode) -> GameState:
        """
        Initialize a new game in the specified mode.
        
        Args:
            mode: GameMode.SINGLE_PLAYER or GameMode.MULTIPLAYER
        
        Returns:
            Initial game state
        
        Requirements: 1.1, 1.2
        """
        self.state = self.engine.initialize_game(mode)
        self.selected_square = None
        self.pending_promotion_move = None
        return self.state
    
    def handle_square_selection(self, square: Square) -> dict:
        """
        Process a player selecting a square on the board.
        
        Behavior:
        - If no piece is selected and square contains current player's piece: select it
        - If a piece is already selected and square is a valid destination: attempt move
        - If a piece is already selected and square contains current player's piece: reselect
        - Otherwise: clear selection
        
        Args:
            square: Square that was selected
        
        Returns:
            Dictionary with:
                - 'action': 'selected', 'move_attempted', 'promotion_required', or 'cleared'
                - 'selected_square': Currently selected square (if any)
                - 'legal_moves': List of legal moves for selected piece (if any)
                - 'move': Move that was attempted (if applicable)
                - 'state': Current game state
        
        Requirements: 2.1, 2.3
        """
        if self.state is None:
            raise ValueError("No game in progress")
        
        # Check if there's a pending promotion
        if self.pending_promotion_move is not None:
            return {
                'action': 'promotion_required',
                'selected_square': None,
                'legal_moves': [],
                'state': self.state
            }
        
        piece = self.state.board.get_piece(square)
        
        # Case 1: No piece selected yet
        if self.selected_square is None:
            # Select piece if it belongs to current player
            if piece is not None and piece.color == self.state.current_player:
                self.selected_square = square
                legal_moves = self._get_legal_moves_for_square(square)
                return {
                    'action': 'selected',
                    'selected_square': self.selected_square,
                    'legal_moves': legal_moves,
                    'state': self.state
                }
            else:
                # Invalid selection (empty square or opponent's piece)
                return {
                    'action': 'cleared',
                    'selected_square': None,
                    'legal_moves': [],
                    'state': self.state
                }
        
        # Case 2: Piece already selected
        else:
            # If clicking on another piece of the same color, reselect
            if piece is not None and piece.color == self.state.current_player:
                self.selected_square = square
                legal_moves = self._get_legal_moves_for_square(square)
                return {
                    'action': 'selected',
                    'selected_square': self.selected_square,
                    'legal_moves': legal_moves,
                    'state': self.state
                }
            
            # Otherwise, attempt to move to this square
            return self.handle_move_attempt(self.selected_square, square)
    
    def handle_move_attempt(self, from_square: Square, to_square: Square) -> dict:
        """
        Process a player attempting to move a piece.
        
        Args:
            from_square: Starting square
            to_square: Destination square
        
        Returns:
            Dictionary with:
                - 'action': 'move_executed', 'promotion_required', 'invalid_move', or 'game_over'
                - 'move': Move that was executed (if successful)
                - 'state': Updated game state
                - 'selected_square': None (selection cleared after move)
                - 'game_over': True if game ended
                - 'result': Game result if game ended
        
        Requirements: 2.2, 2.4, 3.5
        """
        if self.state is None:
            raise ValueError("No game in progress")
        
        # Find the move in legal moves
        legal_moves = self._get_legal_moves_for_square(from_square)
        move = self._find_move(legal_moves, from_square, to_square)
        
        if move is None:
            # Invalid move - reject and clear selection (Requirement 2.4)
            self.selected_square = None
            return {
                'action': 'invalid_move',
                'selected_square': None,
                'state': self.state
            }
        
        # Check if this is a pawn promotion (Requirement 3.5)
        if self._is_promotion_move(move):
            # Store the move and wait for promotion choice
            self.pending_promotion_move = move
            return {
                'action': 'promotion_required',
                'move': move,
                'selected_square': None,
                'state': self.state
            }
        
        # Execute the move (Requirement 2.2)
        return self._execute_move_and_check_game_state(move)
    
    def handle_promotion_choice(self, piece_type: PieceType) -> dict:
        """
        Process a player's choice for pawn promotion.
        
        Args:
            piece_type: Type of piece to promote to (QUEEN, ROOK, BISHOP, or KNIGHT)
        
        Returns:
            Dictionary with move execution result
        
        Requirement 3.5: Handle pawn promotion
        """
        if self.state is None:
            raise ValueError("No game in progress")
        
        if self.pending_promotion_move is None:
            raise ValueError("No pending promotion")
        
        # Validate promotion piece type
        if piece_type not in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
            raise ValueError(f"Invalid promotion piece type: {piece_type}")
        
        # Set the promotion piece on the move
        self.pending_promotion_move.promotion_piece = piece_type
        
        # Execute the move
        move = self.pending_promotion_move
        self.pending_promotion_move = None
        
        return self._execute_move_and_check_game_state(move)
    
    def get_current_state(self) -> Optional[GameState]:
        """
        Get the current game state.
        
        Returns:
            Current GameState, or None if no game in progress
        """
        return self.state
    
    def get_selected_square(self) -> Optional[Square]:
        """
        Get the currently selected square.
        
        Returns:
            Selected square, or None if no square is selected
        """
        return self.selected_square
    
    def get_legal_moves_for_selected(self) -> List[Move]:
        """
        Get legal moves for the currently selected piece.
        
        Returns:
            List of legal moves, or empty list if no piece selected
        """
        if self.selected_square is None or self.state is None:
            return []
        
        return self._get_legal_moves_for_square(self.selected_square)
    
    def generate_ai_move(self) -> Optional[dict]:
        """
        Generate and execute an AI move in single-player mode.
        
        Returns:
            Dictionary with move execution result, or None if not AI's turn
        
        Requirement 1.1: Integrate AI move generation for single-player mode
        """
        if self.state is None:
            return None
        
        # Only generate AI move in single-player mode when it's black's turn
        if self.state.game_mode != GameMode.SINGLE_PLAYER:
            return None
        
        if self.state.current_player != Color.BLACK:
            return None
        
        # Generate AI move
        move = self.ai_opponent.select_move(self.state)
        
        if move is None:
            # No legal moves - game should be over
            return {
                'action': 'game_over',
                'state': self.state,
                'result': self._get_game_result()
            }
        
        # Execute the AI's move
        return self._execute_move_and_check_game_state(move)
    
    def _get_legal_moves_for_square(self, square: Square) -> List[Move]:
        """
        Get all legal moves for a piece at the given square.
        
        Args:
            square: Square to get moves for
        
        Returns:
            List of legal moves
        """
        if self.state is None:
            return []
        
        piece = self.state.board.get_piece(square)
        if piece is None:
            return []
        
        # Get all legal moves for the current player
        all_legal_moves = self.engine.get_legal_moves(self.state, self.state.current_player)
        
        # Filter to moves from this square
        return [move for move in all_legal_moves if move.from_square == square]
    
    def _find_move(self, legal_moves: List[Move], from_square: Square, to_square: Square) -> Optional[Move]:
        """
        Find a move in the legal moves list matching the from/to squares.
        
        Args:
            legal_moves: List of legal moves
            from_square: Starting square
            to_square: Destination square
        
        Returns:
            Matching move, or None if not found
        """
        for move in legal_moves:
            if move.from_square == from_square and move.to_square == to_square:
                return move
        return None
    
    def _is_promotion_move(self, move: Move) -> bool:
        """
        Check if a move is a pawn promotion.
        
        Args:
            move: Move to check
        
        Returns:
            True if this is a pawn reaching the final rank
        """
        if move.piece.piece_type != PieceType.PAWN:
            return False
        
        # White pawns promote on rank 7 (0-indexed), black pawns on rank 0
        if move.piece.color == Color.WHITE:
            return move.to_square.rank == 7
        else:
            return move.to_square.rank == 0
    
    def _execute_move_and_check_game_state(self, move: Move) -> dict:
        """
        Execute a move and check for game-ending conditions.
        
        Args:
            move: Move to execute
        
        Returns:
            Dictionary with execution result and game state
        """
        # Execute the move
        self.state = self.engine.execute_move(self.state, move)
        self.selected_square = None
        
        # Check for game-ending conditions
        if self.engine.is_checkmate(self.state):
            return {
                'action': 'game_over',
                'move': move,
                'state': self.state,
                'game_over': True,
                'result': f"Checkmate! {self.state.current_player.opposite().value.capitalize()} wins!"
            }
        
        if self.engine.is_draw(self.state):
            draw_reason = self._get_draw_reason()
            return {
                'action': 'game_over',
                'move': move,
                'state': self.state,
                'game_over': True,
                'result': f"Draw by {draw_reason}"
            }
        
        # Game continues
        return {
            'action': 'move_executed',
            'move': move,
            'state': self.state,
            'selected_square': None
        }
    
    def _get_game_result(self) -> str:
        """
        Get the result of the game.
        
        Returns:
            String describing the game result
        """
        if self.engine.is_checkmate(self.state):
            winner = self.state.current_player.opposite()
            return f"Checkmate! {winner.value.capitalize()} wins!"
        
        if self.engine.is_draw(self.state):
            draw_reason = self._get_draw_reason()
            return f"Draw by {draw_reason}"
        
        return "Game in progress"
    
    def _get_draw_reason(self) -> str:
        """
        Determine the reason for a draw.
        
        Returns:
            String describing the draw reason
        """
        if self.engine.is_stalemate(self.state):
            return "stalemate"
        if self.engine.is_threefold_repetition(self.state):
            return "threefold repetition"
        if self.engine.is_fifty_move_rule(self.state):
            return "fifty-move rule"
        if self.engine.is_insufficient_material(self.state):
            return "insufficient material"
        return "unknown reason"
