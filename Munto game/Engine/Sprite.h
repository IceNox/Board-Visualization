#pragma once

#include "Colors.h"
#include <string>
#include "ChiliWin.h"

class Sprite
{
public:
	Sprite(const std::string& filename, std::string spriteName);
	Sprite(int width, int height, std::string spriteName);
	Sprite(const Sprite&);
	Sprite() {};
	~Sprite();
	Sprite& operator=(const Sprite&);
	void PutPixel(int x, int y, Color c);
	Color GetPixel(int x, int y) const;
	Color GetPixel(int x, int y, float brightness) const;
	int GetWidth() const;
	int GetHeight() const;
	std::string GetName() const;
private:
	std::string spriteName;
	Color* pPixels = nullptr;
	int width;
	int height;
};
