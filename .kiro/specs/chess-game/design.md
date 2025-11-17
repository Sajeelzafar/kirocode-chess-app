# Chess Game Design Document

## Overview

This document describes the design for a chess application that supports both single-player (vs AI) and multiplayer (human vs human) modes. The system implements complete chess rules including special moves (castling, en passant, pawn promotion), game-ending conditions (checkmate, stalemate, draws), and provides an interactive interface for gameplay.

The design follows a layered architecture separating game logic, AI, and presentation concerns. The core chess engine handles rule enforcement and state management, while separate components handle AI move generation and user interface rendering.

## Architecture

The system is organized into four primary layers:

1. **Core Game Engine Layer**: Implements chess rules, move validation, and state management
2. **AI Layer**: Generates moves for the computer opponent in single-player mode
3. **Presentation Layer**: Handles board rendering and user interaction
4. **Game Controller Layer**: Orchestrates game flow and coordinates between layers

### Design Rationale

- **Separation of Concerns**: The layered architecture ensures that chess rules, AI logic, and UI rendering are independent, making the system maintainable and testable
- **Stateless Move Validation**: Move validation functions operate on immutable game state, enabling easy testing and preventing side effects
- **Pluggable AI**: The AI component is isolated, allowing for future improvements or alternative AI implementations without affecting core game logic

## Components and Interfaces

### Game State Component

Represents the complete state of a chess game at any point in time.

**Key Fields:**
- board: 8x8 grid of pieces
- current_player: WHITE or BLACK
- castling_rights: Tracks available castling options
- en_passant_target: Square where en passant is possible
- halfmove_clock: Moves since last pawn move or capture
- fullmove_number: Increments after black's move
- move_history: Complete game history
- position_history: For threefold repetition detection

### Board Component

Manages the 8x8 chess board and piece positions.

**Key Operations:**
- get_piece(square): Returns piece at given square
- set_piece(square, piece): Places piece at square
- remove_piece(square): Removes piece from square
- get_all_pieces(color): Returns all pieces for a color
- copy(): Creates deep copy of board

### Piece Component

Represents individual chess pieces with their type and color.

**Piece Types:** PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
**Colors:** WHITE, BLACK

### Move Component

Represents a chess move with all necessary information.

**Key Fields:**
- from_square: Starting position
- to_square: Destination position
- piece: Piece being moved
- captured_piece: Piece captured (if any)
- promotion_piece: Piece type for pawn promotion (if applicable)
- is_castling: Flag for castling moves
- is_en_passant: Flag for en passant captures

**Key Operations:**
- to_algebraic_notation(): Converts move to standard notation


### Chess Engine Component

Core component that enforces rules and manages game state.

**Key Operations:**
- initialize_game(mode): Creates new game in single-player or multiplayer mode
- get_legal_moves(state, square): Returns all legal moves for piece at square
- is_legal_move(state, move): Validates if a move is legal
- execute_move(state, move): Applies move and returns new state
- is_check(state, color): Determines if king is in check
- is_checkmate(state): Determines if current player is checkmated
- is_stalemate(state): Determines if game is stalemated
- is_draw(state): Checks for draw conditions (threefold repetition, fifty-move rule, insufficient material)

### Move Generator Component

Generates all possible moves for pieces.

**Key Operations:**
- generate_pseudo_legal_moves(state, color): Generates all moves without checking if they leave king in check
- generate_piece_moves(state, square): Generates moves for specific piece

### Move Validator Component

Validates moves according to chess rules.

**Key Operations:**
- validate_move(state, move): Checks if move follows all rules
- would_leave_in_check(state, move): Checks if move leaves own king in check
- validate_castling(state, move): Validates castling requirements
- validate_en_passant(state, move): Validates en passant capture

### AI Opponent Component

Generates moves for the computer player.

**Key Operations:**
- select_move(state): Chooses best move for current position
- evaluate_position(state): Assigns numeric score to position
- find_checkmate_in_one(state): Detects immediate checkmate opportunities

