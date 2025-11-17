# Implementation Plan

- [x] 1. Set up project structure and core data models





  - Create directory structure for models, engine, AI, and UI components
  - Implement Square class with algebraic notation conversion
  - Implement Piece class with type and color enums
  - Implement Move class with all necessary fields
  - Implement CastlingRights class
  - _Requirements: 1.3, 1.4, 1.5, 2.2, 7.1, 7.4, 7.5_

- [x] 1.1 Write property test for Square algebraic notation






  - **Property: Algebraic notation round-trip**
  - Test that converting to algebraic and back preserves the square
  - _Requirements: 8.2_

- [x] 2. Implement Board component





  - Create Board class with 8x8 grid storage
  - Implement get_piece, set_piece, remove_piece methods
  - Implement get_all_pieces method for retrieving pieces by color
  - Implement board copy method for immutability
  - Implement standard starting position setup
  - _Requirements: 1.3, 6.1_

- [ ]* 2.1 Write property test for board operations
  - **Property 1: Standard starting position**
  - **Validates: Requirements 1.3**


- [x] 3. Implement GameState component



  - Create GameState class with all required fields
  - Implement game state initialization for new games
  - Implement position hashing for threefold repetition detection
  - Implement game state copy method
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.3_

- [ ]* 3.1 Write property tests for game initialization
  - **Property 2: White moves first**
  - **Validates: Requirements 1.4**

- [ ]* 3.2 Write property test for castling rights initialization
  - **Property 3: All castling rights enabled**
  - **Validates: Requirements 1.5**

- [x] 4. Implement move generation for each piece type





  - Implement pseudo-legal move generation for pawns (including two-square initial move)
  - Implement pseudo-legal move generation for knights
  - Implement pseudo-legal move generation for bishops
  - Implement pseudo-legal move generation for rooks
  - Implement pseudo-legal move generation for queens
  - Implement pseudo-legal move generation for kings (including castling)
  - Create MoveGenerator class that coordinates piece-specific generation
  - _Requirements: 2.1, 3.1, 7.1, 7.2_

- [ ]* 4.1 Write property test for piece movement rules
  - **Property 8: Piece movement rules**
  - **Validates: Requirements 3.1**

- [x] 5. Implement check detection





  - Implement method to determine if a square is under attack
  - Implement is_check method to detect if a king is in check
  - Implement method to find king position for a given color
  - _Requirements: 3.2, 3.3, 4.1, 6.5_

- [x] 6. Implement move validation





  - Create MoveValidator class
  - Implement validation that moves don't leave king in check
  - Implement validation for moves when in check (must escape check)
  - Implement castling validation (king/rook not moved, no pieces between, not through check)
  - Implement en passant validation
  - Filter pseudo-legal moves to only legal moves
  - _Requirements: 2.3, 2.4, 3.2, 3.3, 3.4, 7.2_

- [ ]* 6.1 Write property test for check validation
  - **Property 9: Cannot leave king in check**
  - **Validates: Requirements 3.2**

- [ ]* 6.2 Write property test for escaping check
  - **Property 10: Must escape check**
  - **Validates: Requirements 3.3**

- [ ]* 6.3 Write property test for castling validation
  - **Property 11: Castling validation**
  - **Validates: Requirements 3.4**

- [x] 7. Implement move execution





  - Implement execute_move method in ChessEngine
  - Handle normal piece moves
  - Handle pawn promotion
  - Handle castling (move both king and rook)
  - Handle en passant capture (remove captured pawn)
  - Update castling rights when king or rook moves
  - Update castling rights when rook is captured
  - Update en passant target square
  - Update halfmove clock and fullmove number
  - Add move to move history
  - Add position to position history
  - Switch current player
  - _Requirements: 2.2, 2.5, 3.5, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1_

- [ ]* 7.1 Write property test for move execution
  - **Property 4: Legal move execution updates state**
  - **Validates: Requirements 2.2**

- [ ]* 7.2 Write property test for state preservation on illegal moves
  - **Property 5: Illegal moves preserve state**
  - **Validates: Requirements 2.4**

- [ ]* 7.3 Write property test for turn alternation
  - **Property 6: Turn alternation**
  - **Validates: Requirements 2.5**

- [ ]* 7.4 Write property test for move history
  - **Property 7: Move history recording**
  - **Validates: Requirements 8.1**

- [ ]* 7.5 Write property test for pawn promotion
  - **Property 12: Pawn promotion**
  - **Validates: Requirements 3.5**

- [ ]* 7.6 Write property test for castling execution
  - **Property 21: Castling execution**
  - **Validates: Requirements 7.1**

- [ ]* 7.7 Write property test for en passant availability
  - **Property 22: En passant availability**
  - **Validates: Requirements 7.2**

- [ ]* 7.8 Write property test for en passant capture
  - **Property 23: En passant capture**
  - **Validates: Requirements 7.3**

- [ ]* 7.9 Write property test for castling rights revocation on move
  - **Property 24: Castling rights revocation on piece move**
  - **Validates: Requirements 7.4**

