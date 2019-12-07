#include "StudentAI.h"
#include <random>
#include <cmath>

namespace{
    vector<Move> getMoves(const & vector<vector<Move>> Moves)
    {
        vector<Move> result;
        for(auto chess: Moves)
            for(auto move: chess)
                result.push_back(move);
        return result;
    }

}





//The following part should be completed by students.
//The students can modify anything except the class name and exisiting functions and varibles.
StudentAI::StudentAI(int col,int row,int p)
	:AI(col, row, p)
{
    board = Board(col,row,p);
    board.initializeGame();
    player = 2;
    depth = 4;
}

Move StudentAI::GetMove(Move move)
{
    if (move.seq.empty())
    {
        player = 1;
    } else{
        board.makeMove(move,player == 1?2:1);
    }
    vector<vector<Move> > moves = board.getAllPossibleMoves(player);
//    int i = rand() % (moves.size());
//    vector<Move> checker_moves = moves[i];
//    int j = rand() % (checker_moves.size());
//    Move res = checker_moves[j];
    Move res = minimaxMove(getMoves(moves));
    board.makeMove(res,player);
    return res;


}

Move StudentAI::minimaxMove(const & vector<Move> moves)
{
    Move best;
    double best_score = - INFINITY;
    for (auto move : moves)
    {
        board.makeMove(move, player);
        double score = get_min(move, depth, -INFINITY, INFINITY);
        if (score > best_score)
        {
            best = move;
            best_score = score;
        }
    }
    return best;
}

double StudentAI::get_min(Move move, int depth, double alpha, double beta)
{
    if (depth == 0)
        return utility(board);
}