**AI Strategy:**
- Material evaluation: Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9
- Prioritizes checkmate in one move
- Avoids moves that lose material without compensation
- Selects from all legal moves within reasonable time

### Game Controller Component

Orchestrates game flow and user interactions.

**Key Operations:**
- start_new_game(mode): Initializes new game
- handle_square_selection(square): Processes player selecting a square
- handle_move_attempt(from_square, to_square): Processes move attempt
- handle_promotion_choice(piece_type): Processes pawn promotion selection
- get_current_state(): Returns current game state

## Data Models

### Square Representation

Squares are represented using algebraic notation (a1-h8) with internal coordinate conversion.

**Fields:**
- file: 0-7 representing columns a-h
- rank: 0-7 representing rows 1-8

**Operations:**
- from_algebraic(notation): Converts "e4" to coordinates
- to_algebraic(): Converts coordinates to "e4"

### Castling Rights

Tracks which castling moves are still available for each player.

**Fields:**
- white_kingside: Can white castle kingside
- white_queenside: Can white castle queenside
- black_kingside: Can black castle kingside
- black_queenside: Can black castle queenside

**Operations:**
- revoke_for_piece(piece, square): Removes castling rights when king or rook moves

### Game Mode

Enumeration for game types:
- SINGLE_PLAYER: Human vs AI
- MULTIPLAYER: Human vs Human


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Game Initialization Properties

Property 1: Standard starting position
*For any* newly initialized game, the board should contain all 32 pieces in their standard chess starting positions (pawns on ranks 2 and 7, pieces on ranks 1 and 8 in correct order)
**Validates: Requirements 1.3**

Property 2: White moves first
*For any* newly initialized game, the current player should be white
**Validates: Requirements 1.4**

Property 3: All castling rights enabled
*For any* newly initialized game, all four castling rights (white kingside, white queenside, black kingside, black queenside) should be enabled
**Validates: Requirements 1.5**

### Move Execution Properties

Property 4: Legal move execution updates state
*For any* game state and any legal move, executing the move should produce a new game state with the piece at the destination square
**Validates: Requirements 2.2**

Property 5: Illegal moves preserve state
*For any* game state and any illegal move attempt, the game state should remain completely unchanged
**Validates: Requirements 2.4**

Property 6: Turn alternation
*For any* game state and any legal move execution, the current player in the resulting state should be the opposite of the current player in the original state
**Validates: Requirements 2.5**

Property 7: Move history recording
*For any* game state and any executed move, the move should appear as the last entry in the move history of the resulting state
**Validates: Requirements 8.1**

### Move Validation Properties

Property 8: Piece movement rules
*For any* move, if it is legal, then it must follow the movement pattern for that piece type (e.g., bishops move diagonally, knights move in L-shape)
**Validates: Requirements 3.1**

Property 9: Cannot leave king in check
*For any* game state and any move, if executing the move would leave the current player's king in check, then the move should be rejected as illegal
**Validates: Requirements 3.2**

Property 10: Must escape check
*For any* game state where the current player is in check, all legal moves should result in a state where that player is no longer in check
**Validates: Requirements 3.3**

Property 11: Castling validation
*For any* castling move, it should only be legal if: (1) the king and rook have not previously moved, (2) no pieces are between them, (3) the king is not in check, (4) the king does not move through check, and (5) the king does not end in check
**Validates: Requirements 3.4**

Property 12: Pawn promotion
*For any* pawn move that reaches the opposite end of the board (rank 8 for white, rank 1 for black), the move should result in the pawn being replaced by a queen, rook, bishop, or knight
**Validates: Requirements 3.5**

### Game Ending Properties

Property 13: Checkmate detection
*For any* game state where a player is in check and has no legal moves, the game should be declared checkmate with the other player winning
**Validates: Requirements 4.1**

