#include "StudentAI.h"
#include <random>
#include <cmath>
#include <algorithm>

struct WB
{
    int w;
    int b;
    WB(int w, int b)
        :w(w),b(b) {}
};


namespace
{

    WB wking_bking(const Board & board)
    {
        int wking = 0;
        int bking = 0;
        for (int r=0; r<board.row; r++)
            for (int c=0; c<board.col; c++)
                if (board.board[r][c].isKing)
                    if (board.board[r][c].color == "W")
                        wking ++;
                    else    bking++;
        return WB(wking, bking);
    }

    WB wdis_bdis(const Board & board)
    {
        int wdis = 0;
        int bdis = 0;
        for (int r=0; r<board.row; r++)
            for (int c=0; c<board.col; c++)
                if (board.board[r][c].color == "W")
                    wdis += board.row - 1 - r;
                else if (board.board[r][c].color == "B")
                    bdis += r;
        return WB(wdis, bdis);
    }

    WB wback_bback(const Board & board)
    {
        int wback = 0;
        int bback = 0;
        for (int c=0; c<board.col; c++)
            if (board.board[board.row-1][c].color == "W")
                wback ++;
            else if (board.board[0][c].color == "B")
                bback ++;
        return WB(wback, bback);
    }


    WB wedge_bedge(const Board & board)
    {
        int wedge = 0;
        int bedge = 0;
        for (int r=0; r<board.row; r++)
        {
            wedge += (board.board[r][0].color == "W") + (board.board[r][board.col - 1].color == "W");
            bedge += (board.board[0][0].color == "B") + (board.board[0][board.col - 1].color == "B");
        }
        return WB(wedge, bedge);
    }


    WB wcenter_bcenter(const Board & board)
    {
        int wcenter = 0;
        int bcenter = 0;
        for (int c=0; c<board.col; c++)
        {
            wcenter += (board.board[board.row/2][c].color == "W") + (board.board[board.row/2+1][c].color == "W");
            bcenter += (board.board[board.row/2][c].color == "B") + (board.board[board.row/2+1][c].color == "B");
        }
        return WB(wcenter, bcenter);
    }


    WB wdiag_bdiag(const Board & board)
    {
        int wdiag = 0;
        int bdiag = 0;
        for (int r=0; r<board.row-1; r++)
        {
            wdiag += (board.board[r][r].color == "W") + (board.board[r + 1][r].color == "W") + (board.board[r][r + 1].color == "W")
                    + (board.board[r][board.col-1-r].color == "W") + (board.board[r+1][board.col-1-r].color == "W")
                    + (board.board[r][board.col-2-r].color == "W");
            bdiag += (board.board[r][r].color == "B") + (board.board[r+1][r].color == "B") + (board.board[r][r+1].color == "B")
                    + (board.board[r][board.col-1-r].color == "B") + (board.board[r+1][board.col-1-r].color == "B")
                    + (board.board[r][board.col-2-r].color == "B");
        }
        wdiag += (board.board[board.row - 1][0].color == "W") + (board.board[board.row - 1][board.row - 1].color == "W");
        bdiag += (board.board[board.row-1][0].color == "B") + (board.board[board.row-1][board.row-1].color == "B");
        return WB(wdiag, bdiag);
    }


    // some patterns
    WB wdog_bdog(const Board & board)
    {
        int wdog = (board.board[board.row-1][board.col-1].color == "." and board.board[board.row-1][board.col-2].color == "W"
                        and board.board[board.row-2][board.col-1].color == "B")
                    + (board.board[board.row-1][0].color == "." and board.board[board.row-1][1].color == "W"
                        and board.board[board.row-2][0].color == "B");
        int bdog = (board.board[0][0].color == "." and board.board[0][1].color == "B" \
                        and board.board[1][0].color == "W")
                    +  (board.board[0][board.col-1].color == "." and board.board[0][board.col-2].color == "B" \
                        and board.board[1][board.col-1].color == "W");
        return WB(wdog, bdog);
    }

    WB wbridge_bbridge(const Board & board)
    {
        int wbridge = 0;
        int bbridge = 0;
        for (int c=1; c<board.col-3; c++)
        {
            wbridge += (board.board[board.row-1][c].color == "W") and (board.board[board.row-1][c + 2].color == "W");
            bbridge += (board.board[0][c].color == "B") and (board.board[0][c+2].color == "B");
        }
        return WB(wbridge, bbridge);
    }

    WB woreo_boreo(const Board & board)
    {
        int woreo = 0;
        int boreo = 0;
        for (int c=0; c<board.col-3; c++)
        {
            woreo += board.board[board.row-1][c].color == "W" and board.board[board.row-2][c+1].color == "W"
                    and board.board[board.row-1][c+2].color == "W";
            boreo += board.board[0][c].color == "B" and board.board[1][c+1].color == "B"
                    and board.board[0][c+2].color == "B";
        }
        return WB(woreo, boreo);
    }

    WB wuptriangle_buptriangle(const Board & board)
    {
        int wuptriangle = 0;
        int buptriangle = 0;
        for (int r=1; r<board.row - 1; r++)
            for (int c=0; c<board.col - 2; c++)
            {
                wuptriangle += (board.board[r][c].color == "W" and board.board[r-1][c+1].color == "W" and board.board[r][c+2].color == "W");
                buptriangle += (board.board[r][c].color == "B" and board.board[r-1][c+1].color == "B" and board.board[r][c+2].color == "B");
            }
        return WB(wuptriangle, buptriangle);
    }

    WB wdowntriangle_bdowntriangle(const Board & board)
    {
        int wdowntriangle = 0;
        int bdowntriangle = 0;
        for (int r=1; r<board.row - 1; r++)
            for (int c=0; c<board.col - 2; c++)
            {
                wdowntriangle += (board.board[r][c].color == "W" and board.board[r+1][c+1].color == "W" and board.board[r][c+2].color == "W");
                bdowntriangle += (board.board[r][c].color == "B" and board.board[r+1][c+1].color == "B" and board.board[r][c+2].color == "B");
            }
        return WB(wdowntriangle, bdowntriangle);
    }

    WB moveables(Board & board, int player)
    {
        int len = 0;
        int eatable = 0;
        vector<vector<Move>> moves = board.getAllPossibleMoves(player);
        for (auto chess : moves)
            for (auto move: chess)
            {
                len ++;
                if (move.seq.size() > 2)
                    eatable += move.seq.size() - 1;
                else if ((abs(move.seq[0][0] - move.seq[1][0]) + abs(move.seq[0][1] - move.seq[1][1])) > 2)
                    eatable ++;
            }
        return WB(len, eatable);
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
    if (col == 7) depth = 6;
    else
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
            double score = get_min(move, depth, best_score, INFINITY);
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
    WB wk_bk = wking_bking(board);
    if (player == 1)
        return 3*board.blackCount + 5*wk_bk.b - 3*board.whiteCount - 5*wk_bk.w;
    return 3*board.whiteCount + 5*wk_bk.w - 3*board.blackCount - 5*wk_bk.b;
}


