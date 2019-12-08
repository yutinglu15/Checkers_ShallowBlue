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
//
//
//    def moveables(self, board, color):
//        moves = [m for chess in board.get_all_possible_moves(color) for m in chess]
//        eatable = 0
//        for m in moves:
//            if len(m.seq) > 2:
//                eatable += (len(m.seq) - 1)
//                continue
//            if math.sqrt((m.seq[0][0] - m.seq[1][0]) ** 2 + (m.seq[0][1] - m.seq[1][1]) ** 2) > 1:
//                eatable += 1
//        #print(f"len(moves): {len(moves)}, eatable: {eatable}")
//        return len(moves), eatable
//
//
//    def wback_bback(self, board):
//        bback = sum(board.board[0][i].color == "B" for i in range(board.col))
//        wback = sum(board.board[board.row - 1][i].color == "W" for i in range(board.col))
//        return wback, bback
//
//
//    def wedge_bedge(self, board):
//        bedge = sum(
//            (board.board[i][0].color == "B") + (board.board[i][board.col - 1].color == "B") for i in
//            range(board.row))
//        wedge = sum(
//            (board.board[i][0].color == "W") + (board.board[i][board.col - 1].color == "W") for i in
//            range(board.row))
//        #print(f"wedge: {wedge}, bedge: {bedge}")
//        return wedge , bedge
//
//
//    def wcenter_bcenter(self, board):
//        wcenter = sum((board.board[int(board.row/2)][i].color =="W")+ \
//                      (board.board[int(board.row/2)+1][i].color =="W") for i in range(board.col))
//        bcenter = sum((board.board[int(board.row/2)][i].color == "B")+ \
//                      (board.board[int(board.row/2)+1][i].color =="B") for i in range(board.col))
//        #print(f"wcenter: {wcenter}, bcenter: {bcenter}")
//        return wcenter, bcenter
//
//    def wdiagonal_bdiagonal(self, board):
//        bdiagonal = sum(board.board[i][i].color == "B"  for i in range(board.row//4, 3*board.row//4)) + \
//                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "B"  for i in range(board.row))
//        wdiagonal = sum(board.board[i][i].color == "W"  for i in range(board.row)) + \
//                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "W" for i in range(board.row))
//        #print(f"wdiagonal: {wdiagonal}, bdiagonal: {bdiagonal}")
//        return wdiagonal , bdiagonal
//
//    def wdiag_bdiag(self, board):
//        bc,wc = 0, 0
//        for r in range(board.row-1):
//            bc += (board.board[r][r].color == "B") + (board.board[r+1][r].color == "B") + (board.board[r][r+1].color == "B") \
//                + (board.board[r][board.col-1-r].color == "B") + (board.board[r+1][board.col-1-r].color == "B") +\
//                   (board.board[r][board.col-2-r].color == "B")
//
//            wc += (board.board[r][r].color == "W") + (board.board[r + 1][r].color == "W") + (board.board[r][r + 1].color == "W")\
//                + (board.board[r][board.col-1-r].color == "W") + (board.board[r+1][board.col-1-r].color == "W") +\
//                   (board.board[r][board.col-2-r].color == "W")
//        bc += (board.board[board.row-1][0].color == "B") + (board.board[board.row-1][board.row-1].color == "B")
//        wc += (board.board[board.row - 1][0].color == "W") + (board.board[board.row - 1][board.row - 1].color == "W")
//
//        #print(f"wdiag: {wc}, bdiag: {bc}")
//        return wc, bc
//
//    def wdog_bdog(self, board):
//        wc = (board.board[board.row-1][board.col-1].color == "." and board.board[board.row-1][board.col-2].color == "W" \
//            and board.board[board.row-2][board.col-1].color == "B") +\
//             (board.board[board.row-1][0].color == "." and board.board[board.row-1][1].color == "W"\
//            and board.board[board.row-2][0].color == "B")
//
//        bc = (board.board[0][0].color == "." and board.board[0][1].color == "B" \
//             and board.board[1][0].color == "W") + \
//              (board.board[0][board.col-1].color == "." and board.board[0][board.col-2].color == "B" \
//             and board.board[1][board.col-1].color == "W")
//        #print(f"wdog: {wc}, bdog: {bc}")
//        return wc, bc
//
//
//    def wbridge_bbridge(self, board):
//        bc = sum(board.board[0][c].color == "B" and board.board[0][c+2].color == "B" for c in range(1, board.col - 3))
//        wc = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-1][c + 2].color == "W" for c in range(1, board.col - 3))
//        #print(f"wbridge: {wc}, bbridge: {bc}")
//        return wc, bc
//
//    def wuptriangle_buptriangle(self, board):
//        bcount, wcount = 0, 0
//        for r in range(1, board.row-1):
//            for c in range(board.col-2):
//                if board.board[r][c].color == "B" and board.board[r-1][c+1].color == "B" and board.board[r][c+2].color == "B":
//                    bcount += 1
//                if board.board[r][c].color == "W" and board.board[r-1][c+1].color == "W" and board.board[r][c+2].color == "W":
//                    wcount += 1
//        #print(f"wuptriangle: {wcount}, buptriangle: {bcount}")
//        return wcount, bcount
//
//    def wdowntriangle_bdowntriangle(self, board):
//        bcount, wcount = 0, 0
//        for r in range(board.row-1):
//            for c in range(board.col-2):
//                if board.board[r][c].color == "B" and board.board[r+1][c+1].color == "B" and board.board[r][c+2].color == "B":
//                    bcount += 1
//                if board.board[r][c].color == "W" and board.board[r+1][c+1].color == "W" and board.board[r][c+2].color == "W":
//                    wcount += 1
//        #print(f"wdowntriangle: {wcount}, bdowntriangle: {bcount}")
//        return wcount, bcount
//
//
//    def woreo_boreo(self, board):
//        '''
//        :param board:
//        :return: triangle pattern in the last row
//        '''
//        boreo = sum(board.board[0][c].color == "B" and board.board[1][c+1].color == "B" \
//                    and board.board[0][c+2].color == "B" for c in range(0, board.col-2))
//        woreo = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-2][c+1].color == "W" \
//                    and board.board[board.row-1][c+2].color == "W" for c in range(0, board.col-2))
//        #print(f"woreo: {woreo}, boreo: {boreo}")
//        return woreo, boreo
//
//
//    def wdis_bdis(self, board):
//        wdis = sum(board.row - 1 - i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "W")
//        bdis = sum(i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "B")
//        return wdis, bdis
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
    WB wk_bk = wking_bking(board);
    if (player == 1)
        return 3*board.blackCount + 5*wk_bk.b - 3*board.whiteCount - 5*wk_bk.w;
    return 3*board.whiteCount + 5*wk_bk.w - 3*board.blackCount - 5*wk_bk.b;
}


