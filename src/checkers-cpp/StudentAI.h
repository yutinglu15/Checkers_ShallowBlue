#ifndef STUDENTAI_H
#define STUDENTAI_H
#include "AI.h"
#include "Board.h"
#pragma once

//The following part should be completed by students.
//Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI :public AI
{
public:
    Board board;
	StudentAI(int col, int row, int p);
	int depth;
	int movecount;
	float start;
	extern float theta[28];
	virtual Move GetMove(Move board);
	Move minimax_move(vector<Move> moves);
};

#endif //STUDENTAI_H
