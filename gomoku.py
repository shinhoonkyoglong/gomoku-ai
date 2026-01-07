import matplotlib.pyplot as plt
import numpy as np

# 19x19 오목 보드 초기화
board = [[0 for _ in range(19)] for _ in range(19)]


def print_board(board):
    for row in reversed(board):  # 역순으로 출력하여 행이 밑에서부터 증가하도록 함
        print(' '.join(str(cell) for cell in row))


def place_stone(board, x, y, player):
    if board[y][x] == 0:  # 행, 열의 순서를 맞추기 위해 y, x 순서로 접근
        board[y][x] = player
    else:
        raise ValueError("The cell is already occupied")


def is_valid_position(x, y):
    return 0 <= x < 19 and 0 <= y < 19


def is_winning_move(board, x, y, player):
    # Check if placing a stone at (x, y) results in a win for the player
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if is_valid_position(nx, ny) and board[ny][nx] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if is_valid_position(nx, ny) and board[ny][nx] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False


# 일단 완성
def three_rule(board, x, y, player):
    four = False
    # Check if placing a stone at (x, y) can form exactly n in a row for the player

    counter = 1
    if player == 1:
        counter = 2

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    count4 = 0
    count3 = 0

    for dx, dy in directions:
        block_dict = {}
        block_lst = [False, False]  # 위, 중간 벽 확인
        f_lst_idx = None
        s_lst_idx = None
        count = 1  # 연속적이지 않아도  됨
        f_count = 1

        hole1 = False
        hole2 = False
        hole_cnt = 0

        f_lst = []
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if is_valid_position(nx, ny) == False or board[ny][nx] == counter:  # 벽이거나 다른 수
                pre = []
                if len(f_lst) >= 2:
                    pre = f_lst[-1:-3:-1]
                if pre == [1, 0] or hole1 == False:
                    block_lst[0] = True
                break
            elif is_valid_position(nx, ny) == True and board[ny][nx] == player and hole1 == False:
                count += 1
                f_lst.append(1)
            elif is_valid_position(nx, ny) == True and board[ny][nx] == 0:  # hole
                hole_cnt += 1
                if hole_cnt == 1:  # 첫번째 만난 홀, 얘는 취급해줌
                    count += 1
                    hole1 = True
                    f_lst_idx = len(f_lst)
                    f_lst.append(0)
                else:  # 홀이 두번째 이상으로 만난 경우, hole_cnt가 1 초과
                    hole2 = True  # 두번째 hole부터를 벽취급해주는 것

        f_count += (i - 1)

        hole_cnt = 0
        hole1 = False
        hole2 = False
        hole_cnt = 0
        s_lst = []
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if is_valid_position(nx, ny) == False or (is_valid_position(nx, ny) == True and board[ny][nx] == counter):
                pre = []
                if len(s_lst) >= 2:
                    pre = s_lst[-1:-3:-1]
                if pre == [1, 0] or hole1 == False:
                    block_lst[1] = True
                break
            if is_valid_position(nx, ny) == True and board[ny][nx] == player and hole1 == False:
                count += 1
                s_lst.append(1)
            elif is_valid_position(nx, ny) == True and board[ny][nx] == 0:
                hole_cnt += 1
                if hole_cnt == 1:
                    count += 1
                    hole1 = True
                    s_lst_idx = len(s_lst)
                    s_lst.append(0)
                else:
                    hole2 = True  # block count off when meet hole
        f_count += (i - 1)

        if f_count >= 5:

            block_dic = {}
            block_dic[f_lst.count(1) + 1] = block_lst[0]
            block_dic[s_lst.count(1) + 1] = block_lst[1]

            if f_lst_idx != None:
                left_lst = f_lst[:f_lst_idx] + s_lst
            else:
                left_lst = s_lst
            if s_lst_idx != None:
                right_lst = f_lst + s_lst[:s_lst_idx + 1]
            else:
                right_lst = f_lst

            block_dic[left_lst.count(1) + 1] = block_lst[1]
            block_dic[right_lst.count(1) + 1] = block_lst[0]

            max4 = []
            max3 = []
            for key, value in block_dic.items():
                if key == 4:
                    max4.append(value)
                elif key == 3:
                    max3.append(value)
            if False in max4:
                count4 += 1
            elif False in max3:
                count3 += 1
    if count4 + count3 >= 2:
        if count4 >= 1:
            return (True, 4)
        else:
            return (True, 3)
    else:
        return (False, 0)