Property 14: Stalemate detection
*For any* game state where the current player has no legal moves and is not in check, the game should be declared stalemate (draw)
**Validates: Requirements 4.2**

Property 15: Threefold repetition
*For any* game where the same position (same pieces, same positions, same player to move, same castling rights, same en passant availability) occurs three times, a draw should be offered
**Validates: Requirements 4.3**

Property 16: Fifty-move rule
*For any* game state where 50 consecutive moves have occurred without any pawn move or capture, a draw should be offered
**Validates: Requirements 4.4**

Property 17: Insufficient material
*For any* game state with only kings remaining, or only kings and insufficient material to checkmate (e.g., king + bishop vs king, king + knight vs king), the game should be declared a draw
**Validates: Requirements 4.5**

### AI Behavior Properties

Property 18: AI generates legal moves
*For any* game state where it is the AI's turn, the move selected by the AI should be in the set of all legal moves for that position
**Validates: Requirements 5.1, 5.2**

Property 19: Material evaluation consistency
*For any* two game states that differ only in material count, the state with more material (using standard values: pawn=1, knight=3, bishop=3, rook=5, queen=9) should have a higher evaluation score for the player with more material
**Validates: Requirements 5.3**

Property 20: AI finds checkmate in one
*For any* game state where the AI has a move that delivers checkmate, the AI should select that move
**Validates: Requirements 5.5**

### Special Moves Properties

Property 21: Castling execution
*For any* valid castling move, executing it should move both the king and the rook to their correct castling positions (king moves 2 squares toward rook, rook moves to square king crossed)
**Validates: Requirements 7.1**

Property 22: En passant availability
*For any* pawn move of two squares forward, if an opponent pawn is on an adjacent file on the same rank, then en passant capture should be available for exactly the opponent's next move
**Validates: Requirements 7.2**

Property 23: En passant capture
*For any* en passant capture execution, the captured pawn should be removed from the board (not from the destination square, but from the square the capturing pawn passed through)
**Validates: Requirements 7.3**

Property 24: Castling rights revocation on piece move
*For any* game state where a king or rook moves, the appropriate castling rights should be permanently revoked in the resulting state
**Validates: Requirements 7.4**

Property 25: Castling rights revocation on rook capture
*For any* game state where a rook is captured, the castling rights for that rook's side should be permanently revoked in the resulting state
**Validates: Requirements 7.5**

### Display and Notation Properties

Property 26: Algebraic notation format
*For any* move in the move history, its string representation should be valid standard algebraic notation (e.g., "e4", "Nf3", "O-O", "exd5")
**Validates: Requirements 8.2**

Property 27: Move history ordering
*For any* game state with n moves in history, the moves should be ordered chronologically such that move i occurred before move i+1
**Validates: Requirements 8.3**

Property 28: Capture notation
*For any* move that captures a piece, the algebraic notation should include the capture indicator ("x")
**Validates: Requirements 8.4**

Property 29: Check and checkmate notation
*For any* move that results in check, the notation should include "+" and for any move that results in checkmate, the notation should include "#"
**Validates: Requirements 8.5**


## Error Handling

The system handles errors at multiple levels to ensure robustness:

### Input Validation Errors

**Invalid Square Selection:**
- When a player selects a square outside the board (invalid coordinates)
- When a player selects an empty square when a piece is expected
- Response: Reject selection silently, maintain current state

**Invalid Move Attempts:**
- When a player attempts to move to an invalid square
- When a player attempts an illegal move
- Response: Reject move, display error message, maintain current state

**Invalid Piece Selection:**
- When a player selects opponent's piece
- Response: Reject selection, display error message indicating wrong color

### Game State Errors

**Check Violations:**
- When a player attempts a move that leaves their king in check
- Response: Reject move, display message "Move leaves king in check"

**Missing Promotion Choice:**
- When a pawn reaches the final rank but no promotion piece is selected
- Response: Prompt user for promotion choice, block further moves until selection made

### AI Errors