- [ ]* 7.10 Write property test for castling rights revocation on capture
  - **Property 25: Castling rights revocation on rook capture**
  - **Validates: Requirements 7.5**

- [x] 8. Implement game ending detection





  - Implement checkmate detection (in check with no legal moves)
  - Implement stalemate detection (no legal moves, not in check)
  - Implement threefold repetition detection
  - Implement fifty-move rule detection
  - Implement insufficient material detection
  - Create is_draw method that checks all draw conditions
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 8.1 Write property test for checkmate detection
  - **Property 13: Checkmate detection**
  - **Validates: Requirements 4.1**

- [ ]* 8.2 Write property test for stalemate detection
  - **Property 14: Stalemate detection**
  - **Validates: Requirements 4.2**

- [ ]* 8.3 Write property test for threefold repetition
  - **Property 15: Threefold repetition**
  - **Validates: Requirements 4.3**

- [ ]* 8.4 Write property test for fifty-move rule
  - **Property 16: Fifty-move rule**
  - **Validates: Requirements 4.4**

- [ ]* 8.5 Write property test for insufficient material
  - **Property 17: Insufficient material**
  - **Validates: Requirements 4.5**

- [x] 9. Checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.
-

- [x] 10. Implement algebraic notation




  - Implement Move.to_algebraic_notation method
  - Handle piece notation (K, Q, R, B, N, or empty for pawns)
  - Handle capture notation (x)
  - Handle check notation (+)
  - Handle checkmate notation (#)
  - Handle castling notation (O-O, O-O-O)
  - Handle pawn promotion notation (=Q, =R, =B, =N)
  - Handle disambiguation when multiple pieces can move to same square
  - _Requirements: 8.2, 8.3, 8.4, 8.5_

- [ ]* 10.1 Write property test for algebraic notation format
  - **Property 26: Algebraic notation format**
  - **Validates: Requirements 8.2**

- [ ]* 10.2 Write property test for capture notation
  - **Property 28: Capture notation**
  - **Validates: Requirements 8.4**

- [ ]* 10.3 Write property test for check and checkmate notation
  - **Property 29: Check and checkmate notation**
  - **Validates: Requirements 8.5**

- [ ]* 10.4 Write property test for move history ordering
  - **Property 27: Move history ordering**
  - **Validates: Requirements 8.3**

- [x] 11. Implement AI opponent





  - Create AIOpponent class
  - Implement position evaluation based on material count
  - Implement find_checkmate_in_one method
  - Implement select_move method that prioritizes checkmate, avoids losing material
  - Ensure AI only selects from legal moves
  - Add time limit for move selection
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 11.1 Write property test for AI legal moves
  - **Property 18: AI generates legal moves**
  - **Validates: Requirements 5.1, 5.2**

- [ ]* 11.2 Write property test for material evaluation
  - **Property 19: Material evaluation consistency**
  - **Validates: Requirements 5.3**

- [ ]* 11.3 Write property test for AI checkmate in one
  - **Property 20: AI finds checkmate in one**
  - **Validates: Requirements 5.5**

- [ ]* 11.4 Write unit tests for AI behavior
  - Test AI avoids losing material without compensation
  - Test AI on known positions
  - _Requirements: 5.4_

- [x] 12. Implement ChessEngine orchestration





  - Create ChessEngine class
  - Implement initialize_game for single-player and multiplayer modes
  - Implement get_legal_moves method
  - Implement is_legal_move method
  - Wire together move generation, validation, and execution
  - Integrate check, checkmate, stalemate, and draw detection
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4_

- [ ]* 12.1 Write unit tests for game initialization modes
  - Test single-player mode initialization
  - Test multiplayer mode initialization
  - _Requirements: 1.1, 1.2_

- [x] 13. Implement GameController





  - Create GameController class
  - Implement start_new_game method
  - Implement handle_square_selection method
  - Implement handle_move_attempt method
  - Implement handle_promotion_choice method
  - Implement get_current_state method
  - Add state tracking for selected piece
  - Integrate AI move generation for single-player mode
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.5_

- [x] 14. Implement UI display component





  - Create board rendering function
  - Display all pieces in current positions with clear white/black distinction
  - Display current player's turn
  - Highlight selected piece and legal move destinations
  - Display check indicator when player is in check
  - Display move history in algebraic notation
  - Display game result (checkmate, stalemate, draw)
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2, 8.3_

- [ ]* 14.1 Write unit tests for UI display
  - Test board rendering includes all pieces
  - Test color distinction in rendering
  - Test turn indicator display
  - Test check indicator display
  - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [x] 15. Implement main game loop





  - Create main entry point
  - Prompt user for game mode selection
  - Initialize game with selected mode
  - Loop: display board, get user input, process move, check for game end
  - Handle AI turns in single-player mode
  - Display final game result
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 16. Final checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 17. End-to-end testing
  - Test complete game from start to checkmate
  - Test complete game from start to stalemate
  - Test complete game with draw conditions
  - Test single-player mode full game
  - Test multiplayer mode full game
  - _Requirements: All_