def can_form_n_in_a_row(board, x, y, player, n):
    # Check if placing a stone at (x, y) can form exactly n in a row for the player
    counter = 1
    if player == 1:
        counter = 2
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        bool_count = True  # 연속적인 count하기 위한
        f_count = 1
        block = True
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if is_valid_position(nx, ny) == False or (
                    is_valid_position(nx, ny) == True and board[ny][nx] == counter):  # 벽이거나 다른 수(적수)
                if bool_count == True:  # 홀을 아직 안 만났음
                    block = False  # 닫힌 경우 볼려고
                break
            elif is_valid_position(nx, ny) == True and board[ny][nx] == player and bool_count:
                count += 1
            elif is_valid_position(nx, ny) == True and board[ny][nx] == 0:
                bool_count = False  # block count off when meet hole
        f_count += (i - 1)

        bool_count = True
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if is_valid_position(nx, ny) == False or (is_valid_position(nx, ny) == True and board[ny][nx] == counter):
                if bool_count == True:
                    block = False
                break
            if is_valid_position(nx, ny) == True and board[ny][nx] == player and bool_count:
                count += 1
            elif is_valid_position(nx, ny) == True and board[ny][nx] == 0:
                bool_count = False
        f_count += (i - 1)

        if f_count >= 5 and count == n:
            if block == True:  # 양쪽열림
                return (True, 1)
            else:
                return (True, 2)
    return (False, 0)


def find_best_move(board, opponent_x, opponent_y):
    coor = None
    # 1. 즉각적인 승리
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                if is_winning_move(board, x, y, 1):
                    print(1)
                    return x, y

    # 2. 상대의 즉각적인 승리 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                if is_winning_move(board, x, y, 2):
                    print(2)
                    return x, y

    # 3-1. 3 4 만들기 공격
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp0 = three_rule(board, x, y, 1)
                if temp0[0] and temp0[1] == 4:  # 4, 3 확인
                    print('3-1')
                    return x, y

    # 3-2. 열린 3을 4목으로 만들기
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 1, 4)
                if temp[0] and temp[1] == 1:
                    print('3-2')
                    return x, y

    # 4-1. 3 4 만들기 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp0 = three_rule(board, x, y, 2)
                if temp0[0] and temp0[1] == 4:  # 4, 3 확인
                    print('4-1')
                    return x, y

    # 4-2. 열린 3을 4목으로 만들기 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 2, 4)
                if temp[0] and temp[1] == 1:
                    print('4-2')
                    return x, y

    # 5. 3-3 만들기
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp0 = three_rule(board, x, y, 1)
                if temp0[0] and temp0[1] == 3:  # 3, 3 확인
                    print('5')
                    return x, y

    # 6.  3-3 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp0 = three_rule(board, x, y, 2)
                if temp0[0] and temp0[1] == 3:  # 3, 3 확인
                    print('6')
                    return x, y

    # 7. 열린 2를 3목 만들기
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 1, 3)
                if temp[0] and temp[1] == 1:
                    print('7')
                    return x, y

    # 8. 닫힌 3을 4목으로 공격
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 1, 4)
                if temp[0] and temp[1] == 2:
                    print('8')
                    return x, y

    # 9. 열린 2를 3목으로 만들려는 것을 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 2, 3)
                if temp[0] and temp[1] == 1:
                    print('9')
                    return x, y

    # 10. 닫힌 3 4목으로 만들려고 하는 것을 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 2, 4)
                if temp[0] and temp[1] == 2:
                    print('10')
                    return x, y

    # 11. 1목을 2목으로 만들기 - 어디에 둘 지 생각해야 함 : 일단은 벽이 없는 쪽으로 - 상대돌이 없는 쪽으로 - 대각선으로
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 1, 2)
                if temp[0]:
                    if temp[1] == 1:
                        print('11-1')
                        return x, y
                    elif temp[1] == 2:
                        coor = (x, y)
    if coor:
        print('11-2')
        return coor

    # 12. 상대의 2목 저지
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                temp = can_form_n_in_a_row(board, x, y, 2, 2)
                if temp[0]:
                    if temp[1] == 1:
                        print('12-1')
                        return x, y
                    elif temp[1] == 2:
                        coor = (x, y)
    if coor:
        print('12-2')
        return coor

    # 모든 주변 자리가 이미 차있다면 임의의 빈 자리 찾기
    for x in range(19):
        for y in range(19):
            if board[y][x] == 0:
                print('last')
                return y, x


