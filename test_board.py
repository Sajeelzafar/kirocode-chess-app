"""Test the Board component implementation."""

from models import Board, Piece, PieceType, Color, Square


def test_board_initialization():
    """Test that a new board is empty."""
    board = Board()
    for rank in range(8):
        for file in range(8):
            square = Square(file, rank)
            assert board.get_piece(square) is None, f"Square {square} should be empty"
    print("✓ Board initialization test passed")


def test_set_and_get_piece():
    """Test setting and getting pieces."""
    board = Board()
    square = Square.from_algebraic("e4")
    piece = Piece(PieceType.PAWN, Color.WHITE)
    
    board.set_piece(square, piece)
    retrieved = board.get_piece(square)
    
    assert retrieved is not None, "Piece should be present"
    assert retrieved.piece_type == PieceType.PAWN, "Should be a pawn"
    assert retrieved.color == Color.WHITE, "Should be white"
    print("✓ Set and get piece test passed")


def test_remove_piece():
    """Test removing a piece."""
    board = Board()
    square = Square.from_algebraic("d5")
    piece = Piece(PieceType.KNIGHT, Color.BLACK)
    
    board.set_piece(square, piece)
    assert board.get_piece(square) is not None, "Piece should be present"
    
    board.remove_piece(square)
    assert board.get_piece(square) is None, "Piece should be removed"
    print("✓ Remove piece test passed")


def test_get_all_pieces():
    """Test getting all pieces of a color."""
    board = Board()
    
    # Add some white pieces
    board.set_piece(Square.from_algebraic("a1"), Piece(PieceType.ROOK, Color.WHITE))
    board.set_piece(Square.from_algebraic("e1"), Piece(PieceType.KING, Color.WHITE))
    board.set_piece(Square.from_algebraic("h1"), Piece(PieceType.ROOK, Color.WHITE))
    
    # Add some black pieces
    board.set_piece(Square.from_algebraic("a8"), Piece(PieceType.ROOK, Color.BLACK))
    board.set_piece(Square.from_algebraic("e8"), Piece(PieceType.KING, Color.BLACK))
    
    white_pieces = board.get_all_pieces(Color.WHITE)
    black_pieces = board.get_all_pieces(Color.BLACK)
    
    assert len(white_pieces) == 3, f"Should have 3 white pieces, got {len(white_pieces)}"
    assert len(black_pieces) == 2, f"Should have 2 black pieces, got {len(black_pieces)}"
    print("✓ Get all pieces test passed")


def test_board_copy():
    """Test that board copy creates an independent copy."""
    board = Board()
    square = Square.from_algebraic("c3")
    piece = Piece(PieceType.BISHOP, Color.WHITE)
    board.set_piece(square, piece)
    
    # Create a copy
    board_copy = board.copy()
    
    # Verify the copy has the same piece
    copied_piece = board_copy.get_piece(square)
    assert copied_piece is not None, "Copy should have the piece"
    assert copied_piece.piece_type == PieceType.BISHOP, "Copy should have bishop"
    assert copied_piece.color == Color.WHITE, "Copy should have white piece"
    
    # Modify the original
    board.remove_piece(square)
    
    # Verify the copy is unchanged
    copied_piece = board_copy.get_piece(square)
    assert copied_piece is not None, "Copy should still have the piece after original is modified"
    
    # Verify original is changed
    assert board.get_piece(square) is None, "Original should have piece removed"
    print("✓ Board copy test passed")


def test_standard_starting_position():
    """Test that standard starting position is set up correctly."""
    board = Board()
    board.setup_standard_position()
    
    # Check white pieces on rank 1
    assert board.get_piece(Square.from_algebraic("a1")).piece_type == PieceType.ROOK
    assert board.get_piece(Square.from_algebraic("b1")).piece_type == PieceType.KNIGHT
    assert board.get_piece(Square.from_algebraic("c1")).piece_type == PieceType.BISHOP
    assert board.get_piece(Square.from_algebraic("d1")).piece_type == PieceType.QUEEN
    assert board.get_piece(Square.from_algebraic("e1")).piece_type == PieceType.KING
    assert board.get_piece(Square.from_algebraic("f1")).piece_type == PieceType.BISHOP
    assert board.get_piece(Square.from_algebraic("g1")).piece_type == PieceType.KNIGHT
    assert board.get_piece(Square.from_algebraic("h1")).piece_type == PieceType.ROOK
    
    # Check all white pieces are white
    for file_char in 'abcdefgh':
        piece = board.get_piece(Square.from_algebraic(f"{file_char}1"))
        assert piece.color == Color.WHITE, f"Piece at {file_char}1 should be white"
    
    # Check white pawns on rank 2
    for file_char in 'abcdefgh':
        piece = board.get_piece(Square.from_algebraic(f"{file_char}2"))
        assert piece.piece_type == PieceType.PAWN, f"Should have pawn at {file_char}2"
        assert piece.color == Color.WHITE, f"Pawn at {file_char}2 should be white"
    
    # Check black pawns on rank 7
    for file_char in 'abcdefgh':
        piece = board.get_piece(Square.from_algebraic(f"{file_char}7"))
        assert piece.piece_type == PieceType.PAWN, f"Should have pawn at {file_char}7"
        assert piece.color == Color.BLACK, f"Pawn at {file_char}7 should be black"
    
    # Check black pieces on rank 8
    assert board.get_piece(Square.from_algebraic("a8")).piece_type == PieceType.ROOK
    assert board.get_piece(Square.from_algebraic("b8")).piece_type == PieceType.KNIGHT
    assert board.get_piece(Square.from_algebraic("c8")).piece_type == PieceType.BISHOP
    assert board.get_piece(Square.from_algebraic("d8")).piece_type == PieceType.QUEEN
    assert board.get_piece(Square.from_algebraic("e8")).piece_type == PieceType.KING
    assert board.get_piece(Square.from_algebraic("f8")).piece_type == PieceType.BISHOP
    assert board.get_piece(Square.from_algebraic("g8")).piece_type == PieceType.KNIGHT
    assert board.get_piece(Square.from_algebraic("h8")).piece_type == PieceType.ROOK
    
    # Check all black pieces are black
    for file_char in 'abcdefgh':
        piece = board.get_piece(Square.from_algebraic(f"{file_char}8"))
        assert piece.color == Color.BLACK, f"Piece at {file_char}8 should be black"
    
    # Check middle ranks are empty
    for rank in ['3', '4', '5', '6']:
        for file_char in 'abcdefgh':
            piece = board.get_piece(Square.from_algebraic(f"{file_char}{rank}"))
            assert piece is None, f"Square {file_char}{rank} should be empty"
    
    # Count total pieces
    white_pieces = board.get_all_pieces(Color.WHITE)
    black_pieces = board.get_all_pieces(Color.BLACK)
    assert len(white_pieces) == 16, f"Should have 16 white pieces, got {len(white_pieces)}"
    assert len(black_pieces) == 16, f"Should have 16 black pieces, got {len(black_pieces)}"
    
    print("✓ Standard starting position test passed")


if __name__ == "__main__":
    test_board_initialization()
    test_set_and_get_piece()
    test_remove_piece()
    test_get_all_pieces()
    test_board_copy()
    test_standard_starting_position()
    print("\n✅ All Board component tests passed!")
