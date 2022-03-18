class Direct(object):
    def __init__(self, target):
        for key in target:
            if type(target[key]) == dict:
                child = Direct(target[key])
                exec(f'self.{key} = child')
            else:
                exec(f'self.{key} = target[key]')
            if type(target[key]) == list:
                for item in target[key]:
                    nList = []
                    if type(item) == dict:
                        dItem = Direct(item)
                        nList.append(dItem)
                    else:
                        nList.append(item)
                exec(f'self.{key} = nList')