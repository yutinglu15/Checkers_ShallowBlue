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
    int player, depth;
//    int cutoff[];
	StudentAI(int col, int row, int p);


	virtual Move GetMove(Move board);
	double basic_utility(const Board & board, int player) const;
	double utility(Board & board, int player) const;
	double* theta771_start;
	double* theta771_mid;
	double* theta771_last;

    double* theta772_start;
	double* theta772_mid;
	double* theta772_last;
    virtual ~StudentAI()
    { delete[] theta771_start;
      delete[] theta771_mid;
      delete[] theta771_last;
      delete[] theta772_start;
      delete[] theta772_mid;
      delete[] theta772_last;
     }
private:
    Move minimaxMove(const vector<vector<Move>>& moves);
    double get_min(const Move& move, int depth, double alpha, double beta);
    double get_max(const Move& move, int depth, double alpha, double beta);

};

#endif //STUDENTAI_H