def find_move(board, opponent_x, opponent_y):
    has_my_stone = any(cell == 1 for row in board for cell in row)
    if has_my_stone:
        # 보드에 우리 돌이 이미 있으면 우리 돌 주변에 둠
        for y in range(19):
            for x in range(19):
                if board[y][x] == 1:
                    empty_adjacent = find_empty_adjacent(board, x, y)
                    if empty_adjacent:
                        return empty_adjacent


def find_empty_adjacent(board, x, y):
    # 주어진 위치 주변에 빈 공간이 있는지 확인하고 있다면 반환
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if is_valid_position(nx, ny) and board[ny][nx] == 0:
            return nx, ny
    return None


# (아래 수정본)
def plot_board(board):
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 19)
    ax.set_ylim(-1, 19)

    # Draw the grid
    for x in range(19):
        ax.plot([x, x], [-1, 19], color='black', lw=0.5)
    for y in range(19):
        ax.plot([-1, 19], [y, y], color='black', lw=0.5)

    # Draw the stones
    for y in range(19):
        for x in range(19):
            if board[y][x] == 1:
                ax.plot(x, y, 'ko', markersize=10)  # Black stone
            elif board[y][x] == 2:
                ax.plot(x, y, 'ro', markersize=10)  # Red stone

    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Add x and y axis labels
    ax.set_xticks(np.arange(19))
    ax.set_yticks(np.arange(19))
    ax.set_xticklabels([chr(i) for i in range(65, 84)])
    ax.set_yticklabels(np.arange(1, 20)[::-1])

    plt.show()


def convert_input(input_str):
    try:
        x_str, y_str = input_str.strip().split(",")
        x = ord(x_str.upper()) - ord('A')
        y = 19 - int(y_str)
        if not (0 <= x < 19 and 0 <= y < 19):
            raise ValueError("Coordinates out of bounds")
        return x, y
    except Exception as e:
        raise ValueError(f"Invalid input format: {e}")


def main():
    attack = int(input("1이 선공, 0이 후공: "))  # 1이 선공, 0이 후공
    if attack == 1:
        while True:
            try:
                user_input = input("우리의 좌표 입력 (종료하려면 'exit' 입력): ")
                if user_input.lower() == 'exit':
                    return
                user_x, user_y = convert_input(user_input)
                place_stone(board, user_x, user_y, 1)
                break
            except ValueError as e:
                print(e)
                print("잘못된 입력입니다. 다시 입력해주세요.")
    while True:
        try:
            # 사용자의 입력 (상대방의 돌 위치)
            user_input = input("상대방의 좌표 입력 (종료하려면 'exit' 입력): ")
            if user_input.lower() == 'exit':
                break
            user_x, user_y = convert_input(user_input)
            place_stone(board, user_x, user_y, 2)

            # 승리 판단
            if is_winning_move(board, user_x, user_y, 2):
                plot_board(board)
                print(f"상대방이 ({chr(user_x + 65)}, {19 - user_y})에 돌을 놓아 승리했습니다!")
                break

            # 나의 돌을 둘 위치 결정
            my_x, my_y = find_best_move(board, user_x, user_y)
            place_stone(board, my_x, my_y, 1)  # 나의 돌을 1로 표기

            # 결과 출력
            print(f"상대방 의 돌 위치: ({user_input})")
            print(f"나의 돌 위치: ({chr(my_x + 65)}, {19 - my_y})")
            print("현재 보드 상태:")
            plot_board(board)

            # 승리 판단
            if is_winning_move(board, my_x, my_y, 1):
                plot_board(board)
                print(f"내가 ({chr(my_x + 65)}, {19 - my_y})에 돌을 놓아 승리했습니다!")
                break

        except ValueError as e:
            print(f"잘못된 입력입니다: {e}")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


main()