**No Legal Moves Available:**
- When AI has no legal moves (should trigger stalemate/checkmate detection)
- Response: Declare game over with appropriate result

**Evaluation Errors:**
- When position evaluation encounters unexpected state
- Response: Fall back to material-only evaluation

### State Consistency Errors

**Corrupted Game State:**
- When game state becomes inconsistent (e.g., missing king)
- Response: Log error, offer to restart game

**Invalid Position:**
- When loading a saved game with invalid position
- Response: Reject load, display error message, remain in current state

### Error Recovery Strategy

- All errors preserve game state immutability
- Invalid operations never partially modify state
- User is always informed of why an action was rejected
- System remains in valid state after any error

## Testing Strategy

The chess game will employ a comprehensive testing approach combining unit tests and property-based tests to ensure correctness across all components.

### Property-Based Testing

Property-based testing will be the primary method for verifying correctness properties. We will use **Hypothesis** (for Python) or **fast-check** (for JavaScript/TypeScript) as the property-based testing library.

**Configuration:**
- Each property-based test will run a minimum of 100 iterations
- Tests will use custom generators for chess-specific data (positions, moves, pieces)
- Each property test will be tagged with a comment referencing the design document property

**Tag Format:**
```
# Feature: chess-game, Property X: [property description]
# Validates: Requirements Y.Z
```

**Property Test Coverage:**
- All 29 correctness properties defined in this document will have corresponding property-based tests
- Properties will be tested with randomly generated valid game states
- Edge cases (empty boards, endgame positions, complex positions) will be included in generators

**Custom Generators:**
- Valid game state generator (random but legal positions)
- Move generator (generates legal and illegal moves)
- Piece placement generator
- Game history generator (for testing repetition and fifty-move rule)

### Unit Testing

Unit tests will complement property-based tests by verifying specific examples and integration points.

**Unit Test Coverage:**
- Specific famous chess positions (e.g., Scholar's Mate, Fool's Mate)
- Edge cases for special moves (castling through check, en passant edge cases)
- Specific endgame scenarios (K+Q vs K checkmate, insufficient material draws)
- AI behavior on known positions
- Notation parsing and generation for specific moves

**Test Organization:**
- Tests co-located with source files using appropriate naming conventions
- Separate test suites for: game engine, move generation, move validation, AI, notation, UI

### Integration Testing

- Full game playthrough tests (from start to checkmate/stalemate)
- Mode switching tests (single-player vs multiplayer)
- Save/load game state tests (if persistence is implemented)

### Testing Priorities

1. **Critical Path:** Move validation, check detection, checkmate/stalemate detection
2. **High Priority:** Special moves (castling, en passant, promotion), AI move generation
3. **Medium Priority:** Notation generation, draw conditions, UI display
4. **Low Priority:** Performance optimization, AI strength improvements

### Test Data Strategy

- Use FEN (Forsyth-Edwards Notation) for representing test positions
- Maintain library of test positions covering various scenarios
- Use PGN (Portable Game Notation) for testing full games

## Implementation Notes

### Performance Considerations

- Move generation should be optimized as it's called frequently
- Board copying should use efficient data structures
- Position hashing for threefold repetition detection should use Zobrist hashing
- AI evaluation should have depth limits to ensure reasonable response time

### Future Enhancements

- Configurable AI difficulty levels
- Opening book for AI
- Endgame tablebase support
- Time controls and chess clocks
- Online multiplayer support
- Game save/load functionality
- Move hints and analysis
- Undo/redo functionality

### Technology Considerations

The design is language-agnostic but assumes:
- Object-oriented programming support
- Immutable data structures or deep copying capability
- Property-based testing library availability
- Standard algebraic notation parsing/generation libraries may be available

### Dependencies

- Property-based testing library (Hypothesis/fast-check)
- Unit testing framework (pytest/Jest/etc.)
- Optional: Chess notation libraries for FEN/PGN parsing
- Optional: UI framework (terminal-based or graphical)
