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

    void wking_bking(const Board & board, int* wcount, int* bcount)
    {
        int wking = 0;
        int bking = 0;
        for (int r=0; r<board.row; r++)
            for (int c=0; c<board.col; c++)
                if (board.board[r][c].isKing)
                    if (board.board[r][c].color == "W")
                        wking ++;
                    else    bking++;
        wcount[1] = wking;
        bcount[1] = bking;
    }

    void wdis_bdis(const Board & board, int* wcount, int* bcount)
    {
        int wdis = 0;
        int bdis = 0;
        for (int r=0; r<board.row; r++)
            for (int c=0; c<board.col; c++)
                if (board.board[r][c].color == "W")
                    wdis += board.row - 1 - r;
                else if (board.board[r][c].color == "B")
                    bdis += r;
        wcount[2] = wdis;
        bcount[2] = bdis;
//        return WB(wdis, bdis);
    }

    void wback_bback(const Board & board, int* wcount, int* bcount)
    {
        int wback = 0;
        int bback = 0;
        for (int c=0; c<board.col; c++)
            if (board.board[board.row-1][c].color == "W")
                wback ++;
            else if (board.board[0][c].color == "B")
                bback ++;
        wcount[3] = wback;
        bcount[3] = bback;
//        return WB(wback, bback);
    }


    void wedge_bedge(const Board & board, int* wcount, int* bcount)
    {
        int wedge = 0;
        int bedge = 0;
        for (int r=0; r<board.row; r++)
        {
            wedge += (board.board[r][0].color == "W") + (board.board[r][board.col - 1].color == "W");
            bedge += (board.board[0][0].color == "B") + (board.board[0][board.col - 1].color == "B");
        }
        wcount[4] = wedge;
        bcount[4] = bedge;
//        return WB(wedge, bedge);
    }


    void wcenter_bcenter(const Board & board, int* wcount, int* bcount)
    {
        int wcenter = 0;
        int bcenter = 0;
        for (int c=0; c<board.col; c++)
        {
            wcenter += (board.board[board.row/2][c].color == "W") + (board.board[board.row/2+1][c].color == "W");
            bcenter += (board.board[board.row/2][c].color == "B") + (board.board[board.row/2+1][c].color == "B");
        }
        wcount[5] = wcenter;
        bcount[5] = bcenter;
//        return WB(wcenter, bcenter);
    }


    void wdiag_bdiag(const Board & board, int* wcount, int* bcount)
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
        wcount[6] = wdiag;
        bcount[6] = bdiag;
//        return WB(wdiag, bdiag);
    }


    // some patterns
    void wdog_bdog(const Board & board, int* wcount, int* bcount)
    {
        int wdog = (board.board[board.row-1][board.col-1].color == "." and board.board[board.row-1][board.col-2].color == "W"
                        and board.board[board.row-2][board.col-1].color == "B")
                    + (board.board[board.row-1][0].color == "." and board.board[board.row-1][1].color == "W"
                        and board.board[board.row-2][0].color == "B");
        int bdog = (board.board[0][0].color == "." and board.board[0][1].color == "B" \
                        and board.board[1][0].color == "W")
                    +  (board.board[0][board.col-1].color == "." and board.board[0][board.col-2].color == "B" \
                        and board.board[1][board.col-1].color == "W");
        wcount[7] = wdog;
        bcount[7] = bdog;
//        return WB(wdog, bdog);
    }

    void wbridge_bbridge(const Board & board, int* wcount, int* bcount)
    {
        int wbridge = 0;
        int bbridge = 0;
        for (int c=1; c<board.col-3; c++)
        {
            wbridge += (board.board[board.row-1][c].color == "W") and (board.board[board.row-1][c + 2].color == "W");
            bbridge += (board.board[0][c].color == "B") and (board.board[0][c+2].color == "B");
        }
        wcount[8] = wbridge;
        bcount[8] = bbridge;
//        return WB(wbridge, bbridge);
    }

    void wuptriangle_buptriangle(const Board & board, int* wcount, int* bcount)
    {
        int wuptriangle = 0;
        int buptriangle = 0;
        for (int r=1; r<board.row - 1; r++)
            for (int c=0; c<board.col - 2; c++)
            {
                wuptriangle += (board.board[r][c].color == "W" and board.board[r-1][c+1].color == "W" and board.board[r][c+2].color == "W");
                buptriangle += (board.board[r][c].color == "B" and board.board[r-1][c+1].color == "B" and board.board[r][c+2].color == "B");
            }
        wcount[9] = wuptriangle;
        bcount[9] = buptriangle;
//        return WB(wuptriangle, buptriangle);
    }

    void wdowntriangle_bdowntriangle(const Board & board, int* wcount, int* bcount)
    {
        int wdowntriangle = 0;
        int bdowntriangle = 0;
        for (int r=1; r<board.row - 1; r++)
            for (int c=0; c<board.col - 2; c++)
            {
                wdowntriangle += (board.board[r][c].color == "W" and board.board[r+1][c+1].color == "W" and board.board[r][c+2].color == "W");
                bdowntriangle += (board.board[r][c].color == "B" and board.board[r+1][c+1].color == "B" and board.board[r][c+2].color == "B");
            }
        wcount[10] = wdowntriangle;
        bcount[10] = bdowntriangle;
//        return WB(wdowntriangle, bdowntriangle);
    }

    void woreo_boreo(const Board & board, int* wcount, int* bcount)
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
        wcount[11] = woreo;
        bcount[11] = boreo;
