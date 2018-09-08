#include "Sprite.h"
#include <cassert>
#include <fstream>

Sprite::Sprite(const std::string& filename, std::string spriteName)
{
	// Clear pixels
	pPixels = nullptr;

	// Open file
	std::ifstream file;
	file.open(filename, std::ios::binary | std::ios::in);
	assert(file);

	// Read the header info
	file.seekg(2);
	assert(file.get() == 2);

	// Get image dimensions
	file.seekg(10, std::ios::cur);
	int w1 = file.get();
	int w2 = file.get();
	int h1 = file.get();
	int h2 = file.get();

	width = w1 + w2 * 256;
	height = h1 + h2 * 256;

	// Set sprite name
	this->spriteName = spriteName;

	// Allocate memory for the image
	pPixels = new Color[width*height];

	// Read the image
	file.seekg(2, std::ios::cur);
	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			int b = file.get();
			int g = file.get();
			int r = file.get();
			int a = file.get();

			pPixels[(height - 1 - y) * width + x] = Color(a, r, g, b);
		}
	}

	// Close file
	file.close();
}

Sprite::Sprite(int width, int height, std::string spriteName)
	:
	width(width),
	height(height),
	pPixels(new Color[width*height]),
	spriteName(spriteName)
{
}

Sprite::Sprite(const Sprite& rhs)
	:
	Sprite(rhs.width, rhs.height, rhs.spriteName)
{
	const int nPixels = width * height;
	for (int i = 0; i < nPixels; i++) {
		pPixels[i] = rhs.pPixels[i];
	}
}

Sprite::~Sprite()
{
	delete[] pPixels;
	pPixels = nullptr;
}

Sprite& Sprite::operator=(const Sprite& rhs)
{
	width = rhs.width;
	height = rhs.height;
	spriteName = rhs.spriteName;

	delete[] pPixels;
	pPixels = new Color[width*height];

	const int nPixels = width * height;
	for (int i = 0; i < nPixels; i++) {
		pPixels[i] = rhs.pPixels[i];
	}

	return *this;
}

void Sprite::PutPixel(int x, int y, Color c)
{
	assert(x >= 0);
	assert(x < width);
	assert(y >= 0);
	assert(y < height);
	pPixels[y * width + x] = c;
}

Color Sprite::GetPixel(int x, int y) const
{
	assert(x >= 0);
	assert(x < width);
	assert(y >= 0);
	assert(y < height);
	return pPixels[y * width + x];
}

Color Sprite::GetPixel(int x, int y, float brightness) const
{
	assert(x >= 0);
	assert(x < width);
	assert(y >= 0);
	assert(y < height);

	Color set = pPixels[y * width + x];
	int newR = set.GetR() * brightness;
	int newG = set.GetG() * brightness;
	int newB = set.GetB() * brightness;

	set.SetR(newR);
	set.SetG(newG);
	set.SetB(newB);

	return set;
}

int Sprite::GetWidth() const
{
	return width;
}

int Sprite::GetHeight() const
{
	return height;
}

std::string Sprite::GetName() const
{
	return spriteName;
}