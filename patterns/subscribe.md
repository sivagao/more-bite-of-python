### TODO:
- [ ] 感觉这个例子不够好，参考Ruby's Design Pattern那本书的例子

### Summary:
发布/订阅 - 观察者模式 pub/sub
类似事件监听， 可以查看消息中心，了解存在多少信号，信号的订阅者，从而监控程序的运行。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Provider:

    def __init__(self):
        self.msg_queue = []
        self.subscribers = {}

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        if msg not in self.subscribers:
            self.subscribers[msg] = []
            self.subscribers[msg].append(subscriber)  # unfair
        else:
            self.subscribers[msg].append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            if msg in self.subscribers:
                for sub in self.subscribers[msg]:
                    sub.run(msg)
        self.msg_queue = []


class Publisher:

    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)

class Subscriber:

    def __init__(self, name, msg_center):
        self.name = name
        self.provider = msg_center

    def subscribe(self, msg):
        self.provider.subscribe(msg, self)

    def run(self, msg):
        print("%s got %s" % (self.name, msg))

class LikeWatcher(Subscriber):

    def run(self, msg):
        # super(LikeWatcher, self).run(self, msg)
        Subscriber.run(self, msg)
        print("%s like %s" % (self.name, msg))


def main():
    msg_center = Provider()

    tv_show = Publisher(msg_center)
    siva = LikeWatcher("siva", msg_center)
    lulu = Subscriber("lulu", msg_center)
    siva.subscribe("cartoon")
    lulu.subscribe("movie")

    tv_show.publish("cartoon")
    msg_center.update()
    import time
    time.sleep(1)
    tv_show.publish("ads")
    tv_show.publish("movie")
    msg_center.update()

if __name__ == "__main__":
    main()
```