//        return WB(woreo, boreo);
    }


    void moveables(Board & board, int player, int* count)
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
        count[12] = len;
        count[13] = eatable;
//        return WB(len, eatable);
    }

    double calculate_utility(int* wcount, int* bcount, double* theta)
    {
        double result = 0;
        for (int i = 0; i < 14; i++)
            result += wcount[i]*theta[i];
        for (int i = 14; i < 28; i++)
            result += bcount[i]*theta[i];
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
    if (col == 7) depth = 6;
    else
        depth = 4;
    // I don't remember!!!!! Lucy NB!
    theta = new double[28]{-24.13, -7.87, -17.89, -16.67, -6.99, 7.22, 1.19, 0.72,
                       -4.2, -4.52, -2.49, -3.14, 5.69, 0.02, 3.53, -3.58, 9.37,
                       -3.81, -1.58, -1.75, 2.51, 0.26, 18.3, 10.25, 3.63,
                       3.69, 1.32, -4.03};
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

double StudentAI::basic_utility(const Board & board, int player) const
{
    WB wk_bk = wking_bking(board);
    if (player == 1)
        return 3*board.blackCount + 5*wk_bk.b - 3*board.whiteCount - 5*wk_bk.w;
    return 3*board.whiteCount + 5*wk_bk.w - 3*board.blackCount - 5*wk_bk.b;
}

double StudentAI::utility(Board & board, int player) const
{
//    [wcount, wking, wdis, wback, wedge,
//            wcenter, wdiag, wdog, wbridge, wuptriangle,
//            wdowntriangle, woreo, wmoveable, weatable]
    int wcount[14];
    wcount[0] = board.whiteCount;
    int bcount[14];
    bcount[0] = board.blackCount;
    wking_bking(board, wcount, bcount);
    wdis_bdis(board, wcount, bcount);
    wback_bback(board, wcount, bcount);
    wedge_bedge(board, wcount, bcount);
    wcenter_bcenter(board, wcount, bcount);
    wdiag_bdiag(board, wcount, bcount);
    wdog_bdog(board, wcount, bcount);
    wbridge_bbridge(board, wcount, bcount);
    wuptriangle_buptriangle(board, wcount, bcount);
    wdowntriangle_bdowntriangle(board, wcount, bcount);
    woreo_boreo(board, wcount, bcount);

    if (player == 1)
    {
        moveables(board, 2, wcount);
        bcount[12] = 0;
        bcount[13] = 0;
    }
    else
    {
        wcount[12] = 0;
        wcount[13] = 0;
        moveables(board, 1, bcount);
    }

    return calculate_utility(wcount, bcount, theta);

}
