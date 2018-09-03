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

    def getGroupInfoByName(self, group_name):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[group_name.encode()]

    def getGroupIdByName(self, group_name):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[group_name.encode()]['id']

    def getGroupMessageLengthByName(self, group_name):
        if not self._ranGetGroups:
            self.getGroups()
        return self._groupDict[group_name.encode()]['count']

    def getLastMessageIdOfGroup(self, group_name):
        params = {}
        groupId = self.getGroupIdByName(group_name)
        lastMessageId = self._apiCall(requests.get(self._groupUrl + '/groups/' + groupId + '/messages?token=' + self._apiKey, params=params))
        return lastMessageId['messages'][0]['id']

    def retrieveMessages(self, filename, group_name, num_messages):
        group_id = self.getGroupIdByName(group_name)
        last_message_id = self.getLastMessageIdOfGroup(group_name)
        params = {'before_id': last_message_id, 'limit': 1}
        num_iterations = int(math.ceil(num_messages / 1))
        print ("Getting " + str(num_iterations) + " messages")

        quarter_done = False
        half_done = False
        three_quarter_done = False
        with open(filename, "w+") as f:
            for i in range(0, num_iterations):

                if i > int(math.ceil(num_iterations/4)) and not quarter_done:
                    print("25%")
                    quarter_done = True
                if i > int(math.ceil(num_iterations/2)) and not half_done:
                    print("50%")
                    half_done = True
                if i > int(math.ceil(3*num_iterations/4)) and not three_quarter_done:
                    print("75%")
                    three_quarter_done = True

                msgs = self._apiCall(requests.get(self._groupUrl + '/groups/' + group_id +
                                                  '/messages?token=' + self._apiKey, params=params))
                last_message_id = msgs['messages'][0]['id']
                params['before_id']=last_message_id
                for groupMeMessage in msgs['messages']:
                    f.write(json.dumps(groupMeMessage) + '\n')
        print("100%")

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

        Message:
            - user_id
            - attachments
            - source_guid
            - text
            - created_at
            - sender_id
            - sender_type
            - system
            - favorited_by
            - avatar_url
            - group_id
            - id
            - name
        """
        names = {}
        criticals = {}
        super_criticals = {}
        ultra_criticals = {}
        for line in open(filename, 'r'):
            message = json.loads(line)
            user_id = message["user_id"]
            names[user_id] = message["name"]

            if user_id not in criticals:
                criticals[user_id] = 0
            if user_id not in super_criticals:
                super_criticals[user_id] = 0
            if user_id not in ultra_criticals:
                ultra_criticals[user_id] = 0

            like_count = len(message["favorited_by"])
            if user_id in message["favorited_by"]:
                like_count = like_count - 1

            if like_count > 4:
                criticals[user_id] = criticals[user_id] + 1
            if like_count > 5:
                super_criticals[user_id] = super_criticals[user_id] + 1
            if like_count > 6:
                ultra_criticals[user_id] = ultra_criticals[user_id] + 1

        for user_id in names:
            print ("{0:>30} {1:>5} {2:>5} {3:>5}".format(names[user_id].encode('utf-8').strip(),
                                                         criticals[user_id],
                                                         super_criticals[user_id],
                                                         ultra_criticals[user_id]))
