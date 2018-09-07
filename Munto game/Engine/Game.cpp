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
	if (wnd.mouse.LeftIsPressed()) {
		//locked = true;

		int gx = (wnd.mouse.GetPosX() - 25) / 50;
		int gy = (wnd.mouse.GetPosY() - 25) / 50;
	}

	if (!lpressed && (GetKeyState('L') & 0x8000))
	{
		locked = !locked;
	}
	lpressed = (GetKeyState('L') & 0x8000);

	if (!locked) {
		std::ifstream in("BoardData.txt");

		pieces.clear();

		int pieceCount; in >> pieceCount;
		for (int i = 0; i < pieceCount; i++) {
			int x; in >> x;
			int y; in >> y;
			int d; in >> d;
			pieces.push_back(Piece(x, y, d));
		}
		in.close();
	}
	else return;

	if (!(pieceSelected + 1)) {
		int gx = (wnd.mouse.GetPosX() - 25) / 50;
		int gy = (wnd.mouse.GetPosY() - 25) / 50;

		if (gx >= 0 && gx < 9 && gy >= 0 && gy < 9) {
			if (!pressed && wnd.mouse.LeftIsPressed()) {
				for (int i = 0; i < pieces.size(); i++) {
					if (pieces[i].x == gx && pieces[i].y == gy) {
						pieceSelected = i;
						break;
					}
				}
			}
		}
	}
	else {
		int mx = wnd.mouse.GetPosX();
		int my = wnd.mouse.GetPosY();
		bool lp = wnd.mouse.LeftIsPressed();

		// Check for deletion
		if (mx >= 4 && mx <= 20 && my >= 4 && my <= 20) {
			if (!pressed && lp) {
				pieces.erase(pieces.begin() + pieceSelected);

				output_data();

				pieceSelected = -1;
			}
		}

		// Check for swapping
		if (mx >= 479 && mx <= 495 && my >= 4 && my <= 20) {
			if (!pressed && lp) {
				int sid = pieces[pieceSelected].id;
				int nid = sid;

				if		(sid < 10) {
					if (sid % 2 == 0)
						nid = sid + 1;
					else
						nid = sid - 1;
				}
				else if (sid < 21 && sid > 10) {
					if (sid % 2 == 1)
						nid = sid + 1;
					else
						nid = sid - 1;
				}

				pieces[pieceSelected].id = nid;

				output_data();

				pieceSelected = -1;
			}
		}

		// Check for moving
		int gx = (mx - 25) / 50;
		int gy = (my - 25) / 50;

		if (gx >= 0 && gx < 9 && gy >= 0 && gy < 9) {
			if (!pressed && lp) {
				bool occupied = false;
				for (int i = 0; i < pieces.size(); i++) {
					if (i == pieceSelected) continue;

					if (gx == pieces[i].x && gy == pieces[i].y) {
						occupied = true;
					}
				}

				if (!occupied) {
					pieces[pieceSelected].x = gx;
					pieces[pieceSelected].y = gy;

					output_data();

					pieceSelected = -1;
				}
			}
		}
	}

	pressed = wnd.mouse.LeftIsPressed();
}

void Game::ComposeFrame()
{
	// Draw background
	float mainbrightness = 1.0f - (0.5f * locked);
	gfx.DrawSprite(0, 0, bg, mainbrightness);

	// Draw pieces
	for (int i = 0; i < pieces.size(); i++) {
		float piecebrightness = 1.0f - (0.5f * (i == pieceSelected));
		gfx.DrawSprite(25 + pieces[i].x * 50, 25 + pieces[i].y * 50, spr_piece[pieces[i].id], mainbrightness * piecebrightness);
	}
}

void Game::output_data()
{
	std::ofstream out("BoardData.txt");

	out << pieces.size() << std::endl;
	for (int i = 0; i < pieces.size(); i++) {
		out << pieces[i].x << " " << pieces[i].y << " " << pieces[i].id << std::endl;
	}

	out.close();
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
