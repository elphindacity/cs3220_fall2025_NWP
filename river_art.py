def create_river(state):
    river =    [
        ".___________________________________.",
        "|          |             |          |",
        "|LEFT  BANK|    RIVER    |RIGHT BANK|",
        "|__________|_____________|__________|"]
    river_row = "|          | _ _ _ _ _ _ |          |"
    river.append(river_row)

    chars = ['F','W','G','C']

    for x in range(4):
        river_mod = list(river_row)
        if state[x] == 'L' :
            river_mod[5] = chars[x]
        else:
            river_mod[-6] = chars[x]

        new_river_row = "".join(river_mod)
        river.append(new_river_row)
        if x != 1 :
            river.append(river_row)
        else :
            if state[0] == 'L' :
                row = "|        \_____/ _ _ _ _ |          |"
            else:
                row = "|          | _ _ _ _ \_____/        |"
            river.append(row)
    river.pop()
    river.append("|__________|_____________|__________|")
    return river