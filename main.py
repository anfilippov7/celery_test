import datetime
from tasks import cpu_bound


def main():

    a = cpu_bound.delay(1)
    b = cpu_bound.delay(2)
    c = cpu_bound.delay(3)
    d = cpu_bound.delay(4)
    print([a.result, b.result, c.result, d.result])


start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)