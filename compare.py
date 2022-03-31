#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@duck.com>, 2022
#
def main():
    follower_path = '/home/ferit/Downloads/followers.csv'
    following_path = '/home/ferit/Downloads/following.csv'

    with open(follower_path, 'r') as f:
        follower_list = f.readlines()
        f.close()
    with open(following_path, 'r') as f:
        following_list = f.readlines()
        f.close()

    follower_list.remove(follower_list[0])
    following_list.remove(following_list[0])

    follower_list = [line.split(',')[1] for line in follower_list]
    following_list = [line.split(',')[4] for line in following_list]

    for following in following_list:
        if following not in follower_list:
            print(f'{following} is not following you back.')


if __name__ == '__main__':
    main()
