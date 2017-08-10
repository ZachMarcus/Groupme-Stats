import requests
import math
import json





class GroupMe(object):
    def __init__(self, apiKey):
        self._apiKey = apiKey
        self._groupUrl = "https://api.groupme.com/v3"
        self._groupDict = dict()
        self._ranGetGroups = False

    def _apiCall(self, response):
        """
        Retrieve the 'response' portion of the json object.
        """
        return response.json()['response']

    def getGroups(self):
        """
        Returns a dictionary with group names as keys and a dict
        of group id and # of messages as values.
        """
        params = {'per_page' : 100}
        groups = self._apiCall(requests.get(self._groupUrl + '/groups?token=' + self._apiKey, params=params))
        #print(groups[0])
        #print("\n-----\n")
        if groups is None:
            return None
        self._groupDict = {}
        for group in groups:
            name = group['name'].encode('utf-8').strip()
            count = group['messages']['count']
            if count > 0:
                self._groupDict[name] = {}
                self._groupDict[name]['id'] = group['group_id']
                self._groupDict[name]['count'] = count
        self._ranGetGroups = True
        return self._groupDict

    def getGroupInfoByName(self, groupName):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[groupName.encode()]

    def getGroupIdByName(self, groupName):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[groupName.encode()]['id']

    def getGroupMessageLengthByName(self, groupName):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[groupName.encode()]['count']


    def getLastMessageIdOfGroup(self, groupName):
        params = {}
        groupId = self.getGroupIdByName(groupName)
        lastMessageId = self._apiCall(requests.get(self._groupUrl + '/groups/' + groupId + '/messages?token=' + self._apiKey, params=params))
        return lastMessageId['messages'][0]['id']

    def retrieveMessages(self, filename, groupName, numMessages):
        groupId = self.getGroupIdByName(groupName)
        lastMessageId = self.getLastMessageIdOfGroup(groupName)
        params = {'before_id':lastMessageId, 'limit':100}
        numIterations = math.ceil(numMessages / 100)
        with open(filename, "w+") as f:
            for i in range(0, numIterations):
                msgs = self._apiCall(requests.get(self._groupUrl + '/groups/' + groupId + '/messages?token=' + self._apiKey, params=params))
                #print(msgs['count'])
                lastMessageId = msgs['messages'][0]['id']
                params['before_id']=lastMessageId
                for groupMeMessage in msgs['messages']:
                    f.write(json.dumps(groupMeMessage) + '\n')
                

    def analyzeFile(self, filename):
        """
        Calculate:
        - Who mentions who the most
        - Total individual likes for each person on each person
        - Critical likes:
          - not counting liking yourself
          - critical post=5+likes
          - super critical post=6+likes
          - ultra critical post=7+likes
        """
        messageDict = {}
        with open(filename, "r") as f:
            messages = json.load(f)
            for message in messages:
                messageDict[message['id']]=message
        for message in list(messageDict.values):
            print("hi")









