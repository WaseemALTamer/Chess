# this file is responsible for loading all the images as pygame surfaces

from .Setting import *
import pygame
import os






class Images:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    pices_folder = os.path.join(file_dir, "Assets", "Pieces", PIECES_SET)

    # responsible for the paths
    
    # Pieces
    pawn_black_path = os.path.join(pices_folder, "Black_Pawn.png")
    knight_black_path = os.path.join(pices_folder, "Black_Knight.png")
    bishop_black_path = os.path.join(pices_folder, "Black_Bishop.png")
    rock_black_path = os.path.join(pices_folder, "Black_Rock.png")
    queen_black_path = os.path.join(pices_folder, "Black_Queen.png")
    king_black_path = os.path.join(pices_folder, "Black_King.png")
    pawn_white_path = os.path.join(pices_folder, "White_Pawn.png")
    knight_white_path = os.path.join(pices_folder, "White_Knight.png")
    bishop_white_path = os.path.join(pices_folder, "White_Bishop.png")
    rock_white_path = os.path.join(pices_folder, "White_Rock.png")
    queen_white_path = os.path.join(pices_folder, "White_Queen.png")
    king_white_path = os.path.join(pices_folder, "White_King.png")
    ghost_pawn_path = os.path.join(pices_folder, "Gost_Pawn.png")



    # responsible for loading up the surface

    # Pieces
    pawn_black_surface = pygame.image.load(pawn_black_path)
    knight_black_surface = pygame.image.load(knight_black_path)
    bishop_black_surface = pygame.image.load(bishop_black_path)
    rock_black_surface = pygame.image.load(rock_black_path)
    queen_black_surface = pygame.image.load(queen_black_path)
    king_black_surface = pygame.image.load(king_black_path)
    pawn_white_surface = pygame.image.load(pawn_white_path)
    knight_white_surface = pygame.image.load(knight_white_path)
    bishop_white_surface = pygame.image.load(bishop_white_path)
    rock_white_surface = pygame.image.load(rock_white_path)
    queen_white_surface = pygame.image.load(queen_white_path)
    king_white_surface = pygame.image.load(king_white_path)
    ghost_pawn_surface = pygame.image.load(ghost_pawn_path)




