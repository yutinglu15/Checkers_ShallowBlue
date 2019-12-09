#include "StudentAI.h"
#include <random>
#include <cmath>
#include <algorithm>
#include <iostream>

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
            result += bcount[i-14]*theta[i];
//        std::cout << result << std::flush;
        return result;
    }

    double** get_theta_first(int col, int row)
    {
        double theta771_start[] = {-3.05, -1.9, 0.04, -0.85, -0.06, 0.43, 0.21, 0.0, -0.18, 0.56, -0.32, -0.25, 2.9, -2.56, 1.23,
                          0.06, 0.44, 0.89, 0.67, 0.27, -0.0, 0.0, 0.64, 0.56, 0.07, 0.91, 0.0, 0.0};
        double theta771_mid[] = {-2.84, -1.09, -0.05, -0.67, 0.22, 0.42, 0.24, 0.0, -0.18, 0.72, 0.26, 0.38, 3.44, -2.88, 1.83,
                        0.04, 0.3, 0.79, 0.11, -0.02, -0.14, 0.0, 0.36, 0.3, -0.45, 0.9, 0.0, 0.0};
        double theta771_last[] = {-3.01, -1.01, -0.06, 0.13, 0.42, 0.18, 0.03, 0.0, -0.51, 0.75, 1.31, 1.26, 2.86, -2.55, 1.5,
                         0.22, 0.05, 0.42, 0.2, -0.06, -0.16, 0.0, 0.53, 0.45, -0.26, 0.44, 0.0, 0.0};



        double theta981_start[] = {-2.85, -0.22, 0.11, -0.54, 0.31, -0.03, 0.07, 0.0, -0.19, 0.45, -0.17, 0.45, 2.09, -1.88,
                          2.46, 1.24, -0.04, 0.64, 0.41, -0.36, 0.11, 0.25, -0.01, 0.09, -0.34, 0.96, 0.0, 0.0};
        double theta981_mid[] = {-1.95, -1.35, 0.11, -0.44, 0.11, 0.16, 0.02, 0.0, -0.18, 0.57, 0.26, 0.54, 2.37, -2.06, 1.22,
                        -0.19, 0.3, 0.9, 0.43, 0.09, 0.05, -0.06, 0.19, 0.19, -0.04, 0.69, 0.0, 0.0};
        double theta981_last[] = {-3.22, -1.85, 0.18, 0.48, 0.23, 0.14, -0.18, 0.0, -0.53, 1.25, 0.93, 0.03, 3.33, -3.01, 2.08,
                         0.05, 0.15, 0.65, 0.27, 0.03, -0.13, -1.0, -0.24, -0.25, 0.01, 0.03, 0.0, 0.0};



        double** start_mid_last;

        if (col == 7 && row == 7)
        {
            start_mid_last[0] = theta771_start;
            start_mid_last[1] = theta771_mid;
            start_mid_last[2] = theta771_last;
            return start_mid_last;
        }
        else
        {
            start_mid_last[0] = theta981_start;
            start_mid_last[1] = theta981_mid;
            start_mid_last[2] = theta981_last;
            return start_mid_last;
        }

    }

    double** get_theta_backhand(int row, int col)
    {
        double theta772_start[] = {2.07, -0.44, 0.29, 0.45, 0.32, -0.46, -0.04, 0.0, 0.37, -0.25, 0.16, 0.17, 0.0, 0.0, -2.18,
                          -0.62, -0.16, -1.0, 0.24, 0.72, 0.2, 0.0, 0.12, 0.04, 0.75, -1.29, 3.36, -2.93};
        double theta772_mid[] = {1.93, 0.09, 0.16, 0.37, 0.28, -0.18, -0.17, 0.0, 0.02, -0.28, 0.02, 0.13, 0.0, 0.0, -2.3, -1.12,
                        -0.07, -0.63, 0.38, 0.08, 0.16, 0.0, -0.4, 0.43, 0.54, -0.74, 3.47, -3.05};
        double theta772_last[] = {1.51, 0.44, -0.01, 0.11, 0.16, -0.16, -0.14, 0.0, -0.17, 0.47, -0.16, 0.02, 0.0, 0.0, -2.79,
                         -0.98, 0.0, 0.14, 0.4, -0.08, 0.0, 0.0, -0.26, 1.25, 0.06, -0.07, 2.32, -2.19};

        double theta982_start[] = {1.47, -0.0, 0.21, 0.5, 0.09, -0.09, 0.05, 0.0, 0.12, -0.45, 0.15, 0.55, 0.0, 0.0, -2.5, -0.49,
                          0.05, -0.45, 0.24, 0.24, 0.29, 0.29, 0.02, 0.12, 0.26, -0.26, 2.31, -2.11};
        double theta982_mid[] = {1.22, -0.16, 0.29, 0.22, 0.28, -0.21, -0.05, 0.0, 0.38, -0.24, -0.31, 0.59, 0.0, 0.0, -2.04,
                        -1.22, 0.14, -0.54, 0.12, -0.07, 0.05, -0.04, 0.31, 0.57, 0.41, -0.88, 3.14, -2.84};
        double theta982_last[] = {2.12, -0.19, 0.19, -0.23, 0.33, -0.17, -0.11, 0.0, -0.44, 0.32, 0.16, 0.0, 0.0, 0.0, -2.06,
                         -1.58, 0.09, -0.16, 0.46, -0.19, 0.0, -0.94, -0.7, 0.74, 1.33, -0.08, 4.14, -3.98};

        double** start_mid_last;

        if (col == 7 && row == 7)
        {
            start_mid_last[0] = theta772_start;
            start_mid_last[1] = theta772_mid;
            start_mid_last[2] = theta772_last;
            return start_mid_last;
        }
        else
        {
            start_mid_last[0] = theta982_start;
            start_mid_last[1] = theta982_mid;
            start_mid_last[2] = theta982_last;
            return start_mid_last;
        }
    }




}









