"""UI display component for rendering the chess board and game state."""

from typing import Optional, List, Set
from models.game_state import GameState
from models.square import Square
from models.move import Move
from models.piece import Color, PieceType
from engine.check_detector import CheckDetector


class ChessDisplay:
    """
    Handles rendering of the chess board and game information.
    
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2, 8.3
    """
    
    def __init__(self):
        """Initialize the display component."""
        self.check_detector = CheckDetector()
    
    def render_board(
        self,
        state: GameState,
        selected_square: Optional[Square] = None,
        legal_moves: Optional[List[Move]] = None,
        game_result: Optional[str] = None
    ) -> str:
        """
        Render the complete chess board with all game information.
        
        Args:
            state: Current game state
            selected_square: Currently selected square (if any)
            legal_moves: Legal moves for selected piece (if any)
            game_result: Game result message (if game is over)
        
        Returns:
            String representation of the board and game state
        
        Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2, 8.3
        """
        output = []
        
        # Add title
        output.append("=" * 50)
        output.append("CHESS GAME")
        output.append("=" * 50)
        output.append("")
        
        # Display current player's turn (Requirement 6.3)
        if game_result is None:
            turn_text = f"Current Turn: {state.current_player.value.upper()}"
            output.append(turn_text)
            
            # Display check indicator (Requirement 6.5)
            if self.check_detector.is_check(state, state.current_player):
                output.append("*** CHECK! ***")
            
            output.append("")
        
        # Get legal move destinations for highlighting
        legal_destinations = set()
        if legal_moves:
            legal_destinations = {move.to_square for move in legal_moves}
        
        # Render the board (Requirements 6.1, 6.2, 6.4)
        board_lines = self._render_board_grid(
            state,
            selected_square,
            legal_destinations
        )
        output.extend(board_lines)
        output.append("")
        
        # Display move history (Requirements 8.2, 8.3)
        if state.move_history:
            output.append("Move History:")
            output.append("-" * 50)
            history_lines = self._render_move_history(state)
            output.extend(history_lines)
            output.append("")
        
        # Display game result if game is over (Requirement 6.1)
        if game_result:
            output.append("=" * 50)
            output.append(f"GAME OVER: {game_result}")
            output.append("=" * 50)
        
        return "\n".join(output)
    
    def _render_board_grid(
        self,
        state: GameState,
        selected_square: Optional[Square],
        legal_destinations: Set[Square]
    ) -> List[str]:
        """
        Render the 8x8 chess board grid with pieces.
        
        Args:
            state: Current game state
            selected_square: Currently selected square
            legal_destinations: Set of squares that are legal move destinations
        
        Returns:
            List of strings representing board lines
        
        Requirements: 6.1, 6.2, 6.4
        """
        lines = []
        
        # Render from rank 8 to rank 1 (top to bottom)
        for rank in range(7, -1, -1):
            line_parts = [f" {rank + 1} "]
            
            for file in range(8):
                square = Square(file, rank)
                piece = state.board.get_piece(square)
                
                # Determine the display character for this square
                if piece is None:
                    # Empty square
                    char = "."
                else:
                    # Display piece with clear white/black distinction (Requirement 6.2)
                    char = self._get_piece_symbol(piece)
                
                # Add highlighting for selected square and legal moves (Requirement 6.4)
                if square == selected_square:
                    # Highlight selected piece with brackets
                    line_parts.append(f"[{char}]")
                elif square in legal_destinations:
                    # Highlight legal move destinations with asterisks
                    line_parts.append(f"*{char}*")
                else:
                    # Normal display with spacing
                    line_parts.append(f" {char} ")
            
            lines.append("".join(line_parts))
        
        # Add file labels at the bottom
        lines.append("    a  b  c  d  e  f  g  h")
        
        return lines
    
    def _get_piece_symbol(self, piece) -> str:
        """
        Get the display symbol for a piece.
        
        Uses Unicode chess symbols for clear visual distinction between
        white and black pieces.
        
        Args:
            piece: Piece to get symbol for
        
        Returns:
            Unicode character representing the piece
        
        Requirement 6.2: Clearly distinguish between white and black pieces
        """
        # Unicode chess symbols
        white_symbols = {
            PieceType.KING: "♔",
            PieceType.QUEEN: "♕",
            PieceType.ROOK: "♖",
            PieceType.BISHOP: "♗",
            PieceType.KNIGHT: "♘",
            PieceType.PAWN: "♙"
        }
        
        black_symbols = {
            PieceType.KING: "♚",
            PieceType.QUEEN: "♛",
            PieceType.ROOK: "♜",
            PieceType.BISHOP: "♝",
            PieceType.KNIGHT: "♞",
            PieceType.PAWN: "♟"
        }
        
        if piece.color == Color.WHITE:
            return white_symbols[piece.piece_type]
        else:
            return black_symbols[piece.piece_type]
    
    def _render_move_history(self, state: GameState) -> List[str]:
        """
        Render the move history in algebraic notation.
        
        Args:
            state: Current game state
        
        Returns:
            List of strings representing move history
        
        Requirements: 8.2, 8.3
        """
        lines = []
        
        # Display moves in pairs (white move, black move)
        for i in range(0, len(state.move_history), 2):
            move_number = (i // 2) + 1
            white_move = state.move_history[i]
            
            # Get algebraic notation for white's move
            white_notation = self._get_move_notation(white_move)
            
            # Check if there's a black move
            if i + 1 < len(state.move_history):
                black_move = state.move_history[i + 1]
                black_notation = self._get_move_notation(black_move)
                line = f"{move_number:3d}. {white_notation:10s} {black_notation}"
            else:
                line = f"{move_number:3d}. {white_notation}"
            
            lines.append(line)
        
        return lines
    
    def _get_move_notation(self, move: Move) -> str:
        """
        Get the algebraic notation for a move.
        
        This is a simplified version that doesn't include check/checkmate
        indicators or disambiguation, as those require game state context.
        For full notation, use ChessEngine.get_algebraic_notation().
        
        Args:
            move: Move to convert to notation
        
        Returns:
            Algebraic notation string
        
        Requirement 8.2: Display moves in standard algebraic notation
        """
        # Use the move's built-in notation method
        # Note: This won't include check/checkmate indicators without game state
        return move.to_algebraic_notation()
    
    def render_promotion_prompt(self) -> str:
        """
        Render a prompt for pawn promotion piece selection.
        
        Returns:
            String prompting user to select promotion piece
        """
        lines = [
            "",
            "=" * 50,
            "PAWN PROMOTION",
            "=" * 50,
            "Select promotion piece:",
            "  Q - Queen",
            "  R - Rook",
            "  B - Bishop",
            "  N - Knight",
            ""
        ]
        return "\n".join(lines)
    
    def render_game_mode_prompt(self) -> str:
        """
        Render a prompt for game mode selection.
        
        Returns:
            String prompting user to select game mode
        """
        lines = [
            "",
            "=" * 50,
            "CHESS GAME - MODE SELECTION",
            "=" * 50,
            "Select game mode:",
            "  1 - Single Player (vs AI)",
            "  2 - Multiplayer (Human vs Human)",
            ""
        ]
        return "\n".join(lines)
    
    def render_move_prompt(self, current_player: Color) -> str:
        """
        Render a prompt for move input.
        
        Args:
            current_player: Color of the current player
        
        Returns:
            String prompting user for move input
        """
        return f"\n{current_player.value.upper()}'s move (e.g., 'e2' to select, 'e4' to move): "
    
    def render_error(self, message: str) -> str:
        """
        Render an error message.
        
        Args:
            message: Error message to display
        
        Returns:
            Formatted error message
        """
        return f"\n*** ERROR: {message} ***\n"
    
    def render_info(self, message: str) -> str:
        """
        Render an informational message.
        
        Args:
            message: Info message to display
        
        Returns:
            Formatted info message
        """
        return f"\n{message}\n"


def render_board(
    state: GameState,
    selected_square: Optional[Square] = None,
    legal_moves: Optional[List[Move]] = None,
    game_result: Optional[str] = None
) -> str:
    """
    Convenience function to render the chess board.
    
    Args:
        state: Current game state
        selected_square: Currently selected square (if any)
        legal_moves: Legal moves for selected piece (if any)
        game_result: Game result message (if game is over)
    
    Returns:
        String representation of the board and game state
    
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2, 8.3
    """
    display = ChessDisplay()
    return display.render_board(state, selected_square, legal_moves, game_result)
