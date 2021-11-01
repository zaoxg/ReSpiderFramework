from typing import List


class Filter:
    def __init__(self, data: List[dict], keys: List[str]):
        self.data = data
        self.keys = keys

    def dup(self):
        ans = []
        s = set()
        for d in self.data:
            fig = tuple(d.get(key) for key in self.keys)
            if fig not in s:
                ans.append(d)
                s.add(fig)
        return ans


if __name__ == '__main__':
    s = [{'name': '1'}, {'name': '2'}, {'name': '1'}]
    print(Filter(s, ['name']).dup())