//The following part should be completed by students.
//The students can modify anything except the class name and exisiting functions and varibles.
StudentAI::StudentAI(int col,int row, int p)
	:AI(col, row, p)
{
    board = Board(col,row,p);
    board.initializeGame();
    player = 2;
    if (col == 7) depth = 6;
    else
        depth = 4;
//    cutoff[] = {5,3};

    // I don't remember!!!!! Lucy NB!
    theta771_start = new double[28]{-3.05, -1.9, 0.04, -0.85, -0.06, 0.43, 0.21, 0.0, -0.18, 0.56, -0.32, -0.25, 2.9, -2.56, 1.23,
                      0.06, 0.44, 0.89, 0.67, 0.27, -0.0, 0.0, 0.64, 0.56, 0.07, 0.91, 0.0, 0.0};
    theta771_mid = new double[28]{-2.84, -1.09, -0.05, -0.67, 0.22, 0.42, 0.24, 0.0, -0.18, 0.72, 0.26, 0.38, 3.44, -2.88, 1.83,
                    0.04, 0.3, 0.79, 0.11, -0.02, -0.14, 0.0, 0.36, 0.3, -0.45, 0.9, 0.0, 0.0};
    theta771_last = new double[28]{-3.01, -1.01, -0.06, 0.13, 0.42, 0.18, 0.03, 0.0, -0.51, 0.75, 1.31, 1.26, 2.86, -2.55, 1.5,
                     0.22, 0.05, 0.42, 0.2, -0.06, -0.16, 0.0, 0.53, 0.45, -0.26, 0.44, 0.0, 0.0};

    theta772_start = new double[28]{2.07, -0.44, 0.29, 0.45, 0.32, -0.46, -0.04, 0.0, 0.37, -0.25, 0.16, 0.17, 0.0, 0.0, -2.18,
                      -0.62, -0.16, -1.0, 0.24, 0.72, 0.2, 0.0, 0.12, 0.04, 0.75, -1.29, 3.36, -2.93};
    theta772_mid = new double[28]{1.93, 0.09, 0.16, 0.37, 0.28, -0.18, -0.17, 0.0, 0.02, -0.28, 0.02, 0.13, 0.0, 0.0, -2.3, -1.12,
                    -0.07, -0.63, 0.38, 0.08, 0.16, 0.0, -0.4, 0.43, 0.54, -0.74, 3.47, -3.05};
    theta772_last = new double[28]{1.51, 0.44, -0.01, 0.11, 0.16, -0.16, -0.14, 0.0, -0.17, 0.47, -0.16, 0.02, 0.0, 0.0, -2.79,
                     -0.98, 0.0, 0.14, 0.4, -0.08, 0.0, 0.0, -0.26, 1.25, 0.06, -0.07, 2.32, -2.19};
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
        if (row == 7){
            return utility(board, player);}
        else
            return basic_utility(board, player);

    vector<vector<Move>> moves = board.getAllPossibleMoves(player == 1?2:1);

    if (moves.size() == 0)
        return 5000;

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
        if (row == 7)
            return utility(board, player == 1?2:1);
        else
            return basic_utility(board, player);

    vector<vector<Move>> moves = board.getAllPossibleMoves(player);

    if (moves.size() == 0)
        return - 5000;

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

double StudentAI::utility(Board & board, int color) const
{
//    [wcount, wking, wdis, wback, wedge,
//            wcenter, wdiag, wdog, wbridge, wuptriangle,
//            wdowntriangle, woreo, wmoveable, weatable]
    int wcount[14] = {0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0,
                      0, 0, 0, 0};
    wcount[0] = board.whiteCount;
    int bcount[14] = {0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0,
                      0, 0, 0, 0};
//    double[][] theta;
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

//    for (int i=0;i<12;i++)
//    {
//        std::cout << wcount[i] << " ";
//    }


    if (color == 1)
    {
        moveables(board, 2, wcount);
        bcount[12] = 0;
        bcount[13] = 0;
    }
    else{
        wcount[12] = 0;
        wcount[13] = 0;
        moveables(board, 1, bcount);
    }
    if (player == 1)
//        double** theta_start_mid_last = get_theta_first(row, col);
        if (bcount[0] > 5)
            return calculate_utility(wcount, bcount, theta771_start);
        else if (bcount[0] > 3 && bcount[0] <= 5)
            return calculate_utility(wcount, bcount, theta771_mid);
        else
            return calculate_utility(wcount, bcount, theta771_last);
    else
//        double** theta_start_mid_last = get_theta_backhand(row, col);
        if (wcount[0] > 5)
            return calculate_utility(wcount, bcount, theta772_start);
        else if (wcount[0] > 3 && wcount[0] <= 5)
            return calculate_utility(wcount, bcount, theta772_mid);
        else
            return calculate_utility(wcount, bcount, theta772_last);

//    return calculate_utility(wcount, bcount, theta);

}
