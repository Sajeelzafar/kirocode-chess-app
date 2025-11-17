"""Comprehensive tests for algebraic notation covering all requirements."""

import pytest
from models.square import Square
from models.piece import Piece, PieceType, Color
from models.move import Move
from models.board import Board
from models.game_state import GameState
from models.castling_rights import CastlingRights
from engine.chess_engine import ChessEngine


def test_requirement_8_2_piece_notation():
    """
    Requirement 8.2: Display moves in standard algebraic notation.
    Test piece notation (K, Q, R, B, N, or empty for pawns).
    """
    # Pawn move (no piece letter)
    pawn_move = Move(
        from_square=Square.from_algebraic("e2"),
        to_square=Square.from_algebraic("e4"),
        piece=Piece(PieceType.PAWN, Color.WHITE)
    )
    assert pawn_move.to_algebraic_notation() == "e4"
    
    # Knight move
    knight_move = Move(
        from_square=Square.from_algebraic("g1"),
        to_square=Square.from_algebraic("f3"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    assert knight_move.to_algebraic_notation() == "Nf3"
    
    # Bishop move
    bishop_move = Move(
        from_square=Square.from_algebraic("f1"),
        to_square=Square.from_algebraic("c4"),
        piece=Piece(PieceType.BISHOP, Color.WHITE)
    )
    assert bishop_move.to_algebraic_notation() == "Bc4"
    
    # Rook move
    rook_move = Move(
        from_square=Square.from_algebraic("a1"),
        to_square=Square.from_algebraic("a3"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    assert rook_move.to_algebraic_notation() == "Ra3"
    
    # Queen move
    queen_move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("h5"),
        piece=Piece(PieceType.QUEEN, Color.WHITE)
    )
    assert queen_move.to_algebraic_notation() == "Qh5"
    
    # King move
    king_move = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("e2"),
        piece=Piece(PieceType.KING, Color.WHITE)
    )
    assert king_move.to_algebraic_notation() == "Ke2"


def test_requirement_8_2_castling_notation():
    """
    Requirement 8.2: Display moves in standard algebraic notation.
    Test castling notation (O-O, O-O-O).
    """
    # Kingside castling
    kingside = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("g1"),
        piece=Piece(PieceType.KING, Color.WHITE),
        is_castling=True
    )
    assert kingside.to_algebraic_notation() == "O-O"
    
    # Queenside castling
    queenside = Move(
        from_square=Square.from_algebraic("e8"),
        to_square=Square.from_algebraic("c8"),
        piece=Piece(PieceType.KING, Color.BLACK),
        is_castling=True
    )
    assert queenside.to_algebraic_notation() == "O-O-O"


def test_requirement_8_2_promotion_notation():
    """
    Requirement 8.2: Display moves in standard algebraic notation.
    Test pawn promotion notation (=Q, =R, =B, =N).
    """
    # Promotion to queen
    queen_promo = Move(
        from_square=Square.from_algebraic("e7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.QUEEN
    )
    assert queen_promo.to_algebraic_notation() == "e8=Q"
    
    # Promotion to rook
    rook_promo = Move(
        from_square=Square.from_algebraic("a7"),
        to_square=Square.from_algebraic("a8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.ROOK
    )
    assert rook_promo.to_algebraic_notation() == "a8=R"
    
    # Promotion to bishop
    bishop_promo = Move(
        from_square=Square.from_algebraic("h7"),
        to_square=Square.from_algebraic("h8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.BISHOP
    )
    assert bishop_promo.to_algebraic_notation() == "h8=B"
    
    # Promotion to knight
    knight_promo = Move(
        from_square=Square.from_algebraic("c7"),
        to_square=Square.from_algebraic("c8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        promotion_piece=PieceType.KNIGHT
    )
    assert knight_promo.to_algebraic_notation() == "c8=N"


def test_requirement_8_2_disambiguation():
    """
    Requirement 8.2: Display moves in standard algebraic notation.
    Test disambiguation when multiple pieces can move to same square.
    """
    # Disambiguation by file
    rook_file = Move(
        from_square=Square.from_algebraic("a1"),
        to_square=Square.from_algebraic("d1"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    assert rook_file.to_algebraic_notation(disambiguate_file=True) == "Rad1"
    
    # Disambiguation by rank
    rook_rank = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("d4"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    assert rook_rank.to_algebraic_notation(disambiguate_rank=True) == "R1d4"
    
    # Disambiguation by both file and rank
    knight_both = Move(
        from_square=Square.from_algebraic("a1"),
        to_square=Square.from_algebraic("c3"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE)
    )
    assert knight_both.to_algebraic_notation(disambiguate_file=True, disambiguate_rank=True) == "Na1c3"


def test_requirement_8_3_chronological_order():
    """
    Requirement 8.3: Display moves in chronological order.
    Test that move history maintains order.
    """
    engine = ChessEngine()
    state = GameState.new_game()
    
    # Make a sequence of moves
    moves = [
        Move(Square.from_algebraic("e2"), Square.from_algebraic("e4"), 
             Piece(PieceType.PAWN, Color.WHITE)),
        Move(Square.from_algebraic("e7"), Square.from_algebraic("e5"), 
             Piece(PieceType.PAWN, Color.BLACK)),
        Move(Square.from_algebraic("g1"), Square.from_algebraic("f3"), 
             Piece(PieceType.KNIGHT, Color.WHITE)),
    ]
    
    for move in moves:
        state = engine.execute_move(state, move)
    
    # Verify moves are in chronological order
    assert len(state.move_history) == 3
    assert state.move_history[0] == moves[0]
    assert state.move_history[1] == moves[1]
    assert state.move_history[2] == moves[2]


def test_requirement_8_4_capture_notation():
    """
    Requirement 8.4: Indicate captures in move notation.
    Test capture notation (x).
    """
    # Piece capture
    piece_capture = Move(
        from_square=Square.from_algebraic("f3"),
        to_square=Square.from_algebraic("e5"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    assert piece_capture.to_algebraic_notation() == "Nxe5"
    
    # Pawn capture
    pawn_capture = Move(
        from_square=Square.from_algebraic("e4"),
        to_square=Square.from_algebraic("d5"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    assert pawn_capture.to_algebraic_notation() == "exd5"
    
    # En passant capture
    en_passant = Move(
        from_square=Square.from_algebraic("e5"),
        to_square=Square.from_algebraic("d6"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        is_en_passant=True
    )
    assert en_passant.to_algebraic_notation() == "exd6"
    
    # Promotion with capture
    promo_capture = Move(
        from_square=Square.from_algebraic("d7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.ROOK, Color.BLACK),
        promotion_piece=PieceType.QUEEN
    )
    assert promo_capture.to_algebraic_notation() == "dxe8=Q"


def test_requirement_8_5_check_and_checkmate_notation():
    """
    Requirement 8.5: Indicate check and checkmate in move notation.
    Test check (+) and checkmate (#) notation.
    """
    # Check notation
    check_move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("h5"),
        piece=Piece(PieceType.QUEEN, Color.WHITE)
    )
    assert check_move.to_algebraic_notation(is_check=True) == "Qh5+"
    
    # Checkmate notation
    checkmate_move = Move(
        from_square=Square.from_algebraic("d1"),
        to_square=Square.from_algebraic("h5"),
        piece=Piece(PieceType.QUEEN, Color.WHITE)
    )
    assert checkmate_move.to_algebraic_notation(is_checkmate=True) == "Qh5#"
    
    # Castling with check
    castling_check = Move(
        from_square=Square.from_algebraic("e1"),
        to_square=Square.from_algebraic("g1"),
        piece=Piece(PieceType.KING, Color.WHITE),
        is_castling=True
    )
    assert castling_check.to_algebraic_notation(is_check=True) == "O-O+"
    
    # Capture with checkmate
    capture_checkmate = Move(
        from_square=Square.from_algebraic("f3"),
        to_square=Square.from_algebraic("e5"),
        piece=Piece(PieceType.KNIGHT, Color.WHITE),
        captured_piece=Piece(PieceType.PAWN, Color.BLACK)
    )
    assert capture_checkmate.to_algebraic_notation(is_checkmate=True) == "Nxe5#"


def test_engine_disambiguation_detection():
    """Test that the engine correctly detects when disambiguation is needed."""
    engine = ChessEngine()
    
    # Create a position where two rooks can move to the same square
    # Place rooks on a4 and h4, both can move to d4
    board = Board()
    board.set_piece(Square.from_algebraic("a4"), Piece(PieceType.ROOK, Color.WHITE))
    board.set_piece(Square.from_algebraic("h4"), Piece(PieceType.ROOK, Color.WHITE))
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    state = GameState(
        board=board,
        current_player=Color.WHITE,
        castling_rights=CastlingRights(False, False, False, False),
        en_passant_target=None,
        halfmove_clock=0,
        fullmove_number=1
    )
    
    # Move rook from a4 to d4 (should be disambiguated as Rad4)
    move = Move(
        from_square=Square.from_algebraic("a4"),
        to_square=Square.from_algebraic("d4"),
        piece=Piece(PieceType.ROOK, Color.WHITE)
    )
    
    notation = engine.get_algebraic_notation(state, move)
    assert notation == "Rad4"


def test_all_requirements_together():
    """Test a complex move that combines multiple notation features."""
    # Pawn capture with promotion to queen resulting in checkmate
    complex_move = Move(
        from_square=Square.from_algebraic("d7"),
        to_square=Square.from_algebraic("e8"),
        piece=Piece(PieceType.PAWN, Color.WHITE),
        captured_piece=Piece(PieceType.ROOK, Color.BLACK),
        promotion_piece=PieceType.QUEEN
    )
    
    notation = complex_move.to_algebraic_notation(is_checkmate=True)
    assert notation == "dxe8=Q#"
    
    # This demonstrates:
    # - Pawn capture (d file indicated)
    # - Capture notation (x)
    # - Promotion notation (=Q)
    # - Checkmate notation (#)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
