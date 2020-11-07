import json

with open('/home/ubuntu/database/database.json') as file:
    authDic=json.load(file)

    #number of players
    dictionarySize=len(authDic['authorized_Players'])

    def authenticationBool(username, password):
        authenticatedUser = False
        for index in range(0, dictionarySize):
            if (authDic['authorized_Players'][index]['name'] == username):
                if (authDic['authorized_Players'][index]['password'] == password):
                    authenticatedUser = True
                    break
        return authenticatedUser

    #testing function
    canUserPlay=authenticationBool("fritz", "fritz1234")

    if canUserPlay:
       print ("user can authenticate")
    else:
       print ("user can't authenticate")
