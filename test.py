from twitterUsernamefromUserID import getHandles as twee
'''
Test.py - Testing TWINT to make sure everything works.
'''

def sample():
    temp= twee.getHandles(['1008016646458335234'])
    return temp['1008016646458335234']=='rishi_raj_jain_'

def main():
    print("[+] Beginning testing")

    if sample():
        print("\n[+] Testing successfully complete :)")
    else:
        print("\n[-] Testing unsuccessfull :/")

if __name__ == '__main__':
    main()