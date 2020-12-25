from twitterUsernameviaUserID import getHandles as twee

"""
Test.py - Testing twitterUsernameviaUserID to make sure everything works.
"""


def sample(
    testCase=["1008016646458335234"],
    condition=["1008016646458335234", "rishi_raj_jain_"],
):
    temp = twee.getHandles(testCase)
    return temp[condition[0]] == condition[1]


def main():
    print("[+] Beginning testing")

    if sample():
        print("\n[+] Testing successfully complete :)")
    else:
        print("\n[-] Testing unsuccessfull :/")


if __name__ == "__main__":
    main()
