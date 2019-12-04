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
	Move monte_carlo_tree(vector<Move> moves, int simulate_times, int s_parent);
	int simulate(Move move, int simulate_times);
	void undo(Board board, int times);
	float min_value(Move move, int depth, float alpha, float beta);
	float max_value(Move move, int depth, float alpha, float beta);
	float utility(Board board);
	float[] features(Board board, int color);
};

#endif //STUDENTAI_H
