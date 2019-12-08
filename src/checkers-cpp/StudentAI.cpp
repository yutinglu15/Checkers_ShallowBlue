#include "StudentAI.h"
#include <random>
#include <cmath>
#include <algorithm>

//The following part should be completed by students.
//The students can modify anything except the class name and exisiting functions and varibles.
StudentAI::StudentAI(int col,int row,int p)
	:AI(col, row, p)
{
    board = Board(col,row,p);
    board.initializeGame();
    player = 2;
    depth = 6;
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
    Move res = minimaxMove(moves);
    board.makeMove(res,player);
    return res;


}

Move StudentAI::minimaxMove(const vector<vector<Move> > & moves)
{
    Move best;
    double best_score = - INFINITY;
    for (auto chess : moves)
    {
        for (auto move : chess)
        {
            board.makeMove(move, player);
            double score = get_min(move, depth, -INFINITY, INFINITY);
            if (score > best_score)
            {
                best = move;
                best_score = score;
            }
            board.Undo();
        }
    }
    return best;
}

double StudentAI::get_min(const Move& move, int depth, double alpha, double beta)
{
    if (depth == 0)
        return utility(board, player);

    vector<vector<Move>> moves = board.getAllPossibleMoves(player == 1?2:1);

    if (moves.size() == 0)
        return INFINITY;

    double min_val = INFINITY;
    for (auto chess : moves)
    {
        for (auto move: chess)
        {
            board.makeMove(move, player == 1?2:1);
            min_val = std::min(get_max(move, depth - 1, alpha, beta), min_val);
            beta = std::min(beta, min_val);
            board.Undo();
            if (alpha >= beta)  return min_val;
        }
    }
    return min_val;
}

double StudentAI::get_max(const Move& move, int depth, double alpha, double beta)
{
    if (depth == 0)
        return utility(board, player == 1?2:1);

    vector<vector<Move>> moves = board.getAllPossibleMoves(player);

    if (moves.size() == 0)
        return - INFINITY;

    double max_val = - INFINITY;
    for (auto chess : moves)
    {
        for (auto move: chess)
        {
            board.makeMove(move, player);
            max_val = std::max(get_min(move, depth - 1, alpha, beta), max_val);
            alpha = std::max(alpha, max_val);
            board.Undo();
            if (alpha >= beta)  return max_val;
        }
    }
    return max_val;
}

double StudentAI::utility(const Board & board, int player) const
{
    if (player == 1)
        return board.blackCount - board.whiteCount;
    return board.whiteCount - board.blackCount;
}