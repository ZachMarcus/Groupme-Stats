import argparse
import sys

import GroupMe

def testGroupMe():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apiKey", help="Specify your API key here, 24 or 30 characters", type=str)
    parser.add_argument("--listGroups", help="display all groups you are a member of",
                                        action="store_true")
    parser.add_argument("--groupName", help="focus on this group for the command", type=str)
    parser.add_argument("--messageToFile", help="Retrieve all messages and store in this filename", type=str)
    parser.add_argument("--analyzeFile", help="Analyze retrieved file of messages", type=str)
    parser.add_argument("--lastMessageId", help="Get last messageId", action="store_true")


    args = parser.parse_args()
    if not args.apiKey:
        print("Need to specify an apiKey")
        exit()
    if args.listGroups:
        print("listGroups: " + str(args.listGroups))
    if args.groupName:
        print("groupName: " + args.groupName)

    myGroupMe = GroupMe.GroupMe(args.apiKey)

    if args.lastMessageId:
        print("Group message last ID: " + myGroupMe.getLastMessageIdOfGroup(args.groupName))
    if args.listGroups:
        print("GroupMe groups:\n" + str(myGroupMe.getGroups()))
    if args.groupName:
        print("focusing on group: " + args.groupName)
        print("ID: " + myGroupMe.getGroupIdByName(args.groupName))

    if args.groupName and args.messageToFile:
        numMessagesToRetrieve = myGroupMe.getGroupMessageLengthByName(args.groupName)
#        numMessagesToRetrieve = 200
        myGroupMe.retrieveMessages(args.messageToFile, args.groupName, numMessagesToRetrieve)

    if args.groupName and args.analyzeFile and os.path.isfile(args.analyzeFile):
        myGroupMe.analyzeFile(args.analyzeFile)


if __name__ == "__main__":

    testGroupMe()


