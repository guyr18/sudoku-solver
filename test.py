from BoardGenerator import BoardGenerator
import time

i = 0
valid = 0
maxAttempts = 100
startTime = time.time()

# It can be noted that all attempts are valid as that check is made within 
# BoardGenerator.generator()
while i < maxAttempts:
    print("i = " + str(i))
    gen = BoardGenerator()
    result, dispatcher = gen.generate(n=9, difficulty=gen.DIFF_HARD)
    valid += 1
    i += 1
calc = (valid / maxAttempts) * 100
endTime = round(time.time() - startTime, 2)
print(str(calc) + "%")
print(str(endTime) + " seconds.")
print("Average time of execution per puzzle: " + str(endTime / maxAttempts) + " seconds.")