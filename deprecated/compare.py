#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@duck.com>, 2022
#


def main():
    follower_path = '/home/ferit/scripts/follower'
    followed_path = '/home/ferit/scripts/followed'
    follower2_path = '/home/ferit/scripts/follower2'
    with open(follower_path, 'r') as f:
        follower_list = f.readlines()
        f.close()
    with open(followed_path, 'r') as f:
        followed_list = f.readlines()
        f.close()
    with open(follower2_path, 'r') as f:
        follower2_list = f.readlines()
        f.close()

    follower_list = [x.removesuffix('\n') for x in follower_list]
    followed_list = [x.removesuffix('\n') for x in followed_list]
    follower2_list = [x.removesuffix('\n') for x in follower2_list]

    print('Old method:')
    for followed in followed_list:
        if followed not in follower1_list:
            print(followed, 'doesn\'t follow you back.')

    print('New method:')
    for followed in followed_list:
        if followed not in follower2_list:
            print(followed, 'doesn\t follow you back.')

    print('Who unfollowed me:')
    for old_follower in follower_list:
        if old_follower not in follower2_list:
            print(old_follower, 'unfollowed you.')


if __name__ == '__main__':
    main()
