
def tryOpen(password):
    # TODO
    pass
    

def main():
    for x in range(0, 10000):
        for y in range(0, 10000):
            for r1 in range (0, 256):
                for g1 in range (0, 256):
                    for b1 in range (0, 256):
                        for r2 in range (0, 256):
                            for g2 in range (0, 256):
                                for b2 in range (0, 256):
                                    xy = str(x) + str(y)
                                    rgb1 = '{:0{}X}'.format(r1, 2) + '{:0{}X}'.format(g1, 2) + '{:0{}X}'.format(b1, 2)
                                    rgb2 = '{:0{}X}'.format(r2, 2) + '{:0{}X}'.format(g2, 2) + '{:0{}X}'.format(b2, 2)
                                    tryOpen(xy + rgb1 + rgb2)



if __name__ == "__main__":
    main()
