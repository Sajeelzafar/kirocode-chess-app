"""Tests for GameState component."""

from models import GameState, GameMode, Color, Board, CastlingRights, Square, Piece, PieceType


def test_new_game_initialization():
    """Test that a new game is initialized correctly."""
    # Test multiplayer mode
    state = GameState.new_game(GameMode.MULTIPLAYER)
    
    # Verify game mode
    assert state.game_mode == GameMode.MULTIPLAYER
    
    # Verify current player is white (Requirement 1.4)
    assert state.current_player == Color.WHITE
    
    # Verify all castling rights are enabled (Requirement 1.5)
    assert state.castling_rights.white_kingside == True
    assert state.castling_rights.white_queenside == True
    assert state.castling_rights.black_kingside == True
    assert state.castling_rights.black_queenside == True
    
    # Verify initial counters
    assert state.halfmove_clock == 0
    assert state.fullmove_number == 1
    
    # Verify no en passant target
    assert state.en_passant_target is None
    
    # Verify move history is empty
    assert len(state.move_history) == 0
    
    # Verify position history has initial position
    assert len(state.position_history) == 1
    
    # Verify board has standard starting position (Requirement 1.3)
    # Check white pieces on rank 1
    assert state.board.get_piece(Square.from_algebraic('a1')).piece_type == PieceType.ROOK
    assert state.board.get_piece(Square.from_algebraic('b1')).piece_type == PieceType.KNIGHT
    assert state.board.get_piece(Square.from_algebraic('c1')).piece_type == PieceType.BISHOP
    assert state.board.get_piece(Square.from_algebraic('d1')).piece_type == PieceType.QUEEN
    assert state.board.get_piece(Square.from_algebraic('e1')).piece_type == PieceType.KING
    assert state.board.get_piece(Square.from_algebraic('f1')).piece_type == PieceType.BISHOP
    assert state.board.get_piece(Square.from_algebraic('g1')).piece_type == PieceType.KNIGHT
    assert state.board.get_piece(Square.from_algebraic('h1')).piece_type == PieceType.ROOK
    
    # Check white pawns on rank 2
    for file in 'abcdefgh':
        square = Square.from_algebraic(f'{file}2')
        piece = state.board.get_piece(square)
        assert piece.piece_type == PieceType.PAWN
        assert piece.color == Color.WHITE
    
    # Check black pawns on rank 7
    for file in 'abcdefgh':
        square = Square.from_algebraic(f'{file}7')
        piece = state.board.get_piece(square)
        assert piece.piece_type == PieceType.PAWN
        assert piece.color == Color.BLACK
    
    # Check black pieces on rank 8
    assert state.board.get_piece(Square.from_algebraic('a8')).piece_type == PieceType.ROOK
    assert state.board.get_piece(Square.from_algebraic('b8')).piece_type == PieceType.KNIGHT
    assert state.board.get_piece(Square.from_algebraic('c8')).piece_type == PieceType.BISHOP
    assert state.board.get_piece(Square.from_algebraic('d8')).piece_type == PieceType.QUEEN
    assert state.board.get_piece(Square.from_algebraic('e8')).piece_type == PieceType.KING
    assert state.board.get_piece(Square.from_algebraic('f8')).piece_type == PieceType.BISHOP
    assert state.board.get_piece(Square.from_algebraic('g8')).piece_type == PieceType.KNIGHT
    assert state.board.get_piece(Square.from_algebraic('h8')).piece_type == PieceType.ROOK
    
    print("✓ New game initialization test passed")


def test_single_player_mode():
    """Test that single-player mode is initialized correctly."""
    state = GameState.new_game(GameMode.SINGLE_PLAYER)
    
    # Verify game mode (Requirement 1.1)
    assert state.game_mode == GameMode.SINGLE_PLAYER
    
    # Verify other initialization is the same
    assert state.current_player == Color.WHITE
    assert state.castling_rights.white_kingside == True
    
    print("✓ Single-player mode initialization test passed")


def test_game_state_copy():
    """Test that game state can be copied correctly."""
    original = GameState.new_game(GameMode.MULTIPLAYER)
    
    # Make some modifications to the original
    original.halfmove_clock = 5
    original.fullmove_number = 3
    original.en_passant_target = Square.from_algebraic('e3')
    
    # Create a copy
    copy = original.copy()
    
    # Verify copy has same values
    assert copy.current_player == original.current_player
    assert copy.halfmove_clock == original.halfmove_clock
    assert copy.fullmove_number == original.fullmove_number
    assert copy.en_passant_target == original.en_passant_target
    assert copy.game_mode == original.game_mode
    
    # Verify castling rights are copied
    assert copy.castling_rights.white_kingside == original.castling_rights.white_kingside
    
    # Verify it's a deep copy - modifying copy doesn't affect original
    copy.halfmove_clock = 10
    assert original.halfmove_clock == 5
    
    # Verify board is deep copied
    copy.board.remove_piece(Square.from_algebraic('e2'))
    assert original.board.get_piece(Square.from_algebraic('e2')) is not None
    
    print("✓ Game state copy test passed")


def test_position_hashing():
    """Test that position hashing works for threefold repetition detection."""
    state1 = GameState.new_game(GameMode.MULTIPLAYER)
    state2 = GameState.new_game(GameMode.MULTIPLAYER)
    
    # Same position should have same hash
    hash1 = state1.compute_position_hash()
    hash2 = state2.compute_position_hash()
    assert hash1 == hash2
    
    # Different positions should (likely) have different hashes
    state3 = state1.copy()
    state3.board.remove_piece(Square.from_algebraic('e2'))
    hash3 = state3.compute_position_hash()
    assert hash1 != hash3
    
    # Different player to move should have different hash
    state4 = state1.copy()
    state4.current_player = Color.BLACK
    hash4 = state4.compute_position_hash()
    assert hash1 != hash4
    
    # Different castling rights should have different hash
    state5 = state1.copy()
    state5.castling_rights.white_kingside = False
    hash5 = state5.compute_position_hash()
    assert hash1 != hash5
    
    # Different en passant target should have different hash
    state6 = state1.copy()
    state6.en_passant_target = Square.from_algebraic('e3')
    hash6 = state6.compute_position_hash()
    assert hash1 != hash6
    
    print("✓ Position hashing test passed")


if __name__ == '__main__':
    test_new_game_initialization()
    test_single_player_mode()
    test_game_state_copy()
    test_position_hashing()
    print("\n✅ All GameState tests passed!")
