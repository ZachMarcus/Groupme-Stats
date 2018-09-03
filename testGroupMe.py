import argparse
import sys
import os
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
    if not args.groupName:
        args.groupName = "Bio/ECE fam"
    if not args.analyzeFile:
        args.analyzeFile = "out.json"
    # if not args.messageToFile:
        # args.messageToFile = "out.json"

    if not args.apiKey:
        args.apiKey = "p1zCWcRIMMa4dkD3yeKooWBmlNbX24CNaRouXeXE"
        # print("Need to specify an apiKey")
        # exit()
    if args.listGroups:
        print("listGroups: " + str(args.listGroups))
    if args.groupName:
        print("groupName: " + args.groupName)

    my_group_me = GroupMe.GroupMe(args.apiKey)

    if args.lastMessageId:
        print("Group message last ID: " + my_group_me.getLastMessageIdOfGroup(args.groupName))
    if args.listGroups:
        print("GroupMe groups:\n" + str(my_group_me.getGroups()))
    if args.groupName:
        print("focusing on group: " + args.groupName)
        print("ID: " + my_group_me.getGroupIdByName(args.groupName))

    if args.groupName and args.messageToFile:
        num_messages_to_retrieve = my_group_me.getGroupMessageLengthByName(args.groupName)
        my_group_me.retrieveMessages(args.messageToFile, args.groupName, num_messages_to_retrieve)

    if args.groupName and args.analyzeFile and os.path.isfile(args.analyzeFile):
        my_group_me.analyzeFile(args.analyzeFile)


if __name__ == "__main__":
    testGroupMe()


