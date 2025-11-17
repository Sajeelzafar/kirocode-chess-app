"""Property-based tests for Square algebraic notation.

Feature: chess-game, Property: Algebraic notation round-trip
Validates: Requirements 8.2
"""

from hypothesis import given, settings, strategies as st
from models.square import Square


@given(
    file=st.integers(min_value=0, max_value=7),
    rank=st.integers(min_value=0, max_value=7)
)
@settings(max_examples=100)
def test_square_algebraic_notation_round_trip(file: int, rank: int):
    """
    Property: Algebraic notation round-trip
    
    For any valid square coordinates (file 0-7, rank 0-7),
    converting to algebraic notation and back should preserve the original square.
    
    Feature: chess-game, Property: Algebraic notation round-trip
    Validates: Requirements 8.2
    """
    # Create a square with the given coordinates
    original_square = Square(file, rank)
    
    # Convert to algebraic notation
    algebraic = original_square.to_algebraic()
    
    # Convert back from algebraic notation
    reconstructed_square = Square.from_algebraic(algebraic)
    print(f"Testing: file={file}, rank={rank}")
    print("Reconstructed Square", reconstructed_square)
    print("Original Square", original_square)
    print("Asserted condition", reconstructed_square == original_square)
    
    # The reconstructed square should equal the original
    assert reconstructed_square == original_square, (
        f"Round-trip failed: Square({file}, {rank}) -> '{algebraic}' -> "
        f"Square({reconstructed_square.file}, {reconstructed_square.rank})"
    )
    
    # Also verify the individual components
    assert reconstructed_square.file == file, (
        f"File mismatch: expected {file}, got {reconstructed_square.file}"
    )
    assert reconstructed_square.rank == rank, (
        f"Rank mismatch: expected {rank}, got {reconstructed_square.rank}"
    )


if __name__ == "__main__":
    # Run the property test
    print("HELLO")
    test_square_algebraic_notation_round_trip()
    print("✅ Square algebraic notation round-trip property test passed!")
