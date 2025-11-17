"""
Unit tests for the main game loop functions.

Tests the helper functions used in the main game loop.
"""

import pytest
from main import parse_square_input, get_game_mode, get_promotion_choice
from models.square import Square
from models.piece import PieceType


def test_parse_square_input_valid():
    """Test parsing valid square inputs."""
    # Test lowercase
    square = parse_square_input("e4")
    assert square.file == 4
    assert square.rank == 3
    assert square.to_algebraic() == "e4"
    
    # Test uppercase (should be converted to lowercase)
    square = parse_square_input("A1")
    assert square.file == 0
    assert square.rank == 0
    assert square.to_algebraic() == "a1"
    
    # Test with whitespace
    square = parse_square_input("  h8  ")
    assert square.file == 7
    assert square.rank == 7
    assert square.to_algebraic() == "h8"


def test_parse_square_input_invalid():
    """Test parsing invalid square inputs."""
    # Too short
    with pytest.raises(ValueError, match="exactly 2 characters"):
        parse_square_input("e")
    
    # Too long
    with pytest.raises(ValueError, match="exactly 2 characters"):
        parse_square_input("e44")
    
    # Invalid file
    with pytest.raises(ValueError):
        parse_square_input("i4")
    
    # Invalid rank
    with pytest.raises(ValueError):
        parse_square_input("e9")


def test_main_module_imports():
    """Test that the main module can be imported without errors."""
    import main
    assert hasattr(main, 'main')
    assert hasattr(main, 'get_game_mode')
    assert hasattr(main, 'get_promotion_choice')
    assert hasattr(main, 'parse_square_input')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
