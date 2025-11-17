"""Move generation for chess pieces."""

from typing import List
from models.game_state import GameState
from models.move import Move
from models.square import Square
from models.piece import Piece, PieceType, Color


class MoveGenerator:
    """
    Generates pseudo-legal moves for chess pieces.
    
    Pseudo-legal moves follow piece movement rules but may leave the king in check.
    Full validation (ensuring moves don't leave king in check) is handled separately.
    """
    
    def generate_pseudo_legal_moves(self, state: GameState, color: Color) -> List[Move]:
        """
        Generate all pseudo-legal moves for a given color.
        
        Args:
            state: Current game state
            color: Color to generate moves for
        
        Returns:
            List of all pseudo-legal moves
        """
        moves = []
        pieces = state.board.get_all_pieces(color)
        
        for square, piece in pieces.items():
            moves.extend(self.generate_piece_moves(state, square))
        
        return moves
    
    def generate_piece_moves(self, state: GameState, square: Square) -> List[Move]:
        """
        Generate all pseudo-legal moves for the piece at the given square.
        
        Args:
            state: Current game state
            square: Square containing the piece
        
        Returns:
            List of pseudo-legal moves for that piece
        """
        piece = state.board.get_piece(square)
        if piece is None:
            return []
        
        # Dispatch to piece-specific generation method
        if piece.piece_type == PieceType.PAWN:
            return self._generate_pawn_moves(state, square, piece)
        elif piece.piece_type == PieceType.KNIGHT:
            return self._generate_knight_moves(state, square, piece)
        elif piece.piece_type == PieceType.BISHOP:
            return self._generate_bishop_moves(state, square, piece)
        elif piece.piece_type == PieceType.ROOK:
            return self._generate_rook_moves(state, square, piece)
        elif piece.piece_type == PieceType.QUEEN:
            return self._generate_queen_moves(state, square, piece)
        elif piece.piece_type == PieceType.KING:
            return self._generate_king_moves(state, square, piece)
        
        return []
    
    def _generate_pawn_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal pawn moves.
        
        Pawns can:
        - Move forward one square if empty
        - Move forward two squares from starting position if both squares empty
        - Capture diagonally forward
        - Capture en passant
        """
        moves = []
        direction = 1 if piece.color == Color.WHITE else -1
        start_rank = 1 if piece.color == Color.WHITE else 6
        
        # Forward one square
        forward_rank = square.rank + direction
        if 0 <= forward_rank <= 7:
            forward_square = Square(square.file, forward_rank)
            if state.board.get_piece(forward_square) is None:
                # Check for promotion
                if forward_square.rank == 7 or forward_square.rank == 0:
                    # Generate promotion moves for all piece types
                    for promo_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                        moves.append(Move(
                            from_square=square,
                            to_square=forward_square,
                            piece=piece,
                            promotion_piece=promo_type
                        ))
                else:
                    moves.append(Move(
                        from_square=square,
                        to_square=forward_square,
                        piece=piece
                    ))
                
                    # Forward two squares from starting position
                    if square.rank == start_rank:
                        two_forward_square = Square(square.file, square.rank + 2 * direction)
                        if state.board.get_piece(two_forward_square) is None:
                            moves.append(Move(
                                from_square=square,
                                to_square=two_forward_square,
                                piece=piece
                            ))
        
        # Diagonal captures
        for file_offset in [-1, 1]:
            capture_file = square.file + file_offset
            capture_rank = square.rank + direction
            if 0 <= capture_file <= 7 and 0 <= capture_rank <= 7:
                capture_square = Square(capture_file, capture_rank)
                target_piece = state.board.get_piece(capture_square)
                
                # Regular capture
                if target_piece is not None and target_piece.color != piece.color:
                    # Check for promotion
                    if capture_square.rank == 7 or capture_square.rank == 0:
                        for promo_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                            moves.append(Move(
                                from_square=square,
                                to_square=capture_square,
                                piece=piece,
                                captured_piece=target_piece,
                                promotion_piece=promo_type
                            ))
                    else:
                        moves.append(Move(
                            from_square=square,
                            to_square=capture_square,
                            piece=piece,
                            captured_piece=target_piece
                        ))
                
                # En passant capture (target square is empty for en passant)
                elif state.en_passant_target is not None and capture_square == state.en_passant_target:
                    # The captured pawn is on the same rank as the capturing pawn
                    captured_pawn_square = Square(capture_square.file, square.rank)
                    captured_pawn = state.board.get_piece(captured_pawn_square)
                    moves.append(Move(
                        from_square=square,
                        to_square=capture_square,
                        piece=piece,
                        captured_piece=captured_pawn,
                        is_en_passant=True
                    ))
        
        return moves
    
    def _generate_knight_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal knight moves.
        
        Knights move in an L-shape: 2 squares in one direction, 1 square perpendicular.
        """
        moves = []
        
        # All possible knight move offsets
        knight_offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for file_offset, rank_offset in knight_offsets:
            target_file = square.file + file_offset
            target_rank = square.rank + rank_offset
            
            # Check if target is within board bounds
            if 0 <= target_file <= 7 and 0 <= target_rank <= 7:
                target_square = Square(target_file, target_rank)
                target_piece = state.board.get_piece(target_square)
                
                # Can move to empty square or capture opponent's piece
                if target_piece is None or target_piece.color != piece.color:
                    moves.append(Move(
                        from_square=square,
                        to_square=target_square,
                        piece=piece,
                        captured_piece=target_piece
                    ))
        
        return moves
    
    def _generate_bishop_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal bishop moves.
        
        Bishops move diagonally any number of squares.
        """
        moves = []
        
        # Four diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for file_dir, rank_dir in directions:
            moves.extend(self._generate_sliding_moves(state, square, piece, file_dir, rank_dir))
        
        return moves
    
    def _generate_rook_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal rook moves.
        
        Rooks move horizontally or vertically any number of squares.
        """
        moves = []
        
        # Four orthogonal directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for file_dir, rank_dir in directions:
            moves.extend(self._generate_sliding_moves(state, square, piece, file_dir, rank_dir))
        
        return moves
    
    def _generate_queen_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal queen moves.
        
        Queens move like both bishops and rooks (diagonally and orthogonally).
        """
        moves = []
        
        # All eight directions (diagonal + orthogonal)
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Orthogonal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for file_dir, rank_dir in directions:
            moves.extend(self._generate_sliding_moves(state, square, piece, file_dir, rank_dir))
        
        return moves

    def _generate_king_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate pseudo-legal king moves.
        
        Kings can:
        - Move one square in any direction
        - Castle kingside or queenside (if conditions are met)
        """
        moves = []
        
        # One square in any direction
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Orthogonal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for file_dir, rank_dir in directions:
            target_file = square.file + file_dir
            target_rank = square.rank + rank_dir
            if 0 <= target_file <= 7 and 0 <= target_rank <= 7:
                target_square = Square(target_file, target_rank)
                target_piece = state.board.get_piece(target_square)
                
                # Can move to empty square or capture opponent's piece
                if target_piece is None or target_piece.color != piece.color:
                    moves.append(Move(
                        from_square=square,
                        to_square=target_square,
                        piece=piece,
                        captured_piece=target_piece
                    ))
        
        # Castling
        moves.extend(self._generate_castling_moves(state, square, piece))
        
        return moves
    
    def _generate_castling_moves(self, state: GameState, square: Square, piece: Piece) -> List[Move]:
        """
        Generate castling moves for the king.
        
        Castling requirements (checked here):
        - King and rook haven't moved (castling rights)
        - No pieces between king and rook
        
        Additional requirements (checked during validation):
        - King not in check
        - King doesn't move through check
        - King doesn't end in check
        """
        moves = []
        
        if piece.color == Color.WHITE:
            king_start_square = Square(4, 0)  # e1
            
            # Kingside castling
            if state.castling_rights.white_kingside and square == king_start_square:
                # Check if squares between king and rook are empty
                if (state.board.get_piece(Square(5, 0)) is None and
                    state.board.get_piece(Square(6, 0)) is None):
                    # Check if rook is in correct position
                    rook = state.board.get_piece(Square(7, 0))
                    if rook is not None and rook.piece_type == PieceType.ROOK and rook.color == Color.WHITE:
                        moves.append(Move(
                            from_square=square,
                            to_square=Square(6, 0),  # g1
                            piece=piece,
                            is_castling=True
                        ))
            
            # Queenside castling
            if state.castling_rights.white_queenside and square == king_start_square:
                # Check if squares between king and rook are empty
                if (state.board.get_piece(Square(1, 0)) is None and
                    state.board.get_piece(Square(2, 0)) is None and
                    state.board.get_piece(Square(3, 0)) is None):
                    # Check if rook is in correct position
                    rook = state.board.get_piece(Square(0, 0))
                    if rook is not None and rook.piece_type == PieceType.ROOK and rook.color == Color.WHITE:
                        moves.append(Move(
                            from_square=square,
                            to_square=Square(2, 0),  # c1
                            piece=piece,
                            is_castling=True
                        ))
        
        else:  # Black
            king_start_square = Square(4, 7)  # e8
            
            # Kingside castling
            if state.castling_rights.black_kingside and square == king_start_square:
                # Check if squares between king and rook are empty
                if (state.board.get_piece(Square(5, 7)) is None and
                    state.board.get_piece(Square(6, 7)) is None):
                    # Check if rook is in correct position
                    rook = state.board.get_piece(Square(7, 7))
                    if rook is not None and rook.piece_type == PieceType.ROOK and rook.color == Color.BLACK:
                        moves.append(Move(
                            from_square=square,
                            to_square=Square(6, 7),  # g8
                            piece=piece,
                            is_castling=True
                        ))
            
            # Queenside castling
            if state.castling_rights.black_queenside and square == king_start_square:
                # Check if squares between king and rook are empty
                if (state.board.get_piece(Square(1, 7)) is None and
                    state.board.get_piece(Square(2, 7)) is None and
                    state.board.get_piece(Square(3, 7)) is None):
                    # Check if rook is in correct position
                    rook = state.board.get_piece(Square(0, 7))
                    if rook is not None and rook.piece_type == PieceType.ROOK and rook.color == Color.BLACK:
                        moves.append(Move(
                            from_square=square,
                            to_square=Square(2, 7),  # c8
                            piece=piece,
                            is_castling=True
                        ))
        
        return moves
    
    def _generate_sliding_moves(
        self,
        state: GameState,
        square: Square,
        piece: Piece,
        file_dir: int,
        rank_dir: int
    ) -> List[Move]:
        """
        Generate moves for sliding pieces (bishop, rook, queen) in one direction.
        
        Args:
            state: Current game state
            square: Starting square
            piece: Piece being moved
            file_dir: Direction to move in file (-1, 0, or 1)
            rank_dir: Direction to move in rank (-1, 0, or 1)
        
        Returns:
            List of moves in the given direction
        """
        moves = []
        current_file = square.file + file_dir
        current_rank = square.rank + rank_dir
        
        while True:
            # Stop if we've gone off the board
            if not (0 <= current_file <= 7 and 0 <= current_rank <= 7):
                break
            
            target_square = Square(current_file, current_rank)
            
            target_piece = state.board.get_piece(target_square)
            
            if target_piece is None:
                # Empty square - can move here and continue
                moves.append(Move(
                    from_square=square,
                    to_square=target_square,
                    piece=piece
                ))
            elif target_piece.color != piece.color:
                # Opponent's piece - can capture but can't continue
                moves.append(Move(
                    from_square=square,
                    to_square=target_square,
                    piece=piece,
                    captured_piece=target_piece
                ))
                break
            else:
                # Own piece - can't move here
                break
            
            current_file += file_dir
            current_rank += rank_dir
        
        return moves
    
    def _is_valid_square(self, square: Square) -> bool:
        """
        Check if a square is within the board boundaries.
        
        Args:
            square: Square to check
        
        Returns:
            True if square is valid (0-7 for both file and rank)
        """
        try:
            # Square constructor validates bounds
            return 0 <= square.file <= 7 and 0 <= square.rank <= 7
        except (ValueError, AttributeError):
            return False
