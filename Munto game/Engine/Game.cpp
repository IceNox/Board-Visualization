/****************************************************************************************** 
 *	Chili DirectX Framework Version 16.07.20											  *	
 *	Game.cpp																			  *
 *	Copyright 2016 PlanetChili.net <http://www.planetchili.net>							  *
 *																						  *
 *	This file is part of The Chili DirectX Framework.									  *
 *																						  *
 *	The Chili DirectX Framework is free software: you can redistribute it and/or modify	  *
 *	it under the terms of the GNU General Public License as published by				  *
 *	the Free Software Foundation, either version 3 of the License, or					  *
 *	(at your option) any later version.													  *
 *																						  *
 *	The Chili DirectX Framework is distributed in the hope that it will be useful,		  *
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of						  *
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the						  *
 *	GNU General Public License for more details.										  *
 *																						  *
 *	You should have received a copy of the GNU General Public License					  *
 *	along with The Chili DirectX Framework.  If not, see <http://www.gnu.org/licenses/>.  *
 ******************************************************************************************/
#include "MainWindow.h"
#include "Game.h"

#include <fstream>

Game::Game( MainWindow& wnd )
	:
	wnd( wnd ),
	gfx( wnd )
{
	read_pictures();
}

void Game::Go()
{
	gfx.BeginFrame();	
	UpdateModel();
	ComposeFrame();
	gfx.EndFrame();
}

void Game::UpdateModel()
{
	std::ifstream in("BoardData.txt");

	pieces.clear();

	int pieceCount; in >> pieceCount;
	for (int i = 0; i < pieceCount; i++) {
		int x; in >> x;
		int y; in >> y;
		int d; in >> d;
		pieces.push_back(Piece(x, y, d));
	}
}

void Game::ComposeFrame()
{
	// Draw background
	gfx.DrawSprite(0, 0, bg);

	// Draw pieces
	for (int i = 0; i < pieces.size(); i++) {
		gfx.DrawSprite(25 + pieces[i].x * 50, 25 + pieces[i].y * 50, spr_piece[pieces[i].id]);
	}
}

void Game::read_pictures()
{
	// Read background
	bg = Sprite("Textures/bg.tga", "bg");

	// Read pieces
	spr_piece.push_back(Sprite("Textures/Rune (1).tga" , "p1"));
	spr_piece.push_back(Sprite("Textures/Rune (2).tga" , "p2"));
	spr_piece.push_back(Sprite("Textures/Rune (3).tga" , "p3"));
	spr_piece.push_back(Sprite("Textures/Rune (4).tga" , "p4"));
	spr_piece.push_back(Sprite("Textures/Rune (5).tga" , "p5"));
	spr_piece.push_back(Sprite("Textures/Rune (6).tga" , "p6"));
	spr_piece.push_back(Sprite("Textures/Rune (7).tga" , "p7"));
	spr_piece.push_back(Sprite("Textures/Rune (8).tga" , "p8"));
	spr_piece.push_back(Sprite("Textures/Rune (9).tga" , "p9"));
	spr_piece.push_back(Sprite("Textures/Rune (10).tga", "p10"));
	spr_piece.push_back(Sprite("Textures/Rune (11).tga", "p11"));
	spr_piece.push_back(Sprite("Textures/Rune (12).tga", "p12"));
	spr_piece.push_back(Sprite("Textures/Rune (13).tga", "p13"));
	spr_piece.push_back(Sprite("Textures/Rune (14).tga", "p14"));
	spr_piece.push_back(Sprite("Textures/Rune (15).tga", "p15"));
	spr_piece.push_back(Sprite("Textures/Rune (16).tga", "p16"));
	spr_piece.push_back(Sprite("Textures/Rune (17).tga", "p17"));
	spr_piece.push_back(Sprite("Textures/Rune (18).tga", "p18"));
	spr_piece.push_back(Sprite("Textures/Rune (19).tga", "p19"));
	spr_piece.push_back(Sprite("Textures/Rune (20).tga", "p20"));
	spr_piece.push_back(Sprite("Textures/Rune (21).tga", "p21"));
	spr_piece.push_back(Sprite("Textures/Rune (22).tga", "p22"));
}
