#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@duck.com>, 2022
#
import urllib.request


# noinspection PyUnreachableCode
def main():
    if False:
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
        following_list = [line.split(',')[1] for line in following_list]
    else:
        follower_path = '/home/ferit/scripts/follower'
        followed_path = '/home/ferit/scripts/followed'
        with open(follower_path, 'r') as f:
            follower_list = f.readlines()
            f.close()
        with open(followed_path, 'r') as f:
            followed_list = f.readlines()
            f.close()

        follower_list = [x.removesuffix('\n') for x in follower_list]
        followed_list = [x.removesuffix('\n') for x in followed_list]

        for followed in followed_list:
            if followed not in follower_list:
                print(followed, 'doesn\'t follow you.')


if __name__ == '__main__':
    main()
