"""Basic tests to verify core data models work correctly."""

from models import Square, Piece, PieceType, Color, Move, CastlingRights


def test_square_algebraic_conversion():
    """Test Square algebraic notation conversion."""
    # Test creating from algebraic notation
    square = Square.from_algebraic("e4")
    assert square.file == 4
    assert square.rank == 3
    
    # Test converting to algebraic notation
    assert square.to_algebraic() == "e4"
    
    # Test round trip
    for notation in ["a1", "h8", "d4", "e5"]:
        square = Square.from_algebraic(notation)
        assert square.to_algebraic() == notation
    
    print("✓ Square algebraic notation tests passed")


def test_piece_creation():
    """Test Piece creation and properties."""
    white_pawn = Piece(PieceType.PAWN, Color.WHITE)
    assert white_pawn.piece_type == PieceType.PAWN
    assert white_pawn.color == Color.WHITE
    assert white_pawn.to_symbol() == 'P'
    
    black_knight = Piece(PieceType.KNIGHT, Color.BLACK)
    assert black_knight.to_symbol() == 'n'
    
    print("✓ Piece creation tests passed")


def test_move_creation():
    """Test Move creation."""
    from_sq = Square.from_algebraic("e2")
    to_sq = Square.from_algebraic("e4")
    piece = Piece(PieceType.PAWN, Color.WHITE)
    
    move = Move(from_sq, to_sq, piece)
    assert move.from_square == from_sq
    assert move.to_square == to_sq
    assert move.piece == piece
    assert move.captured_piece is None
    assert not move.is_castling
    assert not move.is_en_passant
    
    print("✓ Move creation tests passed")


def test_castling_rights():
    """Test CastlingRights initialization and operations."""
    rights = CastlingRights()
    assert rights.white_kingside
    assert rights.white_queenside
    assert rights.black_kingside
    assert rights.black_queenside
    
    # Test revoking for king move
    rights.revoke_for_piece(PieceType.KING, Color.WHITE, Square.from_algebraic("e1"))
    assert not rights.white_kingside
    assert not rights.white_queenside
    assert rights.black_kingside
    assert rights.black_queenside
    
    # Test copy
    rights_copy = rights.copy()
    assert rights_copy == rights
    
    print("✓ Castling rights tests passed")


def test_color_opposite():
    """Test Color.opposite() method."""
    assert Color.WHITE.opposite() == Color.BLACK
    assert Color.BLACK.opposite() == Color.WHITE
    
    print("✓ Color opposite tests passed")


if __name__ == "__main__":
    test_square_algebraic_conversion()
    test_piece_creation()
    test_move_creation()
    test_castling_rights()
    test_color_opposite()
    print("\n✅ All basic model tests passed!")
