async def stablizer(word) -> bool:
    shifted_list = []
    broken = list(word)
    for x in range(len(broken)):
       try:
           if broken[x] != broken[x+1]:
              shifted_list.append(broken[x])
              shifted_list.append(broken[x+1])
           else:
              pass
       except IndexError:
             shifted_list.append(broken[-1])
    return "".join(sorted(set(shifted_list), key=shifted_list.index